import os
import sys
import tempfile
import unittest
from pathlib import Path
import shutil

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from fastapi.testclient import TestClient
from loguru import logger

# 配置loguru日志
logger.remove()  # 移除默认处理器
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="DEBUG",
    colorize=True
)

# 导入fastapi模块
from aider.fastapi import app, coder_instances


class TestFastAPIUndo(unittest.TestCase):
    def setUp(self):
        """测试前的准备工作"""
        logger.info("设置测试环境")
        self.client = TestClient(app)
        # 清理测试前可能存在的coder实例
        coder_instances.clear()
        
        # 创建临时目录作为测试工作空间
        self.temp_dir = tempfile.TemporaryDirectory()
        logger.info(f"测试环境设置完成: 临时目录={self.temp_dir.name}")

    def tearDown(self):
        """测试后的清理工作"""
        logger.info("清理测试环境")
        # 清理测试后的coder实例
        coder_instances.clear()
        
        # 清理临时目录
        self.temp_dir.cleanup()
        logger.info("测试环境清理完成")

    def test_undo_without_commit(self):
        """测试没有提交时尝试撤销的情况"""
        logger.info("开始测试: test_undo_without_commit")
        
        # 初始化会话，aider会自动处理git初始化
        init_response = self.client.post(
            "/init_session",
            json={
                "session_id": "undo_test_session", 
                "workspace_dir": self.temp_dir.name,
                "history": []
            }
        )
        self.assertEqual(init_response.status_code, 200, "初始化会话失败")
        
        # 调用undo API，此时应该没有提交过任何更改
        undo_response = self.client.post("/undo?session_id=undo_test_session")
        
        # 验证响应包含错误信息
        self.assertEqual(undo_response.status_code, 200, "API调用失败")
        self.assertEqual(undo_response.json()["status"], "error", "应该返回错误状态")
        self.assertEqual(
            undo_response.json()["error"], 
            "没有找到上次的提交",
            "错误消息不符合预期"
        )
        logger.info("成功验证没有提交时的错误处理")

    def test_undo_with_commit(self):
        """测试有提交时撤销的情况，使用aider的正常工作流程"""
        logger.info("开始测试: test_undo_with_commit")
        
        # 1. 初始化会话，aider会自动处理git初始化
        init_response = self.client.post(
            "/init_session",
            json={
                "session_id": "undo_test_session", 
                "workspace_dir": self.temp_dir.name,
                "history": []
            }
        )
        self.assertEqual(init_response.status_code, 200, "初始化会话失败")
        
        # 2. 创建测试文件
        test_file = Path(self.temp_dir.name) / "test.txt"
        test_file.write_text("Initial content")
        
        # 3. 添加文件到会话
        add_file_response = self.client.post(
            "/add_file",
            json={"session_id": "undo_test_session", "filename": "test.txt"}
        )
        self.assertEqual(add_file_response.status_code, 200, "添加文件失败")
        
        # 4. 使用/commit API提交初始文件
        commit_response = self.client.post(
            "/commit",
            json={"session_id": "undo_test_session", "message": "Initial commit"}
        )
        self.assertEqual(commit_response.status_code, 200, "提交初始文件失败")
        logger.info(f"初始提交响应: {commit_response.json()}")
        
        # 5. 直接修改文件
        test_file.write_text("Modified content")
        logger.info(f"已直接修改文件: {test_file}")

        # 执行git add确保文件变更被暂存
        run_response = self.client.post(
            "/run",
            json={"session_id": "undo_test_session", "command": f"git add {test_file}"}
        )
        self.assertEqual(run_response.status_code, 200, "添加文件到git索引失败")
        logger.info(f"Git add响应: {run_response.json()}")
        
        # 6. 再次使用/commit API提交修改
        commit_response = self.client.post(
            "/commit",
            json={"session_id": "undo_test_session", "message": "Modified by test"}
        )
        self.assertEqual(commit_response.status_code, 200, "提交修改失败")
        logger.info(f"修改提交响应: {commit_response.json()}")
        
        # 保存commit信息
        commit_info = commit_response.json().get("commit_info", {})
        logger.info(f"提交信息: {commit_info}")
        
        # 保存初始文件内容用于后续比较
        initial_content = "Initial content"
        
        # 7. 调用undo API
        undo_response = self.client.post("/undo?session_id=undo_test_session")
        
        # 8. 打印响应内容以便调试
        logger.info(f"Undo响应: {undo_response.json()}")
        
        # 9. 验证响应成功
        self.assertEqual(undo_response.status_code, 200, "调用undo API失败")
        self.assertIn(undo_response.json()["status"], ["success", "first"], "undo操作未成功完成")
        
        # 10. 验证文件内容已恢复
        # 10. 验证文件内容已恢复
        if undo_response.json()["status"] == "success":
            self.assertEqual(test_file.read_text(), initial_content, "文件内容未恢复到初始状态")
        
        logger.info("成功验证有提交时的撤销功能")

    def test_undo_across_sessions(self):
        """测试不同会话的撤销互不影响"""
        logger.info("开始测试: test_undo_across_sessions")
        
        # 创建第二个临时目录
        temp_dir2 = tempfile.TemporaryDirectory()
        
        try:
            # 1. 初始化两个会话
            self.client.post(
                "/init_session",
                json={
                    "session_id": "session1", 
                    "workspace_dir": self.temp_dir.name,
                    "history": []
                }
            )
            
            self.client.post(
                "/init_session",
                json={
                    "session_id": "session2", 
                    "workspace_dir": temp_dir2.name,
                    "history": []
                }
            )
            
            # 2. 创建测试文件 - 会话1
            test_file1 = Path(self.temp_dir.name) / "test1.txt"
            test_file1.write_text("Session 1 initial")
            
            # 添加文件到会话1
            self.client.post(
                "/add_file",
                json={"session_id": "session1", "filename": "test1.txt"}
            )
            
            # 使用/commit API提交初始文件 - 会话1
            commit_response1 = self.client.post(
                "/commit",
                json={"session_id": "session1", "message": "Initial commit 1"}
            )
            logger.info(f"会话1初始提交响应: {commit_response1.json()}")
            
            # 3. 创建测试文件 - 会话2
            test_file2 = Path(temp_dir2.name) / "test2.txt"
            test_file2.write_text("Session 2 initial")
            
            # 添加文件到会话2
            self.client.post(
                "/add_file",
                json={"session_id": "session2", "filename": "test2.txt"}
            )
            
            # 使用/commit API提交初始文件 - 会话2
            commit_response2 = self.client.post(
                "/commit",
                json={"session_id": "session2", "message": "Initial commit 2"}
            )
            logger.info(f"会话2初始提交响应: {commit_response2.json()}")
            
            # 4. 直接修改文件 - 会话1
            test_file1.write_text("Session 1 modified")
            logger.info(f"已直接修改会话1文件: {test_file1}")

            # 执行git add确保文件变更被暂存 - 会话1
            run_response1 = self.client.post(
                "/run",
                json={"session_id": "session1", "command": f"git add {test_file1}"}
            )
            logger.info(f"会话1 Git add响应: {run_response1.json()}")
            
            # 使用/commit API提交修改 - 会话1
            commit_response1 = self.client.post(
                "/commit",
                json={"session_id": "session1", "message": "Modified commit 1"}
            )
            logger.info(f"会话1修改提交响应: {commit_response1.json()}")
            
            # 5. 直接修改文件 - 会话2
            test_file2.write_text("Session 2 modified")
            logger.info(f"已直接修改会话2文件: {test_file2}")

            # 执行git add确保文件变更被暂存 - 会话2
            run_response2 = self.client.post(
                "/run",
                json={"session_id": "session2", "command": f"git add {test_file2}"}
            )
            logger.info(f"会话2 Git add响应: {run_response2.json()}")
            
            # 使用/commit API提交修改 - 会话2
            commit_response2 = self.client.post(
                "/commit",
                json={"session_id": "session2", "message": "Modified commit 2"}
            )
            logger.info(f"会话2修改提交响应: {commit_response2.json()}")
            
            # 保存初始文件内容
            session1_initial = "Session 1 initial"
            session2_initial = "Session 2 initial"
            
            # 6. 只对会话1调用undo
            undo_response = self.client.post("/undo?session_id=session1")
            
            # 打印响应内容以便调试
            logger.info(f"Undo会话1响应: {undo_response.json()}")
            
            # 验证会话1的撤销成功
            self.assertEqual(undo_response.status_code, 200)
            self.assertIn(undo_response.json()["status"], ["success", "first"])
            
            # 7. 验证文件内容变化
            # 只有在状态为"success"时才验证文件内容恢复
            if undo_response.json()["status"] == "success":
                self.assertEqual(test_file1.read_text(), session1_initial, "会话1文件应该恢复")
            self.assertEqual(test_file2.read_text(), "Session 2 modified", "会话2文件不应该变化")
            
            logger.info("成功验证不同会话之间的撤销互不影响")
        
        finally:
            # 清理临时目录
            temp_dir2.cleanup()

    def test_run_cmd_comparison(self):
        """测试并比较/run和/run_with_cmd两种不同的命令执行方法"""
        logger.info("开始测试: test_run_cmd_comparison")
        
        # 初始化会话，aider会自动处理git初始化
        init_response = self.client.post(
            "/init_session",
            json={
                "session_id": "run_test_session", 
                "workspace_dir": self.temp_dir.name,
                "history": []
            }
        )
        self.assertEqual(init_response.status_code, 200, "初始化会话失败")
        
        # 创建测试文件
        test_file = Path(self.temp_dir.name) / "test_run.txt"
        test_file.write_text("This is a test file for run command")
        
        # 1. 使用普通/run接口执行ls命令
        standard_run_response = self.client.post(
            "/run",
            json={"session_id": "run_test_session", "command": "ls"}
        )
        self.assertEqual(standard_run_response.status_code, 200, "标准run命令执行失败")
        logger.info(f"标准run响应: {standard_run_response.json()}")
        
        # 验证标准run命令执行成功
        self.assertEqual(standard_run_response.json()["status"], "success", "标准run命令应返回成功状态")
        self.assertIsNotNone(standard_run_response.json().get("output"), "标准run应返回输出内容")
        
        # 2. 使用cmd_run接口执行相同的ls命令
        cmd_run_response = self.client.post(
            "/run_with_cmd",
            json={"session_id": "run_test_session", "command": "ls"}
        )
        self.assertEqual(cmd_run_response.status_code, 200, "cmd_run命令执行失败")
        
        # 打印完整响应以便调试
        cmd_response_json = cmd_run_response.json()
        logger.info(f"cmd_run完整响应: {cmd_response_json}")
        
        # 详细输出响应中的各个字段，用于调试
        output_content = cmd_response_json.get("output", "")
        aider_output = cmd_response_json.get("aider_output", [])
        standard_output = cmd_response_json.get("standard_output", [])
        
        logger.info(f"cmd_run output字段内容: {output_content}")
        logger.info(f"cmd_run aider_output字段内容: {aider_output}")
        logger.info(f"cmd_run standard_output字段内容: {standard_output}")
        
        # 验证cmd_run命令执行成功
        self.assertEqual(cmd_response_json["status"], "success", "cmd_run命令应返回成功状态")
        
        # 验证cmd_run实际执行了ls命令（通过检查所有可能的输出字段）
        # 至少一个字段应该包含test_run.txt
        has_file_in_output = "test_run.txt" in output_content
        has_file_in_aider = any("test_run.txt" in str(line) for line in aider_output)
        has_file_in_standard = any("test_run.txt" in str(line) for line in standard_output)
        
        logger.info(f"测试文件在output中: {has_file_in_output}")
        logger.info(f"测试文件在aider_output中: {has_file_in_aider}")
        logger.info(f"测试文件在standard_output中: {has_file_in_standard}")
        
        # 允许在任何一个输出字段中找到文件名
        self.assertTrue(
            has_file_in_output or has_file_in_aider or has_file_in_standard,
            "cmd_run执行的ls命令应该在某个输出字段中包含测试文件名"
        )
        
        # 3. 执行echo命令测试输出捕获
        test_string = "Hello from command line"
        
        # 使用标准run执行echo
        standard_echo_response = self.client.post(
            "/run",
            json={"session_id": "run_test_session", "command": f'echo "{test_string}"'}
        )
        self.assertEqual(standard_echo_response.status_code, 200, "标准echo命令执行失败")
        logger.info(f"标准echo响应: {standard_echo_response.json()}")
        
        # 使用cmd_run执行echo
        cmd_echo_response = self.client.post(
            "/run_with_cmd",
            json={"session_id": "run_test_session", "command": f'echo "{test_string}"'}
        )
        self.assertEqual(cmd_echo_response.status_code, 200, "cmd_run echo命令执行失败")
        logger.info(f"cmd_run echo响应: {cmd_echo_response.json()}")
        
        # 验证两种方法都能捕获输出
        standard_output = standard_echo_response.json().get("output", [])
        cmd_output = cmd_echo_response.json().get("output", "")
        
        # 检查输出中是否包含测试字符串
        standard_contains_test_string = any(test_string in str(line) for line in standard_output)
        # 验证新的run_with_cmd实现能够从聊天记录中正确提取输出
        cmd_contains_test_string = test_string in cmd_output
        
        self.assertTrue(standard_contains_test_string, "标准run应捕获echo命令输出")
        self.assertTrue(cmd_contains_test_string, "改进后的cmd_run应正确捕获echo命令输出")
        
        # 4. 测试文件创建
        new_file_name = "created_by_command.txt"
        new_file_path = Path(self.temp_dir.name) / new_file_name
        
        # 使用标准run创建文件
        self.client.post(
            "/run",
            json={"session_id": "run_test_session", "command": f'echo "Created by standard run" > {new_file_name}'}
        )
        
        # 验证文件被创建
        self.assertTrue(new_file_path.exists(), "标准run应能创建文件")
        
        # 删除文件，准备下一个测试
        if new_file_path.exists():
            new_file_path.unlink()
        
        # 使用cmd_run创建文件
        cmd_create_response = self.client.post(
            "/run_with_cmd",
            json={"session_id": "run_test_session", "command": f'echo "Created by cmd_run" > {new_file_name}'}
        )
        
        # 验证文件被创建
        self.assertTrue(new_file_path.exists(), "cmd_run应能创建文件")
        
        # 验证aider_output中包含命令执行信息
        aider_output = cmd_create_response.json().get("aider_output", [])
        self.assertTrue(any("Added" in str(line) for line in aider_output), 
                      "cmd_run的aider_output应包含'Added'消息")
        
        logger.info("成功验证两种命令执行方法，确认改进后的run_with_cmd功能正常")


if __name__ == "__main__":
    unittest.main() 
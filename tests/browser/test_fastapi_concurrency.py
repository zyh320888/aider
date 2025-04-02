import os
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

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

# 现在可以正确导入fastapi模块
from aider.fastapi import app, coder_instances


class TestFastAPIConcurrency(unittest.TestCase):
    def setUp(self):
        logger.info("设置测试环境")
        self.client = TestClient(app)
        # 清理测试前可能存在的coder实例
        coder_instances.clear()
        
        # 创建两个临时目录作为不同的工作空间
        self.temp_dir1 = tempfile.TemporaryDirectory()
        self.temp_dir2 = tempfile.TemporaryDirectory()
        
        # 在临时目录中创建一些测试文件
        self.test_file1 = Path(self.temp_dir1.name) / "test1.txt"
        self.test_file1.write_text("This is test file 1")
        logger.debug(f"创建测试文件1: {self.test_file1}")
        
        self.test_file2 = Path(self.temp_dir2.name) / "test2.txt"
        self.test_file2.write_text("This is test file 2")
        logger.debug(f"创建测试文件2: {self.test_file2}")
        
        logger.info(f"测试环境设置完成: 目录1={self.temp_dir1.name}, 目录2={self.temp_dir2.name}")

    def tearDown(self):
        logger.info("清理测试环境")
        # 清理测试后的coder实例
        coder_instances.clear()
        
        # 清理临时目录
        self.temp_dir1.cleanup()
        self.temp_dir2.cleanup()
        logger.info("测试环境清理完成")

    def test_session_isolation(self):
        """测试不同会话之间的工作目录隔离"""
        # 为两个不同的会话设置不同的工作目录，使用init_session
        response1 = self.client.post(
            "/init_session",
            json={
                "session_id": "session1", 
                "workspace_dir": self.temp_dir1.name,
                "history": []
            }
        )
        self.assertEqual(response1.status_code, 200)
        
        response2 = self.client.post(
            "/init_session",
            json={
                "session_id": "session2", 
                "workspace_dir": self.temp_dir2.name,
                "history": []
            }
        )
        self.assertEqual(response2.status_code, 200)
        
        # 验证会话信息
        response1 = self.client.get("/session/session1")
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.json()["workspace_dir"], self.temp_dir1.name)
        
        response2 = self.client.get("/session/session2")
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.json()["workspace_dir"], self.temp_dir2.name)
        
        # 确认coder实例有两个，并且工作目录设置正确
        self.assertEqual(len(coder_instances), 2)
        self.assertTrue(hasattr(coder_instances["session1"], "cwd"))
        self.assertTrue(hasattr(coder_instances["session2"], "cwd"))
        self.assertEqual(coder_instances["session1"].cwd, self.temp_dir1.name)
        self.assertEqual(coder_instances["session2"].cwd, self.temp_dir2.name)

    def test_concurrent_file_operations(self):
        """测试并发文件操作时的工作目录隔离"""
        # 使用init_session设置工作目录
        self.client.post(
            "/init_session",
            json={
                "session_id": "session1", 
                "workspace_dir": self.temp_dir1.name,
                "history": []
            }
        )
        self.client.post(
            "/init_session",
            json={
                "session_id": "session2", 
                "workspace_dir": self.temp_dir2.name,
                "history": []
            }
        )
        
        # 为session1添加文件
        self.client.post(
            "/add_file",
            json={"session_id": "session1", "filename": "test1.txt"}
        )
        
        # 为session2添加文件
        self.client.post(
            "/add_file",
            json={"session_id": "session2", "filename": "test2.txt"}
        )
        
        # 获取每个会话的文件列表
        response1 = self.client.get("/files?session_id=session1")
        self.assertEqual(response1.status_code, 200)
        self.assertIn("test1.txt", response1.json()["files"])
        self.assertNotIn("test2.txt", response1.json()["files"])
        
        response2 = self.client.get("/files?session_id=session2")
        self.assertEqual(response2.status_code, 200)
        self.assertIn("test2.txt", response2.json()["files"])
        self.assertNotIn("test1.txt", response2.json()["files"])

    def test_concurrent_api_calls(self):
        """测试并发API调用时的工作目录隔离"""
        # 使用init_session设置会话和工作目录
        self.client.post(
            "/init_session",
            json={
                "session_id": "session1", 
                "workspace_dir": self.temp_dir1.name,
                "history": []
            }
        )
        self.client.post(
            "/init_session",
            json={
                "session_id": "session2", 
                "workspace_dir": self.temp_dir2.name,
                "history": []
            }
        )
        
        # 添加文件到会话
        self.client.post(
            "/add_file",
            json={"session_id": "session1", "filename": "test1.txt"}
        )
        self.client.post(
            "/add_file",
            json={"session_id": "session2", "filename": "test2.txt"}
        )
        
        # 定义线程函数模拟并发API调用
        results = {"session1": None, "session2": None}
        errors = []
        
        def call_api_for_session(session_id):
            try:
                # 每个线程都尝试获取文件列表
                response = self.client.get(f"/files?session_id={session_id}")
                results[session_id] = response.json()["files"]
            except Exception as e:
                errors.append(f"Error in {session_id}: {str(e)}")
        
        # 创建并启动线程
        threads = [
            threading.Thread(target=call_api_for_session, args=("session1",)),
            threading.Thread(target=call_api_for_session, args=("session2",))
        ]
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # 验证结果
        self.assertEqual(len(errors), 0, f"应该没有错误，但有: {errors}")
        self.assertIn("test1.txt", results["session1"])
        self.assertNotIn("test2.txt", results["session1"])
        self.assertIn("test2.txt", results["session2"])
        self.assertNotIn("test1.txt", results["session2"])

    def test_chat_with_proper_directory(self):
        """测试聊天功能是否在正确的工作目录中运行"""
        logger.info("开始测试: test_chat_with_proper_directory")
        
        try:
            # 使用init_session设置会话和工作目录
            logger.debug(f"初始化会话session1，工作目录: {self.temp_dir1.name}")
            init_response = self.client.post(
                "/init_session",
                json={
                    "session_id": "session1", 
                    "workspace_dir": self.temp_dir1.name,
                    "history": []
                }
            )
            logger.debug(f"初始化会话响应状态码: {init_response.status_code}")
            self.assertEqual(init_response.status_code, 200, "初始化会话失败，可能是因为无法创建Coder实例")
            
            # 添加文件到会话
            logger.debug("将test1.txt添加到会话")
            add_file_response = self.client.post(
                "/add_file",
                json={"session_id": "session1", "filename": "test1.txt"}
            )
            logger.debug(f"添加文件响应状态码: {add_file_response.status_code}")
            if add_file_response.status_code != 200:
                logger.error(f"添加文件失败: {add_file_response.json()}")
                if 'detail' in add_file_response.json():
                    logger.error(f"错误详情: {add_file_response.json()['detail']}")
            self.assertEqual(add_file_response.status_code, 200, "添加文件失败")
            
            # 使用/files API端点测试，而不是使用/chat端点
            # 这样可以避免依赖真实的LLM响应
            logger.debug("调用/files端点获取文件列表")
            response = self.client.get(
                "/files?session_id=session1"
            )
            logger.debug(f"获取文件列表响应状态码: {response.status_code}")
            
            # 验证API调用成功
            self.assertEqual(response.status_code, 200, "获取文件列表失败")
            
            # 输出完整响应内容以便调试
            logger.debug(f"文件列表响应内容: {response.json()}")
            
            # 检查响应是否包含添加的文件信息
            files_list = response.json().get("files", [])
            self.assertIn("test1.txt", files_list, f"文件列表中未找到test1.txt: {files_list}")
            
            # 验证coder实例状态
            logger.debug("验证coder实例状态")
            self.assertTrue("session1" in coder_instances, "在coder_instances字典中找不到session1")
            session_coder = coder_instances["session1"]
            # 验证coder实例记录了正确的文件
            files = session_coder.get_inchat_relative_files()
            logger.debug(f"coder实例中的文件列表: {files}")
            self.assertIn("test1.txt", files, f"coder实例文件列表中未找到test1.txt: {files}")
        
        except Exception as e:
            logger.error(f"测试过程中出现异常: {str(e)}")
            import traceback
            logger.error(f"异常堆栈: {traceback.format_exc()}")
            raise
        
        logger.info("测试完成: test_chat_with_proper_directory")

    def test_history_preservation(self):
        """测试使用init_session时历史记录的保存"""
        # 创建带有历史记录的会话
        history = [
            {"role": "user", "message": "测试消息1", "timestamp": "2023-04-01T12:00:00Z"},
            {"role": "assistant", "message": "测试回复1", "timestamp": "2023-04-01T12:01:00Z"},
            {"role": "user", "message": "测试消息2", "timestamp": "2023-04-01T12:02:00Z"},
            {"role": "assistant", "message": "测试回复2", "timestamp": "2023-04-01T12:03:00Z"}
        ]
        
        # 使用init_session设置会话、工作目录和历史记录
        response = self.client.post(
            "/init_session",
            json={
                "session_id": "history_session", 
                "workspace_dir": self.temp_dir1.name,
                "history": history
            }
        )
        self.assertEqual(response.status_code, 200)
        
        # 验证coder实例中的历史记录
        self.assertTrue("history_session" in coder_instances)
        session_coder = coder_instances["history_session"]
        # 检查历史消息是否正确保存
        self.assertEqual(len(session_coder.done_messages), len(history))
        # 确认第一条用户消息正确保存
        self.assertEqual(session_coder.done_messages[0]["role"], "user")
        self.assertEqual(session_coder.done_messages[0]["content"], "测试消息1")
        # 确认第二条助手消息正确保存
        self.assertEqual(session_coder.done_messages[1]["role"], "assistant")
        self.assertEqual(session_coder.done_messages[1]["content"], "测试回复1")

    def test_high_concurrency_load(self):
        """测试高并发负载下的API表现"""
        logger.info("开始高并发负载测试")
        
        # 创建10个独立的会话，每个会话有独立的工作目录
        temp_dirs = []
        session_ids = []
        
        for i in range(10):
            temp_dir = tempfile.TemporaryDirectory()
            temp_dirs.append(temp_dir)
            session_id = f"high_concurrency_session_{i}"
            session_ids.append(session_id)
            
            # 初始化会话
            response = self.client.post(
                "/init_session",
                json={
                    "session_id": session_id,
                    "workspace_dir": temp_dir.name,
                    "history": []
                }
            )
            self.assertEqual(response.status_code, 200)
            
            # 为每个会话添加一个唯一的文件
            with open(os.path.join(temp_dir.name, f"file_{i}.txt"), "w") as f:
                f.write(f"Content for session {i}")
            
            # 将文件添加到会话中
            add_file_response = self.client.post(
                "/add_file",
                json={"session_id": session_id, "filename": f"file_{i}.txt"}
            )
            self.assertEqual(add_file_response.status_code, 200)
        
        def run_concurrent_operations(session_id, temp_dir, operation_id):
            """在指定会话上执行多种操作"""
            results = {}
            
            # 获取文件列表
            files_response = self.client.get(f"/files?session_id={session_id}")
            results["files"] = files_response.json()
            
            # 检查会话状态
            session_response = self.client.get(f"/session/{session_id}")
            results["session"] = session_response.json()
            
            # 发送简单聊天消息
            chat_response = self.client.post(
                "/chat",
                json={"session_id": session_id, "message": f"Hello from {operation_id}"}
            )
            results["chat"] = chat_response.json()
            
            return results
        
        # 创建并发线程
        threads = []
        results = {}
        
        for i in range(10):
            for j in range(3):  # 每个会话执行3次操作，总共30个并发操作
                operation_id = f"op_{i}_{j}"
                sid = session_ids[i]
                tdir = temp_dirs[i]
                
                def thread_task(s_id, t_dir, o_id):
                    results[f"{s_id}_{o_id}"] = run_concurrent_operations(s_id, t_dir, o_id)
                
                thread = threading.Thread(
                    target=thread_task,
                    args=(sid, tdir, operation_id)
                )
                threads.append(thread)
        
        # 启动所有线程
        logger.info(f"启动{len(threads)}个并发线程")
        for thread in threads:
            thread.start()
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        logger.info("所有并发线程已完成")
        
        # 验证结果
        for i in range(10):
            session_id = session_ids[i]
            # 检查每个会话的操作结果
            for j in range(3):
                operation_id = f"op_{i}_{j}"
                result_key = f"{session_id}_{operation_id}"
                
                self.assertIn(result_key, results)
                session_result = results[result_key]
                
                # 确认文件列表中包含正确的文件
                self.assertIn("files", session_result)
                file_list = session_result["files"]["files"]
                self.assertIn(f"file_{i}.txt", file_list)
                
                # 确认会话状态正确
                self.assertIn("session", session_result)
                self.assertEqual(session_result["session"]["workspace_dir"], temp_dirs[i].name)
                
                # 确认聊天响应不为空
                self.assertIn("chat", session_result)
                self.assertIn("response", session_result["chat"])
        
        # 清理临时目录
        for temp_dir in temp_dirs:
            temp_dir.cleanup()
        
        logger.info("高并发测试完成")


if __name__ == "__main__":
    unittest.main() 
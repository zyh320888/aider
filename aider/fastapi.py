#!/usr/bin/env python

import os
import sys
from typing import List, Optional, Dict, Any
from loguru import logger

# 配置loguru
# 移除默认的处理器
logger.remove()

# 添加控制台处理器，根据环境变量控制日志级别
log_level = os.getenv("AIDER_LOG_LEVEL", "INFO")
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=log_level,
    colorize=True
)

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from fastapi.responses import JSONResponse, StreamingResponse
import json
import asyncio

from aider import urls
from aider.coders import Coder
from aider.main import main as cli_main
from aider.io import InputOutput
from aider.scrape import Scraper

# 在导入模块后添加补丁，禁用版本检查中的sys.exit
import aider.versioncheck
original_install_upgrade = aider.versioncheck.install_upgrade

# 替换原始函数，防止sys.exit()调用
def patched_install_upgrade(io, latest_version):
    io.tool_output(f"检测到新版本 {latest_version}，但在API模式下不会自动退出安装。")
    io.tool_output(f"请手动运行: pip install --upgrade aider-chat")
    return

# 应用补丁
aider.versioncheck.install_upgrade = patched_install_upgrade


class CaptureIO(InputOutput):
    """捕获工具输出的IO类"""
    lines = []

    def tool_output(self, msg, log_only=False):
        if not log_only:
            self.lines.append(msg)
        super().tool_output(msg, log_only=log_only)

    def tool_error(self, msg):
        self.lines.append(msg)
        super().tool_error(msg)

    def tool_warning(self, msg):
        self.lines.append(msg)
        super().tool_warning(msg)

    def get_captured_lines(self):
        lines = self.lines
        self.lines = []
        return lines


class CommandCaptureIO(CaptureIO):
    """专门用于捕获命令执行的所有输出，不进行过滤"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 重新初始化lines列表，确保不会共享父类的静态列表
        self.lines = []
    
    def tool_output(self, msg, log_only=False):
        # 记录所有输出，用于调试
        logger.debug(f"CommandCaptureIO收到输出: {msg}")
        super().tool_output(msg, log_only=log_only)
    
    def get_all_output(self):
        # 返回所有捕获的输出
        lines = self.lines
        logger.debug(f"CommandCaptureIO返回所有输出: {lines}")
        return lines


# 全局Coder实例缓存
coder_instances = {}


# 请求和响应模型
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


# 添加对话历史模型，用于恢复历史记录
class ChatHistoryItem(BaseModel):
    role: str
    message: str
    timestamp: Optional[str] = None


class ChatHistoryRequest(BaseModel):
    session_id: str = "default"
    history: List[ChatHistoryItem]


class ChatResponse(BaseModel):
    response: str
    edits: Optional[Dict[str, Any]] = None


class StreamChunk(BaseModel):
    content: str
    done: bool = False
    edits: Optional[Dict[str, Any]] = None


class FileRequest(BaseModel):
    filename: str
    session_id: str = "default"


class FilesResponse(BaseModel):
    files: List[str]


class WebContentRequest(BaseModel):
    url: str
    session_id: str = "default"


class WebContentResponse(BaseModel):
    content: Optional[str] = None
    error: Optional[str] = None


class WorkspaceDirRequest(BaseModel):
    workspace_dir: str
    session_id: str = "default"


# 添加一体化会话初始化请求模型
class SessionInitRequest(BaseModel):
    session_id: str
    workspace_dir: str
    history: List[ChatHistoryItem] = []


app = FastAPI(title="Aider API", description="与Aider对话并编辑代码的API")

# 添加CORS中间件以允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 获取项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.get("/")
async def root():
    """API根路径，返回基本信息"""
    return {
        "name": "Aider API",
        "description": "通过API与Aider交互",
        "documentation": urls.website,
    }

@app.get("/session/{session_id}")
async def check_session(session_id: str):
    """检查会话是否存在并返回会话信息"""
    try:
        logger.info(f"检查会话状态 - session_id: {session_id}")
        exists = session_id in coder_instances
        workspace_dir = None
        
        if exists:
            coder = coder_instances[session_id]
            # 获取当前工作目录
            try:
                # 首先尝试从coder实例获取工作目录
                if hasattr(coder, 'cwd'):
                    workspace_dir = coder.cwd
                else:
                    # 如果没有cwd属性，尝试获取当前工作目录
                    workspace_dir = os.getcwd()
                
                # 验证工作目录是否存在且可写
                if workspace_dir and os.path.exists(workspace_dir) and os.access(workspace_dir, os.W_OK):
                    logger.info(f"会话存在，有效工作目录: {workspace_dir}")
                else:
                    # 如果工作目录不存在或不可写，将其标记为None
                    logger.warning(f"会话存在但工作目录无效: {workspace_dir}")
                    workspace_dir = None
            except Exception as e:
                logger.warning(f"获取工作目录失败: {str(e)}")
                workspace_dir = None
        else:
            logger.info(f"会话不存在: {session_id}")
            
        return {
            "exists": exists,
            "workspace_dir": workspace_dir,
            "valid": exists and workspace_dir is not None
        }
    except Exception as e:
        logger.error(f"检查会话状态失败: {str(e)}")
        return {
            "exists": False,
            "workspace_dir": None,
            "valid": False,
            "error": str(e)
        }


def get_coder(session_id: str = "default", workspace_dir: str = None, history: List[ChatHistoryItem] = None):
    """获取或创建一个Coder实例，可选择从历史记录恢复对话上下文"""
    logger.info(f"获取Coder实例 - session_id: {session_id}, workspace_dir: {workspace_dir}")
    
    # 保存当前工作目录，以便在操作完成后恢复
    original_dir = os.getcwd()
    logger.info(f"保存原始工作目录: {original_dir}")
    
    try:
        if session_id not in coder_instances:
            current_dir = workspace_dir or os.getcwd()
            logger.info(f"创建新的Coder实例，工作目录: {current_dir}")
            
            try:
                # 临时切换到工作目录进行初始化
                os.chdir(current_dir)
                logger.info(f"已切换到工作目录: {current_dir}")
                
                # 设置命令行参数，从环境变量读取配置
                cli_args = ["--yes-always","--no-suggest-shell-commands"]  # 基本参数
                
                # 指定中文回答
                cli_args.extend(["--chat-language","中文"])
                logger.info(f"已设置中文回答")

                # 读取配置文件路径
                config_file = os.environ.get("AIDER_CONFIG_FILE")
                if config_file:
                    cli_args.extend(["--config", config_file])
                    logger.info(f"使用配置文件: {config_file}")
                
                # 读取模型元数据文件路径
                model_metadata_file = os.environ.get("AIDER_MODEL_METADATA_FILE")
                if model_metadata_file:
                    cli_args.extend(["--model-metadata-file", model_metadata_file])
                    logger.info(f"使用模型元数据文件: {model_metadata_file}")
                
                # 读取模型设置文件路径
                model_settings_file = os.environ.get("AIDER_MODEL_SETTINGS_FILE")
                if model_settings_file:
                    cli_args.extend(["--model-settings-file", model_settings_file])
                    logger.info(f"使用模型设置文件: {model_settings_file}")
                
                # 创建Coder实例并传递命令行参数
                coder = cli_main(argv=cli_args, return_coder=True)
                
                if not isinstance(coder, Coder):
                    raise ValueError(f"无法创建Coder实例: {coder}")
                
                # 配置IO捕获
                io = CaptureIO(
                    pretty=False,
                    dry_run=coder.io.dry_run,
                    encoding=coder.io.encoding,
                )
                coder.commands.io = io
                
                # 配置流式输出
                coder.yield_stream = True
                coder.stream = True
                coder.pretty = False
                
                # 存储工作目录信息到coder实例 - 关键步骤
                coder.cwd = current_dir
                
                # 如果提供了历史记录，恢复对话上下文
                if history:
                    logger.info(f"恢复对话历史记录，共 {len(history)} 条消息")
                    for item in history:
                        if item.role == "user":
                            # 添加用户消息到历史记录
                            coder.done_messages.append({
                                "role": "user", 
                                "content": item.message
                            })
                        elif item.role == "assistant":
                            # 添加助手消息到历史记录
                            coder.done_messages.append({
                                "role": "assistant",
                                "content": item.message
                            })
                    logger.info(f"已恢复对话历史记录")
                
                coder_instances[session_id] = coder
                logger.info(f"已创建并缓存Coder实例: {session_id}")
                
            except Exception as e:
                logger.error(f"创建Coder实例失败: {str(e)}")
                raise
        elif workspace_dir:
            # 如果会话已存在但需要更新工作目录
            logger.info(f"更新现有Coder实例的工作目录: {workspace_dir}")
            coder_instances[session_id].cwd = workspace_dir
    
    finally:
        # 确保恢复原始工作目录
        os.chdir(original_dir)
        logger.info(f"已恢复到原始工作目录: {original_dir}")
    
    return coder_instances[session_id]


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """向LLM发送消息并获取回复（非流式）"""
    try:
        coder = get_coder(request.session_id)
        
        # 保存当前工作目录
        original_dir = os.getcwd()
        logger.info(f"保存聊天前的原始工作目录: {original_dir}")
        
        try:
            # 如果coder有指定的工作目录，则切换到该目录
            if hasattr(coder, 'cwd') and coder.cwd:
                os.chdir(coder.cwd)
                logger.info(f"已切换到会话工作目录: {coder.cwd}")
            
            # 记录输入历史
            coder.io.add_to_input_history(request.message)
            
            # 添加强制中文回复的处理
            chat_message = request.message
            if not chat_message.startswith("/"):
                # 添加中文提醒前缀
                chat_message = "请用中文回答以下问题:\n" + chat_message
            
            # 运行对话
            response = coder.run(chat_message)
            
            # 处理编辑信息
            edit_info = None
            if coder.aider_edited_files:
                edit_info = {
                    "files": list(coder.aider_edited_files),
                }
                
                if coder.last_aider_commit_hash:
                    edit_info["commit_hash"] = coder.last_aider_commit_hash
                    edit_info["commit_message"] = coder.last_aider_commit_message
                    
                    # 获取diff
                    if coder.repo:
                        commits = f"{coder.last_aider_commit_hash}~1"
                        diff = coder.repo.diff_commits(
                            coder.pretty,
                            commits,
                            coder.last_aider_commit_hash,
                        )
                        edit_info["diff"] = diff
            
            # 构建响应
            result = {
                "response": response,
                "edits": edit_info
            }
            
            return result
        
        finally:
            # 确保恢复原始工作目录
            os.chdir(original_dir)
            logger.info(f"已恢复聊天后的原始工作目录: {original_dir}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """向LLM发送消息并获取流式回复"""
    try:
        coder = get_coder(request.session_id)
        
        # 保存当前工作目录
        original_dir = os.getcwd()
        logger.info(f"保存流式聊天前的原始工作目录: {original_dir}")
        
        try:
            # 如果coder有指定的工作目录，则切换到该目录
            if hasattr(coder, 'cwd') and coder.cwd:
                os.chdir(coder.cwd)
                logger.info(f"已切换到会话工作目录: {coder.cwd}")
            
            # 记录输入历史
            coder.io.add_to_input_history(request.message)
            
            # 创建一个生成器来产生流式响应
            async def response_generator():
                # 运行聊天并获取流式响应
                buffer = ""
                
                # 添加提示词强制要求使用中文回复
                # 如果消息不是以特殊命令开头，添加中文提示
                chat_message = request.message
                if not chat_message.startswith("/"):
                    # 添加中文提醒前缀
                    chat_message = "请用中文回答以下问题:\n" + chat_message
                
                for chunk in coder.run_stream(chat_message):
                    buffer += chunk
                    # 构建流式响应片段
                    yield json.dumps({
                        "content": chunk,
                        "done": False,
                        "edits": None
                    }) + "\n"
                    
                    # 为了节省带宽，可以设置更大的缓冲区，这里简单处理
                    await asyncio.sleep(0.01)
                
                # 最后返回编辑信息（如果有）
                edit_info = None
                logger.debug(f"检查编辑文件: {coder.aider_edited_files}")  # 添加日志
                
                if coder.aider_edited_files:
                    edit_info = {
                        "files": list(coder.aider_edited_files),
                    }
                    logger.debug(f"编辑信息: {edit_info}")  # 添加日志
                    
                    if coder.last_aider_commit_hash:
                        edit_info["commit_hash"] = coder.last_aider_commit_hash
                        
                        # base64 编码提交消息
                        if coder.last_aider_commit_message:
                            edit_info["commit_message"] = coder.last_aider_commit_message
                        
                        logger.debug(f"提交哈希: {coder.last_aider_commit_hash}")  # 添加日志
                        logger.debug(f"提交消息: {coder.last_aider_commit_message}")  # 添加日志
                        
                        # 获取diff
                        if coder.repo:
                            commits = f"{coder.last_aider_commit_hash}~1"
                            logger.debug(f"获取diff，比较提交: {commits} 和 {coder.last_aider_commit_hash}")  # 添加日志
                            diff = coder.repo.diff_commits(
                                coder.pretty,
                                commits,
                                coder.last_aider_commit_hash,
                            )
                            
                            if diff:
                                edit_info["diff"] = diff
                            
                            logger.debug(f"生成的diff: {diff}")  # 添加日志
                    
                    # 读取修改后的文件内容 - 注意这里需要使用正确的工作目录
                    updated_files = []
                    for filename in edit_info["files"]:
                        try:
                            logger.debug(f"读取文件: {filename}")  # 添加日志
                            # 构建完整的文件路径，基于会话的工作目录
                            full_path = os.path.join(coder.cwd, filename) if not os.path.isabs(filename) else filename
                            logger.info(f"尝试读取文件的完整路径: {full_path}")
                            
                            with open(full_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                
                            # 确定文件类型
                            ext = filename.split('.')[-1].lower() if '.' in filename else ''
                            file_type = 'text'
                            if ext in ['html', 'htm']:
                                file_type = 'html'
                            elif ext == 'css':
                                file_type = 'css'
                            elif ext == 'js':
                                file_type = 'javascript'
                            elif ext == 'tsx':
                                file_type = 'typescriptreact'
                            elif ext == 'ts':
                                file_type = 'typescript'
                            elif ext == 'json':
                                file_type = 'json'
                            elif ext == 'md':
                                file_type = 'markdown'
                                
                            # 创建文件对象
                            updated_files.append({
                                "name": filename,
                                "content": content,
                                "type": file_type,
                                "is_main": filename.endswith('index.html') or ext == 'tsx'
                            })
                            logger.debug(f"成功读取文件: {filename}, 类型: {file_type}")
                        except Exception as e:
                            logger.error(f"读取文件失败 {filename}: {str(e)}")
                    
                    # 将文件内容添加到编辑信息中
                    edit_info["updated_files"] = updated_files
                
                # 返回完成标记和编辑信息
                yield json.dumps({
                    "content": "",
                    "done": True,
                    "edits": edit_info
                })
            
            # 返回流式响应
            return StreamingResponse(
                response_generator(),
                media_type="application/x-ndjson"
            )
            
        finally:
            # 确保恢复原始工作目录
            os.chdir(original_dir)
            logger.info(f"已恢复流式聊天后的原始工作目录: {original_dir}")
            
    except Exception as e:
        logger.error(f"发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/files", response_model=FilesResponse)
async def get_files(session_id: str = "default"):
    """获取当前聊天中的文件"""
    try:
        logger.info(f"获取文件列表 - session_id: {session_id}")
        coder = get_coder(session_id)
        
        # 保存当前工作目录
        original_dir = os.getcwd()
        logger.info(f"保存获取文件列表前的原始工作目录: {original_dir}")
        
        try:
            # 如果coder有指定的工作目录，则切换到该目录
            if hasattr(coder, 'cwd') and coder.cwd:
                os.chdir(coder.cwd)
                logger.info(f"已切换到会话工作目录: {coder.cwd}")
            
            files = coder.get_inchat_relative_files()
            logger.info(f"获取到的文件列表: {files}")
            return {"files": files}
            
        finally:
            # 确保恢复原始工作目录
            os.chdir(original_dir)
            logger.info(f"已恢复获取文件列表后的原始工作目录: {original_dir}")
            
    except Exception as e:
        logger.error(f"获取文件列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/all_files", response_model=FilesResponse)
async def get_all_files(session_id: str = "default"):
    """获取所有可添加到聊天的文件"""
    try:
        coder = get_coder(session_id)
        return {"files": list(coder.get_all_relative_files())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add_file")
async def add_file(request: FileRequest):
    """添加文件到聊天中"""
    try:
        logger.info(f"尝试添加文件 - 文件名: {request.filename}, 会话ID: {request.session_id}")
        coder = get_coder(request.session_id)
        
        # 保存当前工作目录
        original_dir = os.getcwd()
        logger.info(f"保存添加文件前的原始工作目录: {original_dir}")
        
        try:
            # 如果coder有指定的工作目录，则切换到该目录
            if hasattr(coder, 'cwd') and coder.cwd:
                os.chdir(coder.cwd)
                logger.info(f"已切换到会话工作目录: {coder.cwd}")
            
            # 记录当前工作目录
            current_dir = os.getcwd()
            logger.info(f"当前工作目录: {current_dir}")
            
            # 记录路径信息
            is_abs_path = os.path.isabs(request.filename)
            logger.info(f"是否为绝对路径: {is_abs_path}")
            
            # 尝试获取文件的绝对路径和相对路径
            abs_path = os.path.abspath(request.filename)
            try:
                rel_path = os.path.relpath(request.filename, current_dir)
            except ValueError:
                rel_path = request.filename
                
            logger.info(f"文件绝对路径: {abs_path}")
            logger.info(f"相对于当前目录的路径: {rel_path}")
            
            # 检查原始文件是否存在
            orig_exists = os.path.exists(request.filename)
            logger.info(f"原始路径文件是否存在: {orig_exists}")
            
            # 检查绝对路径文件是否存在
            abs_exists = os.path.exists(abs_path)
            logger.info(f"绝对路径文件是否存在: {abs_exists}")
            
            # 如果需要，创建一个临时文件来测试路径解析
            if not orig_exists and not abs_exists:
                logger.warning(f"文件在指定路径下不存在: {request.filename}")
            
            # 添加文件到Aider会话
            logger.info(f"将文件 {request.filename} 添加到会话")
            coder.add_rel_fname(request.filename)
            
            # 记录添加后的文件列表
            files_in_chat = coder.get_inchat_relative_files()
            logger.info(f"添加后的会话文件列表: {files_in_chat}")
            
            return {"status": "success", "message": f"已将 {request.filename} 添加到聊天中"}
            
        finally:
            # 确保恢复原始工作目录
            os.chdir(original_dir)
            logger.info(f"已恢复添加文件后的原始工作目录: {original_dir}")
            
    except Exception as e:
        logger.error(f"添加文件失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/remove_file")
async def remove_file(request: FileRequest):
    """从聊天中移除文件"""
    try:
        coder = get_coder(request.session_id)
        coder.drop_rel_fname(request.filename)
        return {"status": "success", "message": f"已从聊天中移除 {request.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/clear_history")
async def clear_history(session_id: str = "default"):
    """清除聊天历史"""
    try:
        coder = get_coder(session_id)
        coder.done_messages = []
        coder.cur_messages = []
        return {"status": "success", "message": "已清除聊天历史"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/undo")
async def undo_commit(session_id: str = "default"):
    """撤销最后一次提交"""
    try:
        coder = get_coder(session_id)
        
        # 确保这是最新的Aider提交
        if not coder.last_aider_commit_hash:
            logger.warning(f"会话 {session_id} 没有找到上次的提交")
            return {
                "status": "error",
                "error": "没有找到上次的提交"
            }
        
        # 保存当前工作目录
        original_dir = os.getcwd()
        logger.info(f"保存撤销提交前的原始工作目录: {original_dir}")
        
        try:
            # 如果coder有指定的工作目录，则切换到该目录
            if hasattr(coder, 'cwd') and coder.cwd:
                os.chdir(coder.cwd)
                logger.info(f"已切换到会话工作目录: {coder.cwd}")
            
            # 保存当前的提交哈希用于日志
            current_hash = coder.last_aider_commit_hash
            
            # 清空之前捕获的输出
            if hasattr(coder.commands.io, 'get_captured_lines'):
                coder.commands.io.get_captured_lines()
            
            # 使用Aider内置的cmd_undo方法撤销提交
            logger.info(f"调用cmd_undo撤销提交: {current_hash}")
            try:
                # 使用raw_cmd_undo直接执行撤销操作
                coder.commands.raw_cmd_undo("")
                
                # 获取捕获的输出信息
                output = []
                if hasattr(coder.commands.io, 'get_captured_lines'):
                    output = coder.commands.io.get_captured_lines()
                
                logger.info(f"撤销提交输出: {output}")
                
                # 检查输出是否包含错误消息
                error_messages = [
                    "Cannot undo",
                    "Unable to ",
                    "Error ",
                    "not made by aider",
                    "more than 1 parent",
                    "has uncommitted changes",
                    "not in the repository"
                ]
                
                # first commit 单独处理，不作为错误
                is_first_commit = False
                for line in output:
                    if "first commit" in line:
                        is_first_commit = True
                        break
                
                if is_first_commit:
                    # 对first commit情况进行友好提示，视为正常情况
                    return {
                        "status": "first",
                        "message": "这是仓库中的第一个提交，无法继续撤销。",
                        "output": output
                    }
                
                # 处理其他真正的错误情况
                for line in output:
                    for error_msg in error_messages:
                        if error_msg in line:
                            logger.error(f"撤销失败: {line}")
                            return {
                                "status": "error",
                                "error": line
                            }
                
                return {
                    "status": "success",
                    "message": f"已撤销最后一次提交 ({current_hash})",
                    "output": output
                }
            except Exception as e:
                logger.error(f"调用cmd_undo失败: {str(e)}")
                return {
                    "status": "error",
                    "error": f"撤销提交失败: {str(e)}"
                }
            
        finally:
            # 确保恢复原始工作目录
            os.chdir(original_dir)
            logger.info(f"已恢复撤销提交后的原始工作目录: {original_dir}")
            
    except Exception as e:
        logger.error(f"撤销提交失败: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }


class RunCommandRequest(BaseModel):
    command: str
    session_id: str = "default"


@app.post("/run")
async def run_command(request: RunCommandRequest):
    """运行shell命令（等同于/run聊天命令）"""
    try:
        # 获取coder实例
        coder = get_coder(request.session_id)
        
        # 保存当前工作目录
        original_dir = os.getcwd()
        logger.info(f"保存运行命令前的原始工作目录: {original_dir}")
        
        try:
            # 如果coder有指定的工作目录，则切换到该目录
            cwd = None
            if hasattr(coder, 'cwd') and coder.cwd:
                cwd = coder.cwd
                logger.info(f"将在会话工作目录执行命令: {cwd}")
            else:
                cwd = original_dir
                logger.info(f"将在原始工作目录执行命令: {cwd}")
            
            # 直接使用subprocess执行命令，不通过cmd_run方法
            import subprocess
            process = subprocess.Popen(
                request.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                text=True,
                encoding=sys.stdout.encoding,
                errors="replace",
                cwd=cwd
            )
            
            # 捕获输出
            output_lines = []
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                output_lines.append(line.rstrip())
            
            # 等待进程完成并获取返回码
            exit_status = process.wait()
            combined_output = "\n".join(output_lines)
            
            # 记录进程执行结果
            logger.info(f"命令执行完成，返回码: {exit_status}")
            
            # 清空之前捕获的输出
            if hasattr(coder.commands.io, 'get_captured_lines'):
                coder.commands.io.get_captured_lines()
            
            # 将命令输出添加到coder的IO捕获中
            coder.commands.io.tool_output(combined_output)
            
            # 重新获取捕获的输出
            io_output = []
            if hasattr(coder.commands.io, 'get_captured_lines'):
                io_output = coder.commands.io.get_captured_lines()
            
            return {
                "status": "success",
                "output": io_output or output_lines,
                "exit_status": exit_status
            }
            
        finally:
            # 确保恢复原始工作目录
            os.chdir(original_dir)
            logger.info(f"已恢复运行命令后的原始工作目录: {original_dir}")
            
    except Exception as e:
        logger.error(f"运行命令失败: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }


@app.post("/run_with_cmd")
async def run_with_cmd(request: RunCommandRequest):
    """使用coder.commands.cmd_run方法运行shell命令并从聊天记录中获取输出"""
    try:
        # 获取coder实例
        coder = get_coder(request.session_id)
        
        # 保存当前工作目录
        original_dir = os.getcwd()
        logger.info(f"保存使用cmd_run运行命令前的原始工作目录: {original_dir}")
        
        try:
            # 如果coder有指定的工作目录，则切换到该目录
            if hasattr(coder, 'cwd') and coder.cwd:
                os.chdir(coder.cwd)
                logger.info(f"已切换到会话工作目录: {coder.cwd}")
            
            # 记录当前消息数量，用于之后检测新消息
            cur_messages_before = len(coder.cur_messages)
            logger.info(f"命令执行前的消息数量: {cur_messages_before}")
            
            # 清空之前捕获的输出
            if hasattr(coder.commands.io, 'get_captured_lines'):
                coder.commands.io.get_captured_lines()
            
            # 使用asyncio.to_thread将coder.commands.cmd_run包装为异步函数
            import asyncio
            logger.info(f"使用asyncio.to_thread调用cmd_run执行命令: {request.command}")
            
            # 定义同步函数以在线程中执行
            def run_cmd_in_thread():
                try:
                    # 保存原始io
                    original_io = coder.commands.io
                    original_yes = False
                    if hasattr(original_io, 'yes'):
                        original_yes = original_io.yes
                    
                    # 创建并使用新的CommandCaptureIO
                    command_io = CommandCaptureIO(
                        pretty=False,
                        yes=True,  # 自动确认所有提示
                        dry_run=original_io.dry_run,
                        encoding=original_io.encoding,
                    )
                    coder.commands.io = command_io
                    logger.info("已替换为CommandCaptureIO并设置yes=True以避免交互式提示")
                    
                    try:
                        # 清空lines以确保干净的开始
                        command_io.lines = []
                        
                        # 执行命令，故意不设置add_on_nonzero_exit，让confirm_ask生效
                        # 由于设置了yes=True，confirm_ask会自动返回True
                        result = coder.commands.cmd_run(request.command, False)
                        
                        # 获取所有输出
                        all_lines = command_io.lines
                        logger.info(f"CMD_RUN捕获的所有输出: {all_lines}")
                        
                        return result, all_lines
                    finally:
                        # 恢复原始io配置
                        coder.commands.io = original_io
                except Exception as e:
                    logger.error(f"线程中执行cmd_run失败: {str(e)}")
                    return None, []
            
            # 在线程中异步执行cmd_run
            result, aider_output = await asyncio.to_thread(run_cmd_in_thread)
            logger.info(f"cmd_run执行结果: {result}, Aider输出行数: {len(aider_output)}")
            
            # 输出执行后的消息数量
            cur_messages_after = len(coder.cur_messages)
            logger.info(f"命令执行后的消息数量: {cur_messages_after}, 增加了: {cur_messages_after - cur_messages_before} 条消息")
            
            # 从聊天记录中获取实际命令输出
            cmd_output = None
            if cur_messages_after > cur_messages_before:
                # 查找新增的用户消息，这应该是包含命令输出的消息
                for i in range(cur_messages_before, cur_messages_after):
                    msg = coder.cur_messages[i]
                    if msg['role'] == 'user' and f"I ran this command:\n\n{request.command}" in msg['content']:
                        # 提取输出部分
                        parts = msg['content'].split("And got this output:\n\n")
                        if len(parts) > 1:
                            cmd_output = parts[1]
                            logger.info(f"从聊天历史中提取到命令输出 ({len(cmd_output)} 字节)")
                            break
            
            # 如果无法从聊天记录中获取，返回提示信息
            if cmd_output is None:
                logger.warning("无法从聊天历史中获取命令输出")
                cmd_output = "命令已执行，但无法获取详细输出。请查看aider输出了解更多信息。"
            
            # 获取标准捕获的输出（包含aider的提示）
            standard_output = []
            if hasattr(coder.commands.io, 'get_captured_lines'):
                standard_output = coder.commands.io.get_captured_lines()
                logger.info(f"标准捕获的输出行数: {len(standard_output)}")
            
            # cmd_run返回None不代表失败，强制设置成功状态
            exit_status = 0
            
            return {
                "status": "success",
                "output": cmd_output,  # 实际命令输出或提示信息
                "aider_output": aider_output,  # aider的提示信息作为辅助参考
                "standard_output": standard_output,  # 标准捕获的输出
                "exit_status": exit_status,
                "result": result
            }
            
        finally:
            # 确保恢复原始工作目录
            os.chdir(original_dir)
            logger.info(f"已恢复cmd_run运行命令后的原始工作目录: {original_dir}")
            
    except Exception as e:
        logger.error(f"使用cmd_run运行命令失败: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }


class CommitRequest(BaseModel):
    message: Optional[str] = None
    session_id: str = "default"


@app.post("/commit")
async def commit_changes(request: CommitRequest):
    """提交更改（等同于/commit聊天命令）"""
    try:
        # 获取coder实例
        coder = get_coder(request.session_id)
        
        # 保存当前工作目录
        original_dir = os.getcwd()
        logger.info(f"保存提交更改前的原始工作目录: {original_dir}")
        
        try:
            # 如果coder有指定的工作目录，则切换到该目录
            if hasattr(coder, 'cwd') and coder.cwd:
                os.chdir(coder.cwd)
                logger.info(f"已切换到会话工作目录: {coder.cwd}")
                
            # 清空之前捕获的输出
            if hasattr(coder.commands.io, 'get_captured_lines'):
                coder.commands.io.get_captured_lines()
            
            # 执行commit命令
            result = coder.commands.cmd_commit(request.message)
            
            # 获取捕获的输出
            output = []
            if hasattr(coder.commands.io, 'get_captured_lines'):
                output = coder.commands.io.get_captured_lines()
            
            # 检查是否有提交哈希值
            commit_info = {}
            
            # 如果coder.last_aider_commit_hash为空，尝试通过git直接获取最近的提交哈希
            if not coder.last_aider_commit_hash and coder.repo:
                try:
                    # 使用git命令获取最近提交的哈希
                    import subprocess
                    git_cmd = ["git", "rev-parse", "HEAD"]
                    process = subprocess.Popen(
                        git_cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        cwd=coder.cwd
                    )
                    stdout, stderr = process.communicate()
                    
                    if process.returncode == 0:
                        commit_hash = stdout.strip()
                        logger.info(f"获取到最近提交哈希: {commit_hash}")
                        
                        # 获取提交消息
                        git_msg_cmd = ["git", "log", "-1", "--pretty=%B"]
                        msg_process = subprocess.Popen(
                            git_msg_cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            cwd=coder.cwd
                        )
                        msg_stdout, msg_stderr = msg_process.communicate()
                        
                        if msg_process.returncode == 0:
                            commit_message = msg_stdout.strip()
                            logger.info(f"获取到最近提交消息: {commit_message}")
                            
                            # 设置到coder实例中
                            coder.last_aider_commit_hash = commit_hash
                            coder.last_aider_commit_message = commit_message
                except Exception as e:
                    logger.error(f"获取git提交信息失败: {str(e)}")
            
            if coder.last_aider_commit_hash:
                commit_info = {
                    "commit_hash": coder.last_aider_commit_hash,
                    "commit_message": coder.last_aider_commit_message
                }
                logger.info(f"提交信息设置成功: {commit_info}")
            else:
                logger.warning("未能获取到提交哈希值")
            
            return {
                "status": "success",
                "output": output,
                "result": result,
                "commit_info": commit_info
            }
            
        finally:
            # 确保恢复原始工作目录
            os.chdir(original_dir)
            logger.info(f"已恢复提交更改后的原始工作目录: {original_dir}")
            
    except Exception as e:
        logger.error(f"提交更改失败: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }


@app.post("/web_content", response_model=WebContentResponse)
async def get_web_content(request: WebContentRequest):
    """获取网页内容"""
    try:
        scraper = Scraper(print_error=lambda x: x)
        content = scraper.scrape(request.url)
        
        if content and content.strip():
            return {"content": f"{request.url}\n\n{content}"}
        else:
            return {"error": f"无法获取 {request.url} 的内容"}
    except Exception as e:
        return {"error": str(e)}


# @app.post("/set_workspace_dir")
# async def set_workspace_dir(request: WorkspaceDirRequest):
#     """设置Aider工作目录"""
#     try:
#         logger.info(f"设置工作目录 - session_id: {request.session_id}, dir: {request.workspace_dir}")
        
#         # 检查目录是否存在
#         if not os.path.exists(request.workspace_dir):
#             logger.warning(f"目录不存在: {request.workspace_dir}")
#             return {
#                 "status": "error",
#                 "error": f"目录 {request.workspace_dir} 不存在"
#             }
        
#         # 检查目录权限
#         if not os.access(request.workspace_dir, os.R_OK | os.W_OK):
#             logger.warning(f"目录权限不足: {request.workspace_dir}")
#             return {
#                 "status": "error",
#                 "error": f"目录 {request.workspace_dir} 权限不足"
#             }
        
#         # 如果会话已存在，删除旧的Coder实例
#         if request.session_id in coder_instances:
#             logger.info(f"删除旧的Coder实例: {request.session_id}")
#             del coder_instances[request.session_id]
        
#         # 创建新的Coder实例，传入工作目录
#         coder = get_coder(request.session_id, request.workspace_dir)
#         logger.info(f"已创建新的Coder实例: {request.session_id}")
        
#         return {
#             "status": "success",
#             "message": f"已设置工作目录为 {request.workspace_dir}",
#             "workspace_dir": request.workspace_dir
#         }
#     except Exception as e:
#         logger.error(f"设置工作目录失败: {str(e)}")
#         return {
#             "status": "error",
#             "error": str(e)
#         }


# # 恢复会话历史记录接口
# @app.post("/chat/history/restore")
# async def restore_chat_history(request: ChatHistoryRequest):
#     """恢复对话历史到Aider会话"""
#     try:
#         # 删除现有会话实例（如果存在）
#         if request.session_id in coder_instances:
#             logger.info(f"删除现有会话实例以恢复历史: {request.session_id}")
#             del coder_instances[request.session_id]
        
#         # 获取或创建Coder实例，并传入历史记录
#         coder = get_coder(request.session_id, history=request.history)
        
#         return {
#             "status": "success",
#             "message": f"已恢复对话历史，共 {len(request.history)} 条消息",
#             "session_id": request.session_id
#         }
#     except Exception as e:
#         logger.error(f"恢复对话历史失败: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))


# # 添加自动生成标题的API
# @app.post("/chat/topics/generate_title")
# async def generate_topic_title(request: ChatRequest):
#     """使用LLM自动生成对话主题标题"""
#     try:
#         # 获取Coder实例
#         coder = get_coder(request.session_id)
        
#         # 构造请求生成标题的提示
#         title_prompt = f"基于以下消息生成一个简短、具体的聊天主题标题（不超过20个字符）：\n\n{request.message}\n\n只需回复标题，不需要其他解释。"
        
#         # 使用Coder实例运行请求
#         title = coder.run(title_prompt).strip()
        
#         # 如果生成的标题太长，进行截断
#         if len(title) > 20:
#             title = title[:20] + "..."
            
#         return {"title": title}
#     except Exception as e:
#         logger.error(f"生成主题标题失败: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))


# 一体化会话初始化API
@app.post("/init_session")
async def init_session(request: SessionInitRequest):
    """初始化Aider会话：设置工作目录和历史记录"""
    try:
        logger.info(f"初始化会话 - session_id: {request.session_id}, dir: {request.workspace_dir}, "
                  f"历史记录数: {len(request.history)}")
        
        # 检查目录是否存在
        if not os.path.exists(request.workspace_dir):
            logger.warning(f"目录不存在: {request.workspace_dir}")
            return {
                "status": "error",
                "error": f"目录 {request.workspace_dir} 不存在"
            }
        
        # 检查目录权限
        if not os.access(request.workspace_dir, os.R_OK | os.W_OK):
            logger.warning(f"目录权限不足: {request.workspace_dir}")
            return {
                "status": "error",
                "error": f"目录 {request.workspace_dir} 权限不足"
            }
        
        # 保存当前工作目录
        original_dir = os.getcwd()
        logger.info(f"保存会话初始化前的原始工作目录: {original_dir}")
        
        try:
            # 如果会话已存在，删除旧的Coder实例
            if request.session_id in coder_instances:
                logger.info(f"删除旧的Coder实例: {request.session_id}")
                del coder_instances[request.session_id]
            
            # 创建新的Coder实例，一次性设置工作目录和历史记录
            # get_coder函数会确保在正确的目录下创建实例
            coder = get_coder(request.session_id, request.workspace_dir, request.history)
            logger.info(f"已创建并初始化Coder实例: {request.session_id}")
        
            return {
                "status": "success",
                "message": f"会话已初始化，工作目录: {request.workspace_dir}, 历史记录: {len(request.history)} 条",
                "session_id": request.session_id
            }
        finally:
            # 确保恢复原始工作目录
            os.chdir(original_dir)
            logger.info(f"已恢复会话初始化后的原始工作目录: {original_dir}")
            
    except Exception as e:
        logger.error(f"初始化会话失败: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }


def main(port=8000, config_file=None, model_metadata_file=None, model_settings_file=None):
    """启动FastAPI服务器"""
    # 检查依赖项
    try:
        import importlib
        for pkg in ["fastapi"]:
            try:
                importlib.import_module(pkg)
            except ImportError:
                logger.info(f"正在安装缺失的依赖: {pkg}")
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi"])
    except Exception as e:
        logger.error(f"依赖项检查失败: {e}")
    
    # 设置环境变量，用于配置 Coder 实例
    if config_file:
        os.environ["AIDER_CONFIG_FILE"] = config_file
        logger.info(f"设置配置文件: {config_file}")
    
    if model_metadata_file:
        os.environ["AIDER_MODEL_METADATA_FILE"] = model_metadata_file
        logger.info(f"设置模型元数据文件: {model_metadata_file}")
    
    if model_settings_file:
        os.environ["AIDER_MODEL_SETTINGS_FILE"] = model_settings_file
        logger.info(f"设置模型设置文件: {model_settings_file}")
    
    logger.info(f"启动Aider API服务...")
    logger.info(f"API地址: http://localhost:{port}")
    logger.info(f"API文档: http://localhost:{port}/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    import argparse
    
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="启动Aider API服务")
    parser.add_argument("--port", type=int, default=8000, help="指定服务器端口号")
    parser.add_argument("--config", type=str, help="Aider配置文件路径")
    parser.add_argument("--model-metadata-file", type=str, help="模型元数据文件路径")
    parser.add_argument("--model-settings-file", type=str, help="模型设置文件路径")
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 使用指定的端口和配置启动服务器
    main(
        port=args.port, 
        config_file=args.config,
        model_metadata_file=args.model_metadata_file,
        model_settings_file=args.model_settings_file
    ) 
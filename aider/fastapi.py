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
    if session_id not in coder_instances:
        current_dir = workspace_dir or os.getcwd()
        logger.info(f"创建新的Coder实例，工作目录: {current_dir}")
        
        try:
            # 切换到工作目录
            os.chdir(current_dir)
            logger.info(f"已切换到工作目录: {current_dir}")
            
            # 设置命令行参数，从环境变量读取配置
            cli_args = ["--yes-always"]  # 基本参数
            
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
    
    return coder_instances[session_id]


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """向LLM发送消息并获取回复（非流式）"""
    try:
        coder = get_coder(request.session_id)
        
        # 记录输入历史
        coder.io.add_to_input_history(request.message)
        
        # 运行对话
        response = coder.run(request.message)
        
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
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """向LLM发送消息并获取流式回复"""
    try:
        coder = get_coder(request.session_id)
        
        # 记录输入历史
        coder.io.add_to_input_history(request.message)
        
        # 创建一个生成器来产生流式响应
        async def response_generator():
            # 运行聊天并获取流式响应
            buffer = ""
            for chunk in coder.run_stream(request.message):
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
                
                # 读取修改后的文件内容
                updated_files = []
                for filename in edit_info["files"]:
                    try:
                        logger.debug(f"读取文件: {filename}")  # 添加日志
                        with open(filename, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # 确定文件类型
                        ext = filename.split('.')[-1].lower()
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
                        logger.debug(f"成功读取文件: {filename}, 类型: {file_type}")  # 添加日志
                    except Exception as e:
                        logger.error(f"读取文件失败 {filename}: {str(e)}")
                
                # 将文件内容添加到编辑信息中
                edit_info["updated_files"] = updated_files
                logger.debug(f"最终编辑信息: {json.dumps(edit_info, indent=2)}")  # 添加日志
            
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
    
    except Exception as e:
        logger.error(f"发生错误: {str(e)}")  # 添加错误日志
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/files", response_model=FilesResponse)
async def get_files(session_id: str = "default"):
    """获取当前聊天中的文件"""
    try:
        logger.info(f"获取文件列表 - session_id: {session_id}")
        coder = get_coder(session_id)
        files = coder.get_inchat_relative_files()
        logger.info(f"获取到的文件列表: {files}")
        return {"files": files}
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
        coder = get_coder(request.session_id)
        coder.add_rel_fname(request.filename)
        return {"status": "success", "message": f"已将 {request.filename} 添加到聊天中"}
    except Exception as e:
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
            return {
                "status": "error",
                "error": "没有找到上次的提交"
            }
        
        # 撤销提交
        result = coder.repo.undo_last_commit()
        
        if result:
            return {
                "status": "success",
                "message": "已撤销最后一次提交"
            }
        else:
            return {
                "status": "error",
                "error": "撤销提交失败"
            }
    except Exception as e:
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


@app.post("/set_workspace_dir")
async def set_workspace_dir(request: WorkspaceDirRequest):
    """设置Aider工作目录"""
    try:
        logger.info(f"设置工作目录 - session_id: {request.session_id}, dir: {request.workspace_dir}")
        
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
        
        # 如果会话已存在，删除旧的Coder实例
        if request.session_id in coder_instances:
            logger.info(f"删除旧的Coder实例: {request.session_id}")
            del coder_instances[request.session_id]
        
        # 创建新的Coder实例，传入工作目录
        coder = get_coder(request.session_id, request.workspace_dir)
        logger.info(f"已创建新的Coder实例: {request.session_id}")
        
        return {
            "status": "success",
            "message": f"已设置工作目录为 {request.workspace_dir}",
            "workspace_dir": request.workspace_dir
        }
    except Exception as e:
        logger.error(f"设置工作目录失败: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }


# 恢复会话历史记录接口
@app.post("/chat/history/restore")
async def restore_chat_history(request: ChatHistoryRequest):
    """恢复对话历史到Aider会话"""
    try:
        # 删除现有会话实例（如果存在）
        if request.session_id in coder_instances:
            logger.info(f"删除现有会话实例以恢复历史: {request.session_id}")
            del coder_instances[request.session_id]
        
        # 获取或创建Coder实例，并传入历史记录
        coder = get_coder(request.session_id, history=request.history)
        
        return {
            "status": "success",
            "message": f"已恢复对话历史，共 {len(request.history)} 条消息",
            "session_id": request.session_id
        }
    except Exception as e:
        logger.error(f"恢复对话历史失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# 添加自动生成标题的API
@app.post("/chat/topics/generate_title")
async def generate_topic_title(request: ChatRequest):
    """使用LLM自动生成对话主题标题"""
    try:
        # 获取Coder实例
        coder = get_coder(request.session_id)
        
        # 构造请求生成标题的提示
        title_prompt = f"基于以下消息生成一个简短、具体的聊天主题标题（不超过20个字符）：\n\n{request.message}\n\n只需回复标题，不需要其他解释。"
        
        # 使用Coder实例运行请求
        title = coder.run(title_prompt).strip()
        
        # 如果生成的标题太长，进行截断
        if len(title) > 20:
            title = title[:20] + "..."
            
        return {"title": title}
    except Exception as e:
        logger.error(f"生成主题标题失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


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
        
        # 如果会话已存在，删除旧的Coder实例
        if request.session_id in coder_instances:
            logger.info(f"删除旧的Coder实例: {request.session_id}")
            del coder_instances[request.session_id]
        
        # 创建新的Coder实例，一次性设置工作目录和历史记录
        coder = get_coder(request.session_id, request.workspace_dir, request.history)
        logger.info(f"已创建并初始化Coder实例: {request.session_id}")
        
        return {
            "status": "success",
            "message": f"会话已初始化，工作目录: {request.workspace_dir}, 历史记录: {len(request.history)} 条",
            "session_id": request.session_id
        }
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
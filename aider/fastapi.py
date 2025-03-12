#!/usr/bin/env python

import os
import sys
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from aider import urls
from aider.coders import Coder
from aider.main import main as cli_main
from aider.io import InputOutput
from aider.scrape import Scraper


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


class ChatResponse(BaseModel):
    response: str
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


app = FastAPI(title="Aider API", description="与Aider对话并编辑代码的API")

# 添加CORS中间件以允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_coder(session_id: str = "default"):
    """获取或创建一个Coder实例"""
    if session_id not in coder_instances:
        coder = cli_main(return_coder=True)
        if not isinstance(coder, Coder):
            raise ValueError(f"无法创建Coder实例: {coder}")
        
        # 配置IO捕获
        io = CaptureIO(
            pretty=False,
            yes=True,
            dry_run=coder.io.dry_run,
            encoding=coder.io.encoding,
        )
        coder.commands.io = io
        
        # 配置流式输出
        coder.yield_stream = True
        coder.stream = True
        coder.pretty = False
        
        coder_instances[session_id] = coder
    
    return coder_instances[session_id]


@app.get("/")
async def root():
    """API根路径，返回基本信息"""
    return {
        "name": "Aider API",
        "description": "通过API与Aider交互",
        "documentation": urls.website,
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """向LLM发送消息并获取回复"""
    try:
        coder = get_coder(request.session_id)
        
        # 记录输入历史
        coder.io.add_to_input_history(request.message)
        
        # 运行对话
        response = coder.run(request.message)
        
        # 构建响应
        result = {
            "response": response,
            "edits": None
        }
        
        # 如果有编辑，添加到响应中
        if coder.aider_edited_files:
            edit_info = {
                "files": coder.aider_edited_files,
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
            
            result["edits"] = edit_info
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/files", response_model=FilesResponse)
async def get_files(session_id: str = "default"):
    """获取当前聊天中的文件"""
    try:
        coder = get_coder(session_id)
        return {"files": coder.get_inchat_relative_files()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/all_files", response_model=FilesResponse)
async def get_all_files(session_id: str = "default"):
    """获取所有可添加到聊天的文件"""
    try:
        coder = get_coder(session_id)
        return {"files": coder.get_all_relative_files()}
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
            return {"status": "error", "message": "没有可撤销的提交"}
        
        coder.commands.io.get_captured_lines()
        reply = coder.commands.cmd_undo(None)
        lines = coder.commands.io.get_captured_lines()
        
        return {
            "status": "success", 
            "message": "\n".join(lines),
            "reply": reply
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


def main(port=8000):
    """启动FastAPI服务器"""
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    import argparse
    
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="启动Aider API服务")
    parser.add_argument("--port", type=int, default=8000, help="指定服务器端口号")
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 使用指定的端口启动服务器
    main(port=args.port) 
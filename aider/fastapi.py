#!/usr/bin/env python

import os
import sys
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import glob

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

# 获取项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 挂载静态文件目录
app.mount("/templates", StaticFiles(directory=os.path.join(ROOT_DIR, "templates")), name="templates")
app.mount("/static", StaticFiles(directory=os.path.join(ROOT_DIR, "static")), name="static")

# 首页
@app.get("/", response_class=HTMLResponse)
async def read_root():
    index_path = os.path.join(ROOT_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>多八多AI应用编辑器</h1><p>请创建index.html文件</p>"


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


# 模板响应模型
class TemplateResponse(BaseModel):
    name: str
    content: str

# 模板列表响应模型
class TemplatesListResponse(BaseModel):
    templates: List[str]

# 获取模板列表
@app.get("/templates", response_model=TemplatesListResponse)
async def get_templates():
    templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
    if not os.path.exists(templates_dir):
        return {"templates": []}
    
    # 获取HTML和JS模板文件
    html_templates = glob.glob(os.path.join(templates_dir, "*.html"))
    js_templates = glob.glob(os.path.join(templates_dir, "*.js"))
    
    # 提取模板名称（不包括扩展名）
    template_names = []
    for template in html_templates + js_templates:
        name = os.path.basename(template).split('.')[0]
        if name not in template_names:
            template_names.append(name)
    
    return {"templates": template_names}

# 获取特定模板内容
@app.get("/templates/{name}", response_model=Optional[TemplateResponse])
async def get_template(name: str):
    templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
    
    # 首先尝试查找HTML模板
    html_path = os.path.join(templates_dir, f"{name}.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"name": name, "content": content}
    
    # 如果HTML模板不存在，尝试查找JS模板
    js_path = os.path.join(templates_dir, f"{name}.js")
    if os.path.exists(js_path):
        # 对于JS模板，直接返回文件而不是JSON响应
        return FileResponse(js_path, media_type="application/javascript")
    
    # 如果模板不存在，返回404错误
    raise HTTPException(status_code=404, detail=f"Template '{name}' not found")


def main(port=8000):
    """启动FastAPI服务器"""
    # 检查依赖项
    try:
        import importlib
        for pkg in ["fastapi.staticfiles", "fastapi.responses"]:
            try:
                importlib.import_module(pkg)
            except ImportError:
                print(f"正在安装缺失的依赖: {pkg}")
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi"])
    except Exception as e:
        print(f"依赖项检查失败: {e}")
        
    # 添加静态文件服务
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import RedirectResponse
    
    # 获取当前目录路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(os.path.dirname(current_dir), "static")
    
    # 确保静态目录存在
    os.makedirs(static_dir, exist_ok=True)

    # 将index.html复制到静态目录（如果存在）
    editor_html_path = os.path.join(static_dir, "index.html")
    index_html_path = os.path.join(os.path.dirname(current_dir), "index.html")
    
    if os.path.exists(index_html_path):
        print(f"使用项目根目录中的index.html")
        with open(index_html_path, "r", encoding="utf-8") as src:
            with open(editor_html_path, "w", encoding="utf-8") as dest:
                dest.write(src.read())
    else:
        print(f"未找到index.html文件，将使用默认模板")
        # 如果找不到index.html，使用默认模板
        if not os.path.exists(editor_html_path):
            with open(editor_html_path, "w", encoding="utf-8") as f:
                f.write(get_editor_html())
    
    # 挂载静态文件目录
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    # 添加根路径重定向
    @app.get("/", include_in_schema=False)
    async def root_redirect():
        return RedirectResponse(url="/static/index.html")
    
    print(f"启动Aider AI编辑器服务...")
    print(f"请访问: http://localhost:{port}/ 或 https://23947.dev.d8dcloud.com/")
    print(f"API文档: http://localhost:{port}/docs")
    
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
# Aider API

这是Aider的API版本，允许通过HTTP请求与Aider交互，而不是通过命令行或图形界面。

## 安装

确保已安装Aider及其依赖项，然后安装额外的API依赖：

```bash
pip install fastapi uvicorn
```

## 启动API服务器

```bash
python -m aider.fastapi
```

服务器将在 `http://localhost:8000` 启动。

## API端点

### 基本信息

- **GET /** - 获取API基本信息

### 聊天

- **POST /chat** - 向LLM发送消息并获取回复
  ```json
  {
    "message": "帮我优化这段代码",
    "session_id": "default"
  }
  ```

### 文件管理

- **GET /files** - 获取当前聊天中的文件
  - 查询参数: `session_id` (可选，默认为 "default")

- **GET /all_files** - 获取所有可添加到聊天的文件
  - 查询参数: `session_id` (可选，默认为 "default")

- **POST /add_file** - 添加文件到聊天中
  ```json
  {
    "filename": "main.py",
    "session_id": "default"
  }
  ```

- **POST /remove_file** - 从聊天中移除文件
  ```json
  {
    "filename": "main.py",
    "session_id": "default"
  }
  ```

### 聊天历史

- **POST /clear_history** - 清除聊天历史
  - 查询参数: `session_id` (可选，默认为 "default")

### Git操作

- **POST /undo** - 撤销最后一次提交
  - 查询参数: `session_id` (可选，默认为 "default")

### 网页内容

- **POST /web_content** - 获取网页内容
  ```json
  {
    "url": "https://example.com",
    "session_id": "default"
  }
  ```

## 会话管理

所有API端点都支持 `session_id` 参数，允许你管理多个独立的Aider会话。如果不指定 `session_id`，将使用 "default" 会话。

## 示例使用

### 使用curl发送聊天消息

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "创建一个简单的Python计算器", "session_id": "my_project"}'
```

### 使用Python请求API

```python
import requests

# 添加文件到聊天
requests.post(
    "http://localhost:8000/add_file",
    json={"filename": "calculator.py", "session_id": "my_project"}
)

# 发送聊天消息
response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "请添加除法功能", "session_id": "my_project"}
)

print(response.json())
```

## 前端集成

你可以创建自定义前端应用，通过这些API与Aider交互。API支持CORS，允许从任何源发送请求（在生产环境中应限制为特定域名）。

## 注意事项

- API服务器默认绑定到 `0.0.0.0`，这意味着它在所有网络接口上可用。在生产环境中，你可能需要配置防火墙或使用反向代理增加安全性。
- 当前实现使用内存中缓存保存会话，服务器重启后会话将丢失。生产环境中可能需要持久化存储。 
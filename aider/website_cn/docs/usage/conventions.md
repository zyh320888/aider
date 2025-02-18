---
parent: 使用指南
nav_order: 800
description: 让 aider 在处理代码时遵循您的编码规范。
---
# 指定编码规范

有时您希望 GPT 能遵循特定的编码规范，例如是否提供类型提示、优先使用哪些库或包等。

在 aider 中实现这一点的最简单方法是创建一个小的 Markdown 文件并将其包含在聊天中。

例如，假设我们希望 Python 代码：

```
- 优先使用 httpx 而不是 requests 进行 HTTP 请求
- 尽可能使用类型提示
```

我们只需创建一个包含这些规范的 `CONVENTIONS.md` 文件，然后将其与要编辑的文件一起添加到 aider 聊天中。

建议使用 `/read CONVENTIONS.md` 或 `aider --read CONVENTION.md` 加载规范文件。这种方式会将其标记为只读文件，并在启用提示缓存时进行缓存。

## 社区贡献的规范

您可以查看 [aider 规范仓库](https://github.com/Aider-AI/conventions) 查找或贡献规范文件。

## 自动加载规范

您可以在 [`.aider.conf.yml` 配置文件](https://aider.chat/docs/config/aider_conf.html) 中配置 aider 始终加载规范文件：

```yaml
# 单个文件
read: CONVENTIONS.md

# 多个文件
read: [CONVENTIONS.md, anotherfile.txt]
```

## 示例

以下示例展示了规范文件如何影响 aider 生成的代码。

<div class="chat-transcript" markdown="1">
> $ aider --read CONVENTIONS.md useragent.py  
>  
> Aider v0.24.2-dev  
> 已将 CONVENTIONS.md 添加到聊天  
> 已将 useragent.py 添加到聊天  

#### 编写一个使用 httpbin 检查请求中用户代理的函数，返回 ua

为满足您的要求，我将：

1. 添加 httpx 的导入
2. 编写名为 check_user_agent 的函数，向 httpbin.org/user-agent 发送 GET 请求并返回用户代理字符串

以下是 useragent.py 文件的差异：

```diff
--- useragent.py
+++ useragent.py
@@ ... @@
+import httpx
+
+def check_user_agent() -> str:
+    response = httpx.get('https://httpbin.org/user-agent')
+    return response.json()['user-agent']
```

该函数使用 httpx 向 httpbin.org/user-agent 发送 GET 请求，该端点会返回 HTTP 客户端的用户代理信息。函数从 JSON 响应中提取用户代理字符串并返回。

> 已应用对 useragent.py 的编辑  
</div>

GPT 正确使用了 httpx 并提供了类型提示。以下是未使用 CONVENTIONS.md 时相同任务的执行结果（此时 GPT 使用了 requests 且未添加类型提示）：

<div class="chat-transcript" markdown="1">
> $ aider useragent.py  
>  
> Aider v0.24.2-dev  
> 已将 useragent.py 添加到聊天  


#### 编写一个使用 httpbin 检查请求中用户代理的函数，返回 ua  

```diff
--- /dev/null
+++ useragent.py
@@ ... @@
+import requests
+
+def check_user_agent():
+    response = requests.get('https://httpbin.org/user-agent')
+    user_agent = response.json().get('user-agent')
+    return user_agent
```

> 已应用对 useragent.py 的编辑  
</div>



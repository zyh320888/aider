---
parent: 使用指南
nav_order: 700
description: 在aider编码聊天中添加图片和网页。
---

# 图片和网页

您可以在aider聊天中添加图片和URL链接。

## 图片

Aider支持许多具有视觉能力的模型处理图像文件，
比如GPT-4o和Claude 3.7 Sonnet。
在多种情况下，向聊天添加图片可能会很有帮助：

- 添加您想要aider构建或修改的网页或UI的截图。
- 向aider展示您想要构建的UI模型。
- 截取难以复制粘贴为文本的错误信息。
- 等等。

您可以像添加任何其他文件一样向聊天添加图片：

- 在聊天中使用`/add <图片文件名>`
- 使用`/paste`将剪贴板中的图片粘贴到聊天中。
- 在命令行中使用图片文件名启动aider：`aider <图片文件名>`，以及您需要的任何其他命令行参数。

## 网页

Aider可以从URL中抓取文本并将其添加到聊天中。
这在以下情况下可能会有所帮助：

- 包含不太流行的API的文档页面。
- 包含比模型训练截止日期更新的库或包的最新文档。
- 等等。

要向聊天添加URL：

- 使用`/web <url>`
- 只需将URL粘贴到聊天中，aider会询问您是否要添加它。

您还可以从命令行抓取网页，以查看aider生成的markdown版本：

```
python -m aider.scrape https://aider.chat/docs/usage/tips.html
```

---
parent: 故障排除
excerpt: 使用 "/help <问题>" 寻求有关使用 aider、自定义设置、故障排除、使用 LLM 等方面的帮助。
nav_order: 30
---

# 使用 /help 命令

输入 `/help <问题>`，
aider 将回复有用的信息。
您可以询问有关使用 aider、
自定义设置、故障排除、使用 LLM 等方面的问题。

在后台，aider 已为其所有
[文档](https://aider.chat/)
建立了索引。
它使用您的问题查找相关文档
并与 LLM 共享，实现
检索增强生成（RAG）。
LLM 还能理解您当前 aider 对话的完整上下文，
因此能针对您可能面临的具体问题提供帮助。


<div class="chat-transcript" markdown="1">

> Aider v0.42.1-dev  
> Models: claude-3-5-sonnet with diff edit format  
> Repo-map: using 1024 tokens  
> Use /help \<question\> to ask for help, run with --help to see cmd line args  

#### /help 环境变量文件 .env 是全局的还是针对特定 git 仓库的？

根据提供的文档，以下是关于 aider 中 .env 文件的答案：

.env 文件在 aider 中既可以是全局的，也可以是特定于 git 仓库的。Aider 按照以下优先顺序查找 .env 文件：

1. 您的主目录（全局）
2. 您的 git 仓库根目录（仓库特定）
3. 当前目录
4. 使用 `--env-file <filename>` 参数指定的文件

如果在这些位置存在多个 .env 文件，它们将按照上述顺序加载，后加载的文件优先级更高。这意味着您可以在主目录中设置一个包含通用设置的全局 .env 文件，然后使用 git 仓库根目录中的仓库特定 .env 文件覆盖或添加这些设置。

以下是您可能会觉得有用的一些相关文档链接：

- https://aider.chat/docs/config.html
- https://aider.chat/docs/config/dotenv.html

同时支持全局和仓库特定的 .env 文件使配置更加灵活，您可以全局设置默认值，并根据需要在特定项目基础上覆盖它们。

</div>
<div class="chat-transcript" markdown="1">

#### /help 我可以使用本地 LLM 吗？

是的，您可以在 Aider 中使用本地 LLM。以下是可用选项的概述：

1. Ollama：Aider 支持通过 Ollama 使用本地模型。

2. OpenAI 兼容 API：Aider 可以访问提供 OpenAI 兼容 API 的本地模型。

3. 其他本地模型：Aider 使用 LiteLLM 包连接到各种 LLM 提供商，其中可能包括运行本地模型的选项。

然而，请注意 Aider 在与更强大的模型配合时效果最佳。能力较弱的模型可能难以正确返回"代码编辑"，这可能导致 Aider 无法编辑您的文件并提交更改。

关于使用本地 LLM 和连接到各种模型的更详细信息，您可能想查看以下相关文档页面：

- https://aider.chat/docs/llms.html
- https://aider.chat/docs/llms/ollama.html
- https://aider.chat/docs/llms/openai-compat.html

请记住，本地 LLM 的性能和功能可能会因特定模型和您的硬件资源而异。

</div>


## 获取更多帮助

{% include help.md %}

---
parent: 故障排除
nav_order: 25
---

# Token 限制

每个 LLM 在处理请求时都有 token 数量限制：

- 模型的**上下文窗口**限制了它能处理的*输入和输出* token 总数。
- 每个模型对它能产生的**输出 token** 数量也有限制。

当模型响应表明它已超出 token 限制时，
aider 会报告错误。
错误信息中会包含避免碰到 token 限制的建议操作。

以下是一个错误示例： 

```
Model gpt-3.5-turbo has hit a token limit!

Input tokens: 768 of 16385
Output tokens: 4096 of 4096 -- exceeded output limit!
Total tokens: 4864 of 16385

To reduce output tokens:
- Ask for smaller changes in each request.
- Break your code into smaller source files.
- Try using a stronger model like DeepSeek V3 or Sonnet that can return diffs.

For more info: https://aider.chat/docs/token-limits.html
```

{: .note }
Aider 从不*强制执行* token 限制，它只*报告*来自 API 提供商的 token 限制错误。
Aider 报告的 token 计数是*估计值*。

## 输入 token 和上下文窗口大小

最常见的问题是尝试向模型发送过多数据，
超出了其上下文窗口。
从技术上讲，如果输入太大或输入加输出太大，都会耗尽上下文窗口。

像 GPT-4o 和 Sonnet 这样的强大模型拥有相当大的上下文窗口，
所以这类错误通常只在使用较弱模型时才会出现。

最简单的解决方案是尝试通过从对话中移除文件来减少输入 token。
最好只添加 aider 需要*编辑*的文件来完成您的请求。

- 使用 `/tokens` 查看 token 使用情况。
- 使用 `/drop` 从对话会话中移除不需要的文件。
- 使用 `/clear` 清除对话历史。
- 将代码拆分为更小的源文件。

## 输出 token 限制

大多数模型的输出限制相当小，通常仅为 4k token。
如果您要求 aider 进行影响大量代码的大规模更改，
LLM 可能会在尝试返回所有更改时碰到输出 token 限制。

为避免碰到输出 token 限制：

- 在每个请求中要求较小的更改。
- 将代码拆分为更小的源文件。
- 使用能够返回差异的强大模型，如 gpt-4o、sonnet 或 DeepSeek V3。
- 使用支持[无限输出](/docs/more/infinite-output.html)的模型。

## 其他原因

有时 token 限制错误是由
不合规的 API 代理服务器
或您用于托管本地模型的 API 服务器中的 bug 导致的。
当直接连接到主要的
[LLM 提供商云 API](https://aider.chat/docs/llms.html) 时，
aider 已经过充分测试。
对于托管本地模型，
[Ollama](https://aider.chat/docs/llms/ollama.html) 与 aider 配合良好。

尝试在不使用 API 代理服务器的情况下使用 aider，
或直接使用推荐的云 API 之一，
看看您的 token 限制问题是否解决。

## 更多帮助

{% include help.md %}

---
parent: 故障排除
nav_order: 28
---

# 模型和 API 密钥

您需要告诉 aider 使用哪种 LLM 并提供一个 API 密钥。
最简单的方法是使用 `--model` 和 `--api-key`
命令行参数，如下所示：

```
# 通过 DeepSeek 的 API 使用 DeepSeek
aider --model deepseek --api-key deepseek=your-key-goes-here

# 通过 Anthropic 的 API 使用 Claude 3.7 Sonnet
aider --model sonnet --api-key anthropic=your-key-goes-here

# 通过 OpenAI 的 API 使用 o3-mini
aider --model o3-mini --api-key openai=your-key-goes-here

# 通过 OpenRouter 的 API 使用 Sonnet
aider --model openrouter/anthropic/claude-3.7-sonnet --api-key openrouter=your-key-goes-here

# 通过 OpenRouter 的 API 使用 DeepSeek Chat V3
aider --model openrouter/deepseek/deepseek-chat --api-key openrouter=your-key-goes-here
```

更多信息，请参阅文档部分：

- [连接 LLM](https://aider.chat/docs/llms.html)
- [配置 API 密钥](https://aider.chat/docs/config/api-keys.html)

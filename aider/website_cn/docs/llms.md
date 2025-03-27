---
title: 连接到大语言模型
nav_order: 40
has_children: true
description: Aider可以连接到大多数大语言模型进行AI结对编程。
---

# Aider能连接到大多数大语言模型
{: .no_toc }

[![连接到多种大语言模型](/assets/llms.jpg)](https://aider.chat/assets/llms.jpg)


## 最佳模型
{: .no_toc }

Aider与以下擅长编辑代码的模型配合效果最佳：

- [DeepSeek R1和V3](/docs/llms/deepseek.html)
- [Claude 3.5 Sonnet](/docs/llms/anthropic.html)
- [OpenAI o1, o3-mini和GPT-4o](/docs/llms/openai.html)


## 免费模型
{: .no_toc }

Aider可以使用多种**免费**API提供商：

- 谷歌的[Gemini 1.5 Pro](/docs/llms/gemini.html)与Aider兼容，代码编辑能力与GPT-3.5相当。
- 您可以使用[Groq上的Llama 3 70B](/docs/llms/groq.html)，其代码编辑性能与GPT-3.5相当。
- Cohere也提供其[Command-R+模型](/docs/llms/cohere.html)的免费API访问，可作为Aider的*基础*编码助手。

## 本地模型
{: .no_toc }

Aider也可以与本地模型配合使用，例如通过[Ollama](/docs/llms/ollama.html)。
它还可以访问提供[OpenAI兼容API](/docs/llms/openai-compat.html)的本地模型。

## 使用功能强大的模型
{: .no_toc }

查看[Aider的LLM排行榜](https://aider.chat/docs/leaderboards/)，了解哪些模型与Aider配合效果最佳。

请注意，Aider可能无法与能力较弱的模型良好配合。
如果您看到模型返回代码，但Aider无法编辑您的文件并提交更改...
这通常是因为该模型无法正确返回"代码编辑"。
弱于GPT-3.5的模型可能难以与Aider良好配合。


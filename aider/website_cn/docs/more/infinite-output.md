--- 
parent: 更多信息
nav_order: 480
description: Aider可以通过支持预填充的模型实现"无限输出"。
---

# 无限输出

LLM服务提供商通常会限制单个请求的输出量，这通常称为输出令牌限制。

对于支持"预填充"助手响应的模型，Aider能够突破这一限制。当您使用支持预填充的模型时，启动时会显示"infinite output"的提示：

```
Aider v0.58.0
主模型: claude-3-5-sonnet-20240620 支持差异编辑格式、提示缓存和无限输出
```

支持预填充的模型可以被设定为从特定文本开始响应。当Aider从模型收集代码编辑遇到输出令牌限制时，它会用部分响应预填充发起新的LLM请求，提示模型从断点处继续生成内容。这种预填充机制可以重复进行，从而实现超长输出。跨越这些输出限制边界的文本拼接需要一些启发式方法，但通常相当可靠。

目前支持"无限输出"的预填充模型包括：

<!--[[[cog
import requests
import json

# 获取JSON数据
url = "https://raw.githubusercontent.com/BerriAI/litellm/refs/heads/main/model_prices_and_context_window.json"
response = requests.get(url)
data = json.loads(response.text)

# 筛选支持预填充的模型
prefill_models = [model for model, info in data.items() if info.get('supports_assistant_prefill') == True]

# 生成模型列表
model_list = "\n".join(f"- {model}" for model in sorted(prefill_models))

cog.out(model_list)
]]]-->
- anthropic.claude-3-5-haiku-20241022-v1:0
- anthropic.claude-3-5-sonnet-20241022-v2:0
- claude-3-5-haiku-20241022
- claude-3-5-sonnet-20240620
- claude-3-5-sonnet-20241022
- claude-3-haiku-20240307
- claude-3-opus-20240229
- claude-3-sonnet-20240229
- codestral/codestral-2405
- codestral/codestral-latest
- deepseek/deepseek-chat
- deepseek/deepseek-coder
- deepseek/deepseek-reasoner
- eu.anthropic.claude-3-5-haiku-20241022-v1:0
- eu.anthropic.claude-3-5-sonnet-20241022-v2:0
- mistral/codestral-2405
- mistral/codestral-latest
- mistral/codestral-mamba-latest
- mistral/mistral-large-2402
- mistral/mistral-large-2407
- mistral/mistral-large-2411
- mistral/mistral-large-latest
- mistral/mistral-medium
- mistral/mistral-medium-2312
- mistral/mistral-medium-latest
- mistral/mistral-small
- mistral/mistral-small-latest
- mistral/mistral-tiny
- mistral/open-codestral-mamba
- mistral/open-mistral-7b
- mistral/open-mistral-nemo
- mistral/open-mistral-nemo-2407
- mistral/open-mixtral-8x22b
- mistral/open-mixtral-8x7b
- mistral/pixtral-12b-2409
- mistral/pixtral-large-2411
- mistral/pixtral-large-latest
- openrouter/anthropic/claude-3.5-sonnet
- openrouter/deepseek/deepseek-r1
- us.anthropic.claude-3-5-haiku-20241022-v1:0
- us.anthropic.claude-3-5-sonnet-20241022-v2:0
- vertex_ai/claude-3-5-haiku
- vertex_ai/claude-3-5-haiku@20241022
- vertex_ai/claude-3-5-sonnet
- vertex_ai/claude-3-5-sonnet-v2
- vertex_ai/claude-3-5-sonnet-v2@20241022
- vertex_ai/claude-3-5-sonnet@20240620
- vertex_ai/claude-3-haiku
- vertex_ai/claude-3-haiku@20240307
- vertex_ai/claude-3-opus
- vertex_ai/claude-3-opus@20240229
- vertex_ai/claude-3-sonnet
- vertex_ai/claude-3-sonnet@20240229
<!--[[[end]]]-->



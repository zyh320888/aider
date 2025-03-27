---
parent: Configuration
nav_order: 950
description: 配置LLM的高级设置。
---

# 高级模型设置

## 上下文窗口大小和令牌成本

在大多数情况下，您可以安全地忽略aider关于未知上下文窗口大小和模型成本的警告。

{: .note }
Aider从不*强制执行*令牌限制，它只*报告*来自API提供商的令牌限制错误。
您可能不需要为不常见的模型配置aider的正确令牌限制。

但是，您可以为aider不知道的模型注册上下文窗口限制和成本。在以下位置之一创建`.aider.model.metadata.json`文件：

- 您的主目录。
- 您的git仓库根目录。
- 您启动aider的当前目录。
- 或使用`--model-metadata-file <filename>`开关指定特定文件。


如果上述文件存在，它们将按该顺序加载。
最后加载的文件将优先。

json文件应该是一个字典，每个模型有一个条目，如下所示：

```
{
    "deepseek/deepseek-chat": {
        "max_tokens": 4096,
        "max_input_tokens": 32000,
        "max_output_tokens": 4096,
        "input_cost_per_token": 0.00000014,
        "output_cost_per_token": 0.00000028,
        "litellm_provider": "deepseek",
        "mode": "chat"
    }
}
```

{: .tip }
在`.aider.model.metadata.json`文件中使用带有前缀`provider/`的完全限定模型名称。
例如，使用`deepseek/deepseek-chat`，而不仅仅是`deepseek-chat`。
该前缀应与`litellm_provider`字段匹配。

### 贡献模型元数据

Aider依赖于
[litellm的model_prices_and_context_window.json文件](https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json)
获取模型元数据。

考虑向该文件提交PR以添加缺失的模型。

## 模型设置

Aider有许多设置来控制它如何与不同模型一起工作。
这些模型设置针对大多数流行模型都进行了预配置。
但有时覆盖它们或为aider不知道的模型添加设置可能会有所帮助。


### 配置文件位置

您可以通过在以下位置之一创建`.aider.model.settings.yml`文件来覆盖或添加任何模型的设置：

- 您的主目录。
- 您的git仓库根目录。
- 您启动aider的当前目录。
- 或使用`--model-settings-file <filename>`开关指定特定文件。

如果上述文件存在，它们将按该顺序加载。
最后加载的文件将优先。

yaml文件应该是每个模型的字典对象列表。


### 向litellm.completion传递额外参数

模型设置的`extra_params`属性用于在向给定模型发送数据时，
向`litellm.completion()`调用传递任意额外参数。

例如：

```yaml
- name: some-provider/my-special-model
  extra_params:
    extra_headers:
      Custom-Header: value
    max_tokens: 8192
```

### 全局额外参数

您可以使用特殊模型名称`aider/extra_params`定义
将传递给所有模型的`litellm.completion()`的`extra_params`。
此特殊模型名称仅使用`extra_params`字典。

例如：

```yaml
- name: aider/extra_params
  extra_params:
    extra_headers:
      Custom-Header: value
    max_tokens: 8192
```

这些设置将与任何特定于模型的设置合并，对于任何直接冲突，
`aider/extra_params`设置将优先。

### 控制o1推理努力

您需要这段yaml：

```
  extra_params:
    extra_body:
      reasoning_effort: high
```

这是带有该设置的o1完整条目，通过在下面的列表中找到默认条目并添加上述`extra_params`条目获得：

```
- name: o1
  edit_format: diff
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  send_undo_reply: false
  lazy: false
  reminder: user
  examples_as_sys_msg: false
  cache_control: false
  caches_by_default: false
  use_system_prompt: true
  use_temperature: false
  streaming: false
  editor_model_name: gpt-4o
  editor_edit_format: editor-diff
  extra_params:
    extra_body:
      reasoning_effort: high
```

### 默认模型设置

以下是所有预配置的模型设置，以了解所支持的设置。

您还可以查看
[models.py](https://github.com/Aider-AI/aider/blob/main/aider/models.py)
文件中的`ModelSettings`类，了解有关aider支持的所有模型设置的更多详细信息。

第一个条目显示了所有设置及其默认值。
对于实际模型，
您只需包含想要覆盖默认值的字段。

<!--[[[cog
from aider.models import get_model_settings_as_yaml
cog.out("```yaml\n")
cog.out(get_model_settings_as_yaml())
cog.out("```\n")
]]]-->
```yaml
- name: (default values)
  edit_format: whole
  weak_model_name: null
  use_repo_map: false
  send_undo_reply: false
  lazy: false
  overeager: false
  reminder: user
  examples_as_sys_msg: false
  extra_params: null
  cache_control: false
  caches_by_default: false
  use_system_prompt: true
  use_temperature: true
  streaming: true
  editor_model_name: null
  editor_edit_format: null
  reasoning_tag: null
  remove_reasoning: null
  system_prompt_prefix: null
  accepts_settings: null

- name: anthropic/claude-3-5-haiku-20241022
  edit_format: diff
  weak_model_name: anthropic/claude-3-5-haiku-20241022
  use_repo_map: true
  extra_params:
    extra_headers:
      anthropic-beta: prompt-caching-2024-07-31,pdfs-2024-09-25
  cache_control: true

- name: anthropic/claude-3-5-sonnet-20240620
  edit_format: diff
  weak_model_name: anthropic/claude-3-5-haiku-20241022
  use_repo_map: true
  examples_as_sys_msg: true
  extra_params:
    extra_headers:
      anthropic-beta: prompt-caching-2024-07-31,pdfs-2024-09-25
    max_tokens: 8192
  cache_control: true
  editor_model_name: anthropic/claude-3-5-sonnet-20240620
  editor_edit_format: editor-diff

- name: anthropic/claude-3-5-sonnet-20241022
  edit_format: diff
  weak_model_name: anthropic/claude-3-5-haiku-20241022
  use_repo_map: true
  examples_as_sys_msg: true
  extra_params:
    extra_headers:
      anthropic-beta: prompt-caching-2024-07-31,pdfs-2024-09-25
    max_tokens: 8192
  cache_control: true
  editor_model_name: anthropic/claude-3-5-sonnet-20241022
  editor_edit_format: editor-diff

- name: anthropic/claude-3-5-sonnet-latest
  edit_format: diff
  weak_model_name: anthropic/claude-3-5-haiku-20241022
  use_repo_map: true
  examples_as_sys_msg: true
  extra_params:
    extra_headers:
      anthropic-beta: prompt-caching-2024-07-31,pdfs-2024-09-25
    max_tokens: 8192
  cache_control: true
  editor_model_name: anthropic/claude-3-5-sonnet-20241022
  editor_edit_format: editor-diff

- name: anthropic/claude-3-haiku-20240307
  weak_model_name: anthropic/claude-3-haiku-20240307
  examples_as_sys_msg: true
  extra_params:
    extra_headers:
      anthropic-beta: prompt-caching-2024-07-31,pdfs-2024-09-25
  cache_control: true

- name: azure/o1
  edit_format: diff
  weak_model_name: azure/gpt-4o-mini
  use_repo_map: true
  use_temperature: false
  streaming: false
  editor_model_name: azure/gpt-4o
  editor_edit_format: editor-diff

- name: azure/o1-mini
  weak_model_name: azure/gpt-4o-mini
  use_repo_map: true
  use_system_prompt: false
  use_temperature: false
  editor_model_name: azure/gpt-4o
  editor_edit_format: editor-diff

- name: azure/o1-preview
  edit_format: diff
  weak_model_name: azure/gpt-4o-mini
  use_repo_map: true
  use_system_prompt: false
  use_temperature: false
  editor_model_name: azure/gpt-4o
  editor_edit_format: editor-diff

- name: azure/o3-mini
  edit_format: diff
  weak_model_name: azure/gpt-4o-mini
  use_repo_map: true
  use_temperature: false
  editor_model_name: azure/gpt-4o
  editor_edit_format: editor-diff
  system_prompt_prefix: 'Formatting re-enabled. '

- name: bedrock/anthropic.claude-3-5-haiku-20241022-v1:0
  edit_format: diff
  weak_model_name: bedrock/anthropic.claude-3-5-haiku-20241022-v1:0
  use_repo_map: true
  extra_params:
    extra_headers:
      anthropic-beta: prompt-caching-2024-07-31,pdfs-2024-09-25
  cache_control: true

- name: bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0
  edit_format: diff
  weak_model_name: bedrock/anthropic.claude-3-5-haiku-20241022-v1:0
  use_repo_map: true
  examples_as_sys_msg: true
  extra_params:
    extra_headers:
      anthropic-beta: prompt-caching-2024-07-31,pdfs-2024-09-25
    max_tokens: 8192
  cache_control: true
  editor_model_name: bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0
  editor_edit_format: editor-diff

- name: claude-3-5-haiku-20241022
  edit_format: diff
  weak_model_name: claude-3-5-haiku-20241022
  use_repo_map: true
  examples_as_sys_msg: true
  extra_params:
    extra_headers:
      anthropic-beta: prompt-caching-2024-07-31,pdfs-2024-09-25
  cache_control: true

- name: claude-3-5-sonnet-20240620
  edit_format: diff
  weak_model_name: claude-3-5-haiku-20241022
  use_repo_map: true
  examples_as_sys_msg: true
  extra_params:
    extra_headers:
      anthropic-beta: prompt-caching-2024-07-31,pdfs-2024-09-25
    max_tokens: 8192
  cache_control: true
  editor_model_name: claude-3-5-sonnet-20240620
  editor_edit_format: editor-diff

- name: claude-3-5-sonnet-20241022
  edit_format: diff
  weak_model_name: claude-3-5-haiku-20241022
  use_repo_map: true
  examples_as_sys_msg: true
  extra_params:
    extra_headers:
      anthropic-beta: prompt-caching-2024-07-31,pdfs-2024-09-25
    max_tokens: 8192
  cache_control: true
  editor_model_name: claude-3-5-sonnet-20241022
  editor_edit_format: editor-diff

- name: claude-3-haiku-20240307
  weak_model_name: claude-3-haiku-20240307
  examples_as_sys_msg: true
  extra_params:
    extra_headers:
      anthropic-beta: prompt-caching-2024-07-31,pdfs-2024-09-25
  cache_control: true

- name: claude-3-opus-20240229
  edit_format: diff
  weak_model_name: claude-3-5-haiku-20241022
  use_repo_map: true

- name: claude-3-sonnet-20240229
  weak_model_name: claude-3-5-haiku-20241022

- name: command-r-08-2024
  weak_model_name: command-r-08-2024
  use_repo_map: true

- name: command-r-plus
  weak_model_name: command-r-plus
  use_repo_map: true

- name: command-r-plus-08-2024
  weak_model_name: command-r-plus-08-2024
  use_repo_map: true

- name: deepseek-chat
  edit_format: diff
  use_repo_map: true
  reminder: sys
  examples_as_sys_msg: true
  extra_params:
    max_tokens: 8192

- name: deepseek-coder
  edit_format: diff
  use_repo_map: true
  reminder: sys
  examples_as_sys_msg: true
  extra_params:
    max_tokens: 8192
  caches_by_default: true

- name: deepseek/deepseek-chat
  edit_format: diff
  use_repo_map: true
  reminder: sys
  examples_as_sys_msg: true
  extra_params:
    max_tokens: 8192
  caches_by_default: true

- name: deepseek/deepseek-coder
  edit_format: diff
  use_repo_map: true
  reminder: sys
  examples_as_sys_msg: true
  extra_params:
    max_tokens: 8192
  caches_by_default: true

- name: deepseek/deepseek-reasoner
  edit_format: diff
  weak_model_name: deepseek/deepseek-chat
  use_repo_map: true
  examples_as_sys_msg: true
  extra_params:
    max_tokens: 8192
  caches_by_default: true
  use_temperature: false
  editor_model_name: deepseek/deepseek-chat
  editor_edit_format: editor-diff

- name: fireworks_ai/accounts/fireworks/models/deepseek-r1
  edit_format: diff
  weak_model_name: fireworks_ai/accounts/fireworks/models/deepseek-v3
  use_repo_map: true
  extra_params:
    max_tokens: 160000
  use_temperature: false
  editor_model_name: fireworks_ai/accounts/fireworks/models/deepseek-v3
  editor_edit_format: editor-diff
  remove_reasoning: think

- name: fireworks_ai/accounts/fireworks/models/deepseek-v3
  edit_format: diff
  use_repo_map: true
  reminder: sys
  examples_as_sys_msg: true
  extra_params:
    max_tokens: 128000

- name: gemini/gemini-1.5-flash-002

- name: gemini/gemini-1.5-flash-exp-0827

- name: gemini/gemini-1.5-pro
  edit_format: diff-fenced
  use_repo_map: true

- name: gemini/gemini-1.5-pro-002
  edit_format: diff
  use_repo_map: true

- name: gemini/gemini-1.5-pro-exp-0827
  edit_format: diff-fenced
  use_repo_map: true

- name: gemini/gemini-1.5-pro-latest
  edit_format: diff-fenced
  use_repo_map: true

- name: gemini/gemini-2.0-flash
  edit_format: diff
  use_repo_map: true

- name: gemini/gemini-2.0-flash-exp
  edit_format: diff
  use_repo_map: true

- name: gemini/gemini-exp-1114
  edit_format: diff
  use_repo_map: true

- name: gemini/gemini-exp-1121
  edit_format: diff
  use_repo_map: true

- name: gemini/gemini-exp-1206
  edit_format: diff
  use_repo_map: true

- name: gpt-3.5-turbo
  weak_model_name: gpt-4o-mini
  reminder: sys

- name: gpt-3.5-turbo-0125
  weak_model_name: gpt-4o-mini
  reminder: sys

- name: gpt-3.5-turbo-0613
  weak_model_name: gpt-4o-mini
  reminder: sys

- name: gpt-3.5-turbo-1106
  weak_model_name: gpt-4o-mini
  reminder: sys

- name: gpt-3.5-turbo-16k-0613
  weak_model_name: gpt-4o-mini
  reminder: sys

- name: gpt-4-0125-preview
  edit_format: udiff
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  lazy: true
  reminder: sys
  examples_as_sys_msg: true

- name: gpt-4-0314
  edit_format: diff
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  reminder: sys
  examples_as_sys_msg: true

- name: gpt-4-0613
  edit_format: diff
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  reminder: sys

- name: gpt-4-1106-preview
  edit_format: udiff
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  lazy: true
  reminder: sys

- name: gpt-4-32k-0613
  edit_format: diff
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  reminder: sys

- name: gpt-4-turbo
  edit_format: udiff
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  lazy: true
  reminder: sys

- name: gpt-4-turbo-2024-04-09
  edit_format: udiff
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  lazy: true
  reminder: sys

- name: gpt-4-vision-preview
  edit_format: diff
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  reminder: sys

- name: gpt-4o
  edit_format: diff
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  lazy: true
  reminder: sys
  examples_as_sys_msg: true
  editor_edit_format: editor-diff

- name: gpt-4o-2024-08-06
  edit_format: diff
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  lazy: true
  reminder: sys
  examples_as_sys_msg: true

- name: gpt-4o-2024-11-20
  edit_format: diff
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  lazy: true
  reminder: sys
  examples_as_sys_msg: true

- name: gpt-4o-mini
  weak_model_name: gpt-4o-mini
  lazy: true
  reminder: sys

- name: groq/llama3-70b-8192
  edit_format: diff
  weak_model_name: groq/llama3-8b-8192
  examples_as_sys_msg: true

- name: o1
  edit_format: diff
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  use_temperature: false
  streaming: false
  editor_model_name: gpt-4o
  editor_edit_format: editor-diff
  system_prompt_prefix: 'Formatting re-enabled. '

- name: o1-mini
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  use_system_prompt: false
  use_temperature: false
  editor_model_name: gpt-4o
  editor_edit_format: editor-diff

- name: o1-preview
  edit_format: architect
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  use_system_prompt: false
  use_temperature: false
  editor_model_name: gpt-4o
  editor_edit_format: editor-diff

- name: o3-mini
  edit_format: diff
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  use_temperature: false
  editor_model_name: gpt-4o
  editor_edit_format: editor-diff
  system_prompt_prefix: 'Formatting re-enabled. '

- name: openai/gpt-4o
  edit_format: diff
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  lazy: true
  reminder: sys
  examples_as_sys_msg: true
  editor_edit_format: editor-diff

- name: openai/gpt-4o-2024-08-06
  edit_format: diff
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  lazy: true
  reminder: sys
  examples_as_sys_msg: true

- name: openai/gpt-4o-2024-11-20
  edit_format: diff
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  lazy: true
  reminder: sys
  examples_as_sys_msg: true

- name: openai/gpt-4o-mini
  weak_model_name: openai/gpt-4o-mini
  lazy: true
  reminder: sys

- name: openai/o1
  edit_format: diff
  weak_model_name: openai/gpt-4o-mini
  use_repo_map: true
  use_temperature: false
  streaming: false
  editor_model_name: openai/gpt-4o
  editor_edit_format: editor-diff
  system_prompt_prefix: 'Formatting re-enabled. '

- name: openai/o1-mini
  weak_model_name: openai/gpt-4o-mini
  use_repo_map: true
  use_system_prompt: false
  use_temperature: false
  editor_model_name: openai/gpt-4o
  editor_edit_format: editor-diff

- name: openai/o1-preview
  edit_format: diff
  weak_model_name: openai/gpt-4o-mini
  use_repo_map: true
  use_system_prompt: false
  use_temperature: false
  editor_model_name: openai/gpt-4o
  editor_edit_format: editor-diff

- name: openai/o3-mini
  edit_format: diff
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  use_temperature: false
  editor_model_name: gpt-4o
  editor_edit_format: editor-diff
  system_prompt_prefix: 'Formatting re-enabled. '

- name: openrouter/anthropic/claude-3-opus
  edit_format: diff
  weak_model_name: openrouter/anthropic/claude-3-5-haiku
  use_repo_map: true

- name: openrouter/anthropic/claude-3.5-sonnet
  edit_format: diff
  weak_model_name: openrouter/anthropic/claude-3-5-haiku
  use_repo_map: true
  examples_as_sys_msg: true
  extra_params:
    max_tokens: 8192
  cache_control: true
  editor_model_name: openrouter/anthropic/claude-3.5-sonnet
  editor_edit_format: editor-diff

- name: openrouter/anthropic/claude-3.5-sonnet:beta
  edit_format: diff
  weak_model_name: openrouter/anthropic/claude-3-5-haiku:beta
  use_repo_map: true
  examples_as_sys_msg: true
  extra_params:
    max_tokens: 8192
  cache_control: true
  editor_model_name: openrouter/anthropic/claude-3.5-sonnet:beta
  editor_edit_format: editor-diff

- name: openrouter/deepseek/deepseek-chat
  edit_format: diff
  use_repo_map: true
  reminder: sys
  examples_as_sys_msg: true

- name: openrouter/deepseek/deepseek-coder
  edit_format: diff
  use_repo_map: true
  reminder: sys
  examples_as_sys_msg: true

- name: openrouter/deepseek/deepseek-r1
  edit_format: diff
  weak_model_name: openrouter/deepseek/deepseek-chat
  use_repo_map: true
  examples_as_sys_msg: true
  extra_params:
    max_tokens: 8192
  caches_by_default: true
  use_temperature: false
  editor_model_name: openrouter/deepseek/deepseek-chat
  editor_edit_format: editor-diff

- name: openrouter/deepseek/deepseek-r1-distill-llama-70b
  edit_format: diff
  weak_model_name: openrouter/deepseek/deepseek-chat
  use_repo_map: true
  examples_as_sys_msg: true
  extra_params:
    max_tokens: 8192
  caches_by_default: true
  use_temperature: false
  editor_model_name: openrouter/deepseek/deepseek-chat
  editor_edit_format: editor-diff

- name: openrouter/deepseek/deepseek-r1:free
  edit_format: diff
  weak_model_name: openrouter/deepseek/deepseek-r1:free
  use_repo_map: true
  examples_as_sys_msg: true
  extra_params:
    max_tokens: 8192
  caches_by_default: true
  use_temperature: false
  editor_model_name: openrouter/deepseek/deepseek-r1:free
  editor_edit_format: editor-diff

- name: openrouter/meta-llama/llama-3-70b-instruct
  edit_format: diff
  weak_model_name: openrouter/meta-llama/llama-3-70b-instruct
  examples_as_sys_msg: true

- name: openrouter/openai/gpt-4o
  edit_format: diff
  weak_model_name: openrouter/openai/gpt-4o-mini
  use_repo_map: true
  lazy: true
  reminder: sys
  examples_as_sys_msg: true
  editor_edit_format: editor-diff

- name: openrouter/openai/o1
  edit_format: diff
  weak_model_name: openrouter/openai/gpt-4o-mini
  use_repo_map: true
  use_temperature: false
  streaming: false
  editor_model_name: openrouter/openai/gpt-4o
  editor_edit_format: editor-diff
  system_prompt_prefix: 'Formatting re-enabled. '

- name: openrouter/openai/o1-mini
  weak_model_name: openrouter/openai/gpt-4o-mini
  use_repo_map: true
  use_system_prompt: false
  use_temperature: false
  streaming: false
  editor_model_name: openrouter/openai/gpt-4o
  editor_edit_format: editor-diff

- name: openrouter/openai/o1-preview
  edit_format: diff
  weak_model_name: openrouter/openai/gpt-4o-mini
  use_repo_map: true
  use_system_prompt: false
  use_temperature: false
  streaming: false
  editor_model_name: openrouter/openai/gpt-4o
  editor_edit_format: editor-diff

- name: openrouter/openai/o3-mini
  edit_format: diff
  weak_model_name: openrouter/openai/gpt-4o-mini
  use_repo_map: true
  use_temperature: false
  editor_model_name: openrouter/openai/gpt-4o
  editor_edit_format: editor-diff
  system_prompt_prefix: 'Formatting re-enabled. '

- name: openrouter/qwen/qwen-2.5-coder-32b-instruct
  edit_format: diff
  weak_model_name: openrouter/qwen/qwen-2.5-coder-32b-instruct
  use_repo_map: true
  editor_model_name: openrouter/qwen/qwen-2.5-coder-32b-instruct
  editor_edit_format: editor-diff

- name: vertex_ai/claude-3-5-haiku@20241022
  edit_format: diff
  weak_model_name: vertex_ai/claude-3-5-haiku@20241022
  use_repo_map: true
  extra_params:
    max_tokens: 4096

- name: vertex_ai/claude-3-5-sonnet-v2@20241022
  edit_format: diff
  weak_model_name: vertex_ai/claude-3-5-haiku@20241022
  use_repo_map: true
  examples_as_sys_msg: true
  extra_params:
    max_tokens: 8192
  editor_model_name: vertex_ai/claude-3-5-sonnet-v2@20241022
  editor_edit_format: editor-diff

- name: vertex_ai/claude-3-5-sonnet@20240620
  edit_format: diff
  weak_model_name: vertex_ai/claude-3-5-haiku@20241022
  use_repo_map: true
  examples_as_sys_msg: true
  extra_params:
    max_tokens: 8192
  editor_model_name: vertex_ai/claude-3-5-sonnet@20240620
  editor_edit_format: editor-diff

- name: vertex_ai/claude-3-opus@20240229
  edit_format: diff
  weak_model_name: vertex_ai/claude-3-5-haiku@20241022
  use_repo_map: true

- name: vertex_ai/claude-3-sonnet@20240229
  weak_model_name: vertex_ai/claude-3-5-haiku@20241022

- name: vertex_ai/gemini-pro-experimental
  edit_format: diff-fenced
  use_repo_map: true
```
<!--[[[end]]]-->



---
parent: 连接到LLMs
nav_order: 200
---

# Anthropic

要使用Anthropic的模型，您需要提供您的[Anthropic API密钥](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)，可以通过`ANTHROPIC_API_KEY`环境变量或`--anthropic-api-key`命令行参数提供。

Aider内置了最流行的Anthropic模型的快捷方式，并经过测试和基准测试，可以与它们很好地配合使用：

```
python -m pip install -U aider-chat

export ANTHROPIC_API_KEY=<key> # Mac/Linux
setx   ANTHROPIC_API_KEY <key> # Windows, 使用setx后需重启shell

# Aider默认使用Claude 3.7 Sonnet
aider

# Claude 3 Opus
aider --model claude-3-opus-20240229

# 列出Anthropic可用的模型
aider --list-models anthropic/
```

{: .tip }
Anthropic有非常低的速率限制。
您可以通过[OpenRouter](openrouter.md)或[Google Vertex AI](vertex.md)访问所有Anthropic模型，这些平台提供更宽松的速率限制。

您可以使用`aider --model <model-name>`来使用任何其他Anthropic模型。
例如，如果您想使用特定版本的Opus，可以执行`aider --model claude-3-opus-20240229`。

## 思考tokens

Aider可以使用Sonnet 3.7的新思考tokens功能，但默认情况下不会要求Sonnet使用思考tokens。

启用思考功能目前需要手动配置。
您需要在您的`.aider.model.settings.yml`[模型设置文件](/docs/config/adv-model-settings.html#model-settings)中添加以下内容。
调整`budget_tokens`值来更改目标思考tokens的数量。

```yaml
- name: anthropic/claude-3-7-sonnet-20250219
  edit_format: diff
  weak_model_name: anthropic/claude-3-5-haiku-20241022
  use_repo_map: true
  examples_as_sys_msg: true
  use_temperature: false
  extra_params:
    extra_headers:
      anthropic-beta: prompt-caching-2024-07-31,pdfs-2024-09-25,output-128k-2025-02-19
    max_tokens: 64000
    thinking:
      type: enabled
      budget_tokens: 32000 # 调整这个数字
  cache_control: true
  editor_model_name: anthropic/claude-3-7-sonnet-20250219
  editor_edit_format: editor-diff
```

更简化的支持将很快推出。

---
parent: 配置
nav_order: 110
description: 如何配置来自次要提供商的推理模型设置。
---

# 推理模型

![思考演示](/assets/thinking.jpg)

## 基本用法

Aider 配置为开箱即可使用大多数流行的推理模型。
您可以这样使用它们：

```bash
# Sonnet 使用思考令牌预算
aider --model sonnet --thinking-tokens 8k

# o3-mini 使用低/中/高推理努力级别
aider --model o3-mini --reasoning-effort high

# R1 没有可配置的思考/推理
aider --model r1
```

在 aider 聊天中，您可以使用 `/thinking-tokens 4k` 或 `/reasoning-effort low` 来更改
推理量。

本文档的其余部分描述了更高级的细节，这些细节主要在
如果您正在配置 aider 以使用较少知名的推理模型或通过
非常规提供商提供的模型时才需要。

## 推理设置

不同的模型支持不同的推理设置。Aider 提供了几种控制推理行为的方法：

### 推理努力级别

您可以使用 `--reasoning-effort` 开关来控制支持此设置的模型的推理努力程度。
这个开关对 OpenAI 的推理模型很有用，它们接受 "low"、"medium" 和 "high"。

### 思考令牌

您可以使用 `--thinking-tokens` 开关请求
模型使用特定数量的思考令牌。
这个开关对 Sonnet 3.7 很有用。
您可以指定令牌预算，如 "1024"、"1k"、"8k" 或 "0.01M"。

### 模型兼容性和设置

并非所有模型都支持这两种设置。Aider 使用
[模型的元数据](/docs/config/adv-model-settings.html)
来确定每个模型接受哪些设置：

```yaml
- name: o3-mini
  ...
  accepts_settings: ["reasoning_effort"]
```

如果您尝试使用模型不明确支持的设置，Aider 将警告您：

```
警告：o3-mini 不支持 'thinking_tokens'，忽略。
使用 --no-check-model-accepts-settings 强制使用 'thinking_tokens' 设置。
```

该警告告诉您：
1. 由于模型在 `accepts_settings` 中没有列出该设置，因此不会应用该设置
2. 您可以使用 `--no-check-model-accepts-settings` 强制应用该设置

这个功能有助于防止 API 错误，同时仍允许您在需要时尝试设置。

每个模型在其配置中都有一个预定义的支持设置列表。例如：

- OpenAI 推理模型通常支持 `reasoning_effort`
- Anthropic 推理模型通常支持 `thinking_tokens`


### `accepts_settings` 的工作原理

模型使用 `accepts_settings` 属性定义它们接受哪些推理设置：

```yaml
- name: a-fancy-reasoning-model
  edit_format: diff
  use_repo_map: true
  accepts_settings:                  # <---
    - reasoning_effort               # <---
```

这个配置：
1. 告诉 Aider 该模型接受 `reasoning_effort` 设置
2. 表示该模型不接受 `thinking_tokens`（因为它没有列出）
3. 导致 Aider 忽略为此模型传递的任何 `--thinking-tokens` 值
4. 如果您尝试对此模型使用 `--thinking-tokens`，会生成警告

您可以使用 `--no-check-model-accepts-settings` 覆盖此行为，它将：
1. 强制 Aider 应用通过命令行传递的所有设置
2. 跳过所有兼容性检查
3. 如果模型真的不支持该设置，可能会导致 API 错误

这在测试新模型或通过自定义 API 提供商使用模型时很有用。


## XML 标签中的思考令牌

还有一个 `reasoning_tag` 设置，它接受模型用来包装其推理/思考输出的 XML 标签的名称。

例如，当使用来自 Fireworks 的 DeepSeek R1 时，推理会在
`<think>...</think>` 标签内返回，因此 aider 的设置
包括 `reasoning_tag: think`。

```
<think>
用户想要我问候他们！
</think>

你好！
```

Aider 将显示思考/推理输出，
但它不会用于文件编辑指令，不会添加到聊天历史记录等。
Aider 将依靠非思考输出来获取如何进行代码更改的指令等。

### 特定模型的推理标签

不同的模型使用不同的 XML 标签进行推理：
当使用自定义或自托管模型时，您可能需要在配置中指定适当的推理标签。

```yaml
- name: fireworks_ai/accounts/fireworks/models/deepseek-r1
  edit_format: diff
  weak_model_name: fireworks_ai/accounts/fireworks/models/deepseek-v3
  use_repo_map: true
  extra_params:
    max_tokens: 160000
  use_temperature: false
  editor_model_name: fireworks_ai/accounts/fireworks/models/deepseek-v3
  editor_edit_format: editor-diff
  reasoning_tag: think                 # <---
```

## 推理模型限制

许多"推理"模型在使用方式上有限制：
它们有时禁止流式传输、使用温度和/或系统提示。
Aider 配置为在通过主要提供商 API 提供服务时与流行模型正常工作。

如果您通过不同的提供商（如 Azure 或自定义部署）使用模型，
您可能需要[配置模型设置](/docs/config/adv-model-settings.html)，
如果您看到与温度或系统提示相关的错误。

在项目根目录或主目录中包含新提供商的设置，放在 `.aider.model.settings.yml` 文件中。

### 温度、流式传输和系统提示

推理模型通常对这些设置有特定要求：

| 设置 | 描述 | 常见限制 |
|---------|-------------|---------------------|
| `use_temperature` | 是否使用温度采样 | 许多推理模型要求将此设置为 `false` |
| `streaming` | 是否流式传输响应 | 一些推理模型不支持流式传输 |
| `use_system_prompt` | 是否使用系统提示 | 一些推理模型不支持系统提示 |

查找一个您感兴趣的模型的[现有模型设置配置条目](https://github.com/Aider-AI/aider/blob/main/aider/resources/model-settings.yml)可能会有所帮助，比如 o3-mini：

```yaml
- name: o3-mini
  edit_format: diff
  weak_model_name: gpt-4o-mini
  use_repo_map: true
  use_temperature: false             # <---
  editor_model_name: gpt-4o
  editor_edit_format: editor-diff
  accepts_settings: ["reasoning_effort"]
```

注意这些设置，对于某些推理模型，必须将它们设置为 `false`：

- `use_temperature`
- `streaming` 
- `use_system_prompt`

### 自定义提供商示例

这里是通过 Azure 使用 o3-mini 的设置示例。
注意，aider 已经预先配置了这些设置，但它们
作为如何为不同提供商调整主要模型设置的良好示例。

```yaml
- name: azure/o3-mini
  edit_format: diff
  weak_model_name: azure/gpt-4o-mini
  use_repo_map: true
  use_temperature: false             # <---
  editor_model_name: azure/gpt-4o
  editor_edit_format: editor-diff
  accepts_settings: ["reasoning_effort"]
```

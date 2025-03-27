---
parent: 配置
nav_order: 1000
description: 为模型分配方便的简短名称。
---

# 模型别名

模型别名允许您为经常使用的模型创建简写名称。这对于名称较长的模型或当您想在团队中标准化模型使用时特别有用。

## 命令行用法

您可以在启动aider时使用`--alias`选项定义别名：

```bash
aider --alias "fast:gpt-4o-mini" --alias "smart:o3-mini"
```

通过多次使用`--alias`选项可以定义多个别名。每个别名定义应采用`alias:model-name`格式。

## 配置文件

当然，您还可以在[`.aider.conf.yml`文件](https://aider.chat/docs/config/aider_conf.html)中定义别名：

```yaml
alias:
  - "fast:gpt-4o-mini"
  - "smart:o3-mini"
  - "hacker:claude-3-sonnet-20240229"
```

## 使用别名

一旦定义，您可以在命令行中使用别名代替完整的模型名称：

```bash
aider --model fast  # 使用gpt-4o-mini
aider --model smart  # 使用o3-mini
```

或者在聊天中使用`/model`命令：

```
Aider v0.75.3
Main model: anthropic/claude-3-7-sonnet-20250219 with diff edit format, prompt cache, infinite output
Weak model: claude-3-5-sonnet-20241022
Git repo: .git with 406 files
Repo-map: using 4096 tokens, files refresh
─────────────────────────────────────────────────────────────────────────────────────────────────────
> /model fast

Aider v0.75.3
Main model: gpt-4o-mini with diff edit format
─────────────────────────────────────────────────────────────────────────────────────────────────────
diff> /model smart

Aider v0.75.3
Main model: o3-mini with diff edit format
─────────────────────────────────────────────────────────────────────────────────────────────────────
>
```

## 内置别名

Aider包含一些内置别名，方便使用：

<!--[[[cog
import cog
from aider.models import MODEL_ALIASES

for alias, model in sorted(MODEL_ALIASES.items()):
    cog.outl(f"- `{alias}`: {model}")
]]]-->
- `3`: gpt-3.5-turbo
- `35-turbo`: gpt-3.5-turbo
- `35turbo`: gpt-3.5-turbo
- `4`: gpt-4-0613
- `4-turbo`: gpt-4-1106-preview
- `4o`: gpt-4o
- `deepseek`: deepseek/deepseek-chat
- `flash`: gemini/gemini-2.0-flash-exp
- `gemini-2.5-pro`: gemini/gemini-2.5-pro-exp-03-25
- `haiku`: claude-3-5-haiku-20241022
- `opus`: claude-3-opus-20240229
- `r1`: deepseek/deepseek-reasoner
- `sonnet`: anthropic/claude-3-7-sonnet-20250219
<!--[[[end]]]-->

## 优先级

如果在多个地方定义了相同的别名，优先级为：

1. 命令行别名（最高优先级）
2. 配置文件别名
3. 内置别名（最低优先级）

这允许您用自己的偏好覆盖内置别名。

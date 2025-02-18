---
parent: 使用指南
nav_order: 60
description: 使用代码模式、架构模式、问答模式和帮助模式进行聊天交互。
---

# 聊天模式

Aider 提供以下几种不同的聊天模式：

- `code` - Aider 会直接修改代码来满足您的要求
- `architect` - Aider 会先提出解决方案，然后询问是否要将其转化为文件修改
- `ask` - Aider 会回答关于代码的问题，但不会修改代码
- `help` - Aider 会回答关于使用 aider、配置和故障排除等问题

默认情况下，aider 以"code"模式启动。在聊天过程中，您可以使用以下命令为特定消息指定模式：
`/code`、`/architect`、`/ask` 和 `/help`。这些斜杠命令仅适用于当前消息，下条消息将返回当前激活模式（默认为"code"模式）。

您可以使用 `/chat-mode <模式>` 命令永久切换激活模式：

```
/chat-mode code
/chat-mode architect
/chat-mode ask
/chat-mode help
```

或者使用无参数命令在编码模式间切换：

```
/code
/architect
/ask
```

也可以通过 `--chat-mode <模式>` 参数启动对应模式，或使用 `--architect` 快捷方式启动架构模式。

## 架构模式与编辑器模型

在架构模式下，aider 会将您的请求发送给两个模型：

1. 首先发送给主模型（通过 `/model`、`--model` 或 `--sonnet` 等快捷参数配置）。主模型回复后，aider 会询问是否根据回复内容修改文件

2. 确认修改时，aider 会发送第二个 LLM 请求来获取具体的代码编辑指令。这个请求会发送给"编辑器"模型。aider 会根据主模型自动选择默认编辑器模型，您也可以用 `--editor-model <模型>` 自行选择

架构模式比代码模式能产生更好的结果，但需要两次 LLM 请求，因此速度和成本可能更高。

当使用 OpenAI 的 o1 系列模型时，架构模式特别有用。这些模型擅长推理但编辑能力较弱，配合 GPT-4o 或 Sonnet 作为编辑器模型效果最佳。

即使主模型和编辑器模型都使用 GPT-4o 或 Sonnet，架构模式也能通过两次请求获得更好的结果。编辑器模型使用 aider 的编辑格式来修改源代码，默认会自动选择合适格式，也可以通过 `--editor-edit-format <格式>` 自定义。建议使用["editor-diff" 和 "editor-whole" 编辑格式](/docs/more/edit-formats.html#editor-diff-and-editor-whole)。详见[架构模式技术文章](/2024/09/26/architect.html)。


## 使用示例

<div class="chat-transcript" markdown="1">


> Aider v0.47.1-dev  
> 模型: claude-3-5-sonnet-20240620 使用 diff 编辑格式  
> Git 仓库: .git 包含 298 个文件  
> 仓库映射: 使用 1024 tokens  
> 使用 /help 查看聊天命令，运行时使用 --help 查看命令行参数  

#### /ask 这个仓库是什么？

这是流行 Django 包的源代码仓库。

#### /help 如何使用 ollama？

运行 `aider --model ollama/<ollama模型>`，详见这些文档：https://aider.chat/docs/llms/ollama.html

#### /code 添加计算阶乘的函数

好的！我将添加计算阶乘的函数：

```python
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

# 使用示例
print(factorial(5))  # 输出: 120
```

这个递归实现的阶乘函数已添加到您的代码中。

#### /architect 能否简化这个实现？

可以改用 `math.factorial()` 内置函数。这样无需维护自定义实现，且内置函数经过优化。

> 要修改文件吗？(Y)是/(N)否 [是]: 是

```python
<<<<<<< SEARCH
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)
=======
from math import factorial
>>>>>>> REPLACE
```

</div>


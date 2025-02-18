---
nav_order: 30
has_children: true
description: 如何使用 aider 与 AI 结对编程，并在本地 git 仓库中编辑代码。
---

# 使用指南

运行 `aider` 时带上您想要编辑的源代码文件。
这些文件会被"添加到聊天会话"中，以便
aider 可以查看其内容并为您进行编辑。
可以是现有文件或您希望 aider 创建的新文件。

```
aider <文件1> <文件2> ...
```

在 aider 的 `>` 提示符下，提出代码修改请求，
aider 将编辑这些文件来完成您的要求。

```
$ aider factorial.py

Aider v0.37.1-dev
模型: 使用 diff 编辑格式的 gpt-4o，弱模型 gpt-3.5-turbo
Git 仓库: .git 包含 258 个文件
仓库地图: 使用 1024 个 token
使用 /help 查看聊天命令，运行 --help 查看命令行参数
───────────────────────────────────────────────────────────────────────
> 编写一个要求输入数字并输出其阶乘的程序

...
```

{% include help-tip.md %}

## 添加文件

要编辑文件，您需要"将它们添加到聊天会话"中。
可以通过在 aider 命令行中指定文件名，
或使用聊天中的 `/add` 命令来添加文件。

只添加任务需要编辑的文件。
不要添加大量无关文件。
如果添加过多文件，LLM 可能会不知所措
并产生混乱（同时会增加 token 消耗）。
Aider 会自动
从相关文件中提取内容，以便
[理解代码库的其余部分](https://aider.chat/docs/repomap.html)。

您也可以不添加任何文件直接使用 aider，
它会根据您的要求尝试推断需要编辑哪些文件。

{: .tip }
如果您能明确需要编辑哪些文件，将获得最佳结果。
只将**这些**文件添加到聊天会话。Aider 会从
仓库的其余部分包含相关上下文。

## 大语言模型

{% include works-best.md %}

```
# o3-mini
$ aider --model o3-mini --api-key openai=<密钥>

# Claude 3.5 Sonnet
$ aider --model sonnet --api-key anthropic=<密钥>
```

或者您可以使用 `aider --model XXX` 启动 aider 并
选择其他模型。
在聊天过程中，您可以使用 `/model` 命令随时切换模型。

## 进行修改

要求 aider 对代码进行修改。
它会显示所做的 diff 变更。
[Aider 会将所有修改进行 git 提交](/docs/git.html)，
便于跟踪和撤销。

您始终可以使用 `/undo` 命令撤销不满意的 AI 修改。

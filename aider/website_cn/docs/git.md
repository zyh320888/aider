---
parent: 更多信息
nav_order: 100
description: Aider与Git深度集成。
---

# Git集成

Aider在与Git仓库配合使用时效果最佳。Aider与Git深度集成，这使得您可以轻松：

- 使用`/undo`命令立即撤销任何不满意的AI更改
- 回溯Git历史记录查看Aider对代码的修改
- 在Git分支上管理Aider的系列更改

Aider通过以下方式使用Git：

- 如果在非Git目录启动，Aider会提示创建Git仓库
- 每次编辑文件后，都会用描述性提交信息进行提交，便于撤销或审查更改
- 在编辑已有未提交更改（脏文件）前，Aider会先提交现有更改。这可以将您的编辑与Aider的修改分开，确保不会因不当修改丢失工作

## 聊天命令

您可以使用[聊天命令](/docs/usage/commands.html)执行Git操作：

- `/diff` 显示自上次消息以来的所有文件更改
- `/undo` 撤销并丢弃最后一次更改
- `/commit` 用合理的提交信息提交所有脏更改
- `/git` 允许运行原始Git命令进行更复杂的历史管理

您也可以使用其他Git工具管理历史记录。

## 禁用Git集成

虽然不推荐，但可以通过以下方式禁用Git集成：

- `--no-auto-commits` 停止自动提交Aider的每次更改
- `--no-dirty-commits` 停止在编辑前提交脏文件
- `--no-git` 完全禁用Git功能（需自行做好文件备份）
- `--git-commit-verify` 在提交时运行pre-commit钩子。默认情况下，Aider通过使用`--no-verify`标志跳过pre-commit钩子（`--git-commit-verify=False`）。

## 提交信息

Aider会向`--weak-model`发送差异和聊天记录来生成遵循[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)规范的提交信息。

可通过`--commit-prompt`选项自定义[提交提示](https://github.com/Aider-AI/aider/blob/main/aider/prompts.py#L5)，支持命令行配置或[配置文件/环境变量](https://aider.chat/docs/config.html)。

## 提交归属

Aider通过以下方式标记其参与的提交：

- 当Aider创作提交时，Git作者和提交者元数据会附加"(aider)"
- 当仅提交现有更改时，提交者元数据附加"(aider)"

可用选项控制元数据：
- `--no-attribute-author` 禁用作者元数据标记
- `--no-attribute-committer` 禁用提交者元数据标记

提交信息前缀选项：
- `--attribute-commit-message-author` 在Aider创作的提交前加'aider: '前缀
- `--attribute-commit-message-committer` 为所有提交添加'aider: '前缀

（默认关闭这些前缀选项，但有助于识别Aider的更改）

---
title: 安装指南
has_children: true
nav_order: 20
description: 如何安装 aider 并开始 AI 结对编程。
lang: zh-CN
---

# 安装指南
{: .no_toc }

## 使用 aider-install 快速开始

{% include get-started.md %}

这将在独立的 Python 环境中安装 aider。
如果需要，
aider-install 还会安装一个单独的 Python 3.12 版本来运行 aider。

安装完成后，
您还可以执行一些[可选的安装步骤](/zh-CN/docs/install/optional.html)。

查看[使用说明](https://aider.chat/zh-CN/docs/usage.html)开始使用 aider 进行编程。

## 一键安装

以下是一键安装命令，如果需要的话也会安装 Python 3.12。
这些命令基于 [uv 安装程序](https://docs.astral.sh/uv/getting-started/installation/)。

#### Windows

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://aider.chat/install.ps1 | iex"
```

#### Mac 和 Linux

使用 curl 下载并执行安装脚本：

```bash
curl -LsSf https://aider.chat/install.sh | sh
```

如果您的系统没有安装 curl，可以使用 wget：

```bash
wget -qO- https://aider.chat/install.sh | sh
```

## 使用 uv 安装

您可以使用 uv 安装 aider：

```bash
python -m pip install uv  # 如果需要安装 uv
uv tool install --force --python python3.12 aider-chat@latest
```

这将使用您现有的 Python 版本（3.8-3.13）安装 uv，
并用它来安装 aider。
如果需要，
uv 会自动安装一个单独的 Python 3.12 来运行 aider。

另请参阅 [uv 本身的其他安装方法文档](https://docs.astral.sh/uv/getting-started/installation/)。

## 使用 pipx 安装

您可以使用 pipx 安装 aider：

```bash
python -m pip install pipx  # 如果需要安装 pipx
pipx install aider-chat
```

您可以使用 pipx 在 Python 3.9-3.12 版本中安装 aider。

另请参阅 [pipx 本身的其他安装方法文档](https://pipx.pypa.io/stable/installation/)。

## 其他安装方法

您可以使用以下方法安装 aider，但通常使用上述方法之一会更安全。

#### 使用 pip 安装

如果您使用 pip 安装，建议使用
[虚拟环境](https://docs.python.org/3/library/venv.html)
来隔离 aider 的依赖项。

您可以使用 pip 在 Python 3.9-3.12 版本中安装 aider。

```bash
python -m pip install -U --upgrade-strategy only-if-needed aider-chat
```

{% include python-m-aider.md %}

#### 使用包管理器安装

建议使用上述推荐的方法之一来安装 aider。
虽然 aider 在许多系统包管理器中都可用，
但它们往往会安装错误的依赖项。

## 下一步...

您可以考虑执行一些[可选的安装步骤](/zh-CN/docs/install/optional.html)。
查看[使用说明](https://aider.chat/zh-CN/docs/usage.html)开始使用 aider 进行编程。 
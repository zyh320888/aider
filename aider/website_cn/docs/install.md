---
title: 安装
has_children: true
nav_order: 20
description: 如何安装并开始与aider进行结对编程。
---

# 安装
{: .no_toc }


## 使用aider-install快速入门

{% include get-started.md %}

这将在独立的Python环境中安装aider。
如有需要，
aider-install还会安装单独的Python 3.12版本供aider使用。

安装aider后，
还有一些[可选的安装步骤](/docs/install/optional.html)。

查看[使用说明](https://aider.chat/docs/usage.html)开始使用aider进行编码。

## 一键安装命令

以下一行命令可以安装aider，如果需要还会安装Python 3.12。
它们基于
[uv安装程序](https://docs.astral.sh/uv/getting-started/installation/)。

#### Windows

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://aider.chat/install.ps1 | iex"
```

#### Mac和Linux

使用curl下载脚本并用sh执行：

```bash
curl -LsSf https://aider.chat/install.sh | sh
```

如果您的系统没有curl，可以使用wget：

```bash
wget -qO- https://aider.chat/install.sh | sh
```


## 使用uv安装

您可以使用uv安装aider：

```bash
python -m pip install uv  # 如果您需要安装uv
uv tool install --force --python python3.12 aider-chat@latest
```

这将使用您现有的Python版本(3.8-3.13)安装uv，
然后使用它来安装aider。
如有需要，
uv会自动安装单独的Python 3.12供aider使用。

另请参阅
[安装uv本身的其他方法文档](https://docs.astral.sh/uv/getting-started/installation/)。

## 使用pipx安装

您可以使用pipx安装aider：

```bash
python -m pip install pipx  # 如果您需要安装pipx
pipx install aider-chat
```

您可以使用pipx通过Python 3.9-3.12版本安装aider。

另请参阅
[安装pipx本身的其他方法文档](https://pipx.pypa.io/stable/installation/)。

## 其他安装方法

您可以使用以下方法安装aider，但通常上述方法之一更安全。

#### 使用pip安装

如果您使用pip安装，应考虑使用
[虚拟环境](https://docs.python.org/3/library/venv.html)
来分离aider的依赖项。

您可以使用pip通过Python 3.9-3.12版本安装aider。

```bash
python -m pip install -U --upgrade-strategy only-if-needed aider-chat
```

{% include python-m-aider.md %}

#### 使用包管理器安装

最好使用上面推荐的方法之一安装aider。
虽然aider在许多系统包管理器中可用，
但它们经常安装带有不正确依赖项的aider。

## 后续步骤...

您可以考虑一些[可选的安装步骤](/docs/install/optional.html)。
查看[使用说明](https://aider.chat/docs/usage.html)开始使用aider进行编码。


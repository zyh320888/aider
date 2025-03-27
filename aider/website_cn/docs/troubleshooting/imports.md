---
parent: 故障排除
nav_order: 28
---

# 依赖版本问题

Aider 需要安装正确版本的所有必需依赖项才能正常工作。

如果您是从 GitHub 问题链接到此文档，
或者 aider 报告 `ImportErrors` 错误，
很可能是您的 aider 安装使用了不正确的依赖项。


## 避免包冲突

如果您正在使用 aider 处理 Python 项目，有时您的项目可能需要
特定版本的 Python 包，而这些版本与 aider 所需的版本冲突。
如果发生这种情况，您可能会在运行 pip 安装时看到类似的错误：

```
aider-chat 0.23.0 requires somepackage==X.Y.Z, but you have somepackage U.W.V which is incompatible.
```

## 使用 aider-install、uv 或 pipx 安装

如果您遇到依赖问题，建议考虑
[使用 aider-install、uv 或 pipx 安装 aider](/docs/install.html)。
这将确保 aider 安装在自己的 Python 环境中，
并拥有正确的依赖集。

## 包管理器如 Homebrew、AUR、ports

包管理器通常会安装带有错误依赖项的 aider，导致
导入错误和其他问题。

推荐
[使用 aider-install、uv 或 pipx 安装 aider](/docs/install.html)。


## 依赖版本很重要

Aider 锁定其依赖项并经过测试以确保与这些特定版本兼容。
如果您直接使用 pip 安装 aider，
在升级或降级 aider 使用的 Python 包时应该格外小心。

特别注意
[aider 的 requirements.in 文件](https://github.com/Aider-AI/aider/blob/main/requirements/requirements.in)
末尾标注的固定版本包。
这些版本之所以固定，是因为 aider 已知无法与
这些库的最新版本一起工作。

同样要谨慎升级 `litellm`，因为它经常更改版本
并有时会引入错误或不向后兼容的更改。

## Replit

{% include replit-pipx.md %}

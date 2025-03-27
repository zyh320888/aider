---
nav_order: 55
has_children: true
description: 关于aider所有设置及其使用方法的信息。
---

# 配置

Aider有许多选项可以通过命令行开关设置。
大多数选项也可以在`.aider.conf.yml`文件中设置，
该文件可以放在您的主目录或Git仓库的根目录中。
或者通过在shell或`.env`文件中设置环境变量，如`AIDER_xxx`。

以下是设置选项的4种等效方式。

使用命令行开关：

```
$ aider --dark-mode
```

使用`.aider.conf.yml`文件：

```yaml
dark-mode: true
```

通过设置环境变量：

```
export AIDER_DARK_MODE=true
```

使用`.env`文件：

```
AIDER_DARK_MODE=true
```

{% include keys.md %}


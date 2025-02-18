---
parent: 使用指南
nav_order: 901
description: 使用 aider 编辑配置文件、文档和其他基于文本的格式。
---

# 编辑配置和文本文件

Aider 不仅适用于代码编辑，在修改几乎任何文本文件时都能提供帮助。你可以用 aider 来修改 shell/ssh 配置、
Dockerfile 或任何配置/文档文件。

以下是一些常见配置/文本文件修改的实用示例：

## Shell 配置

<div class="chat-transcript" markdown="1">
$ aider .bashrc

已将 .bashrc 添加到对话


#### 添加显示全部文件详细信息的人类可读格式别名 'll'，并更新 PATH 包含 uv 安装工具

```
+ alias ll='ls -alh'
+ export PATH="$PATH:$HOME/.local/bin:$PATH"
```
</div>

## SSH 配置

<div class="chat-transcript" markdown="1">
$ aider ~/.ssh/config

已将 config 添加到对话

#### 使用 bastion.example.com 作为跳板机创建 'my-server' 主机配置

```
+ Host my-server
+     HostName 192.168.1.100
+     User deploy
+     Port 2222
+     IdentityFile ~/.ssh/deploy_key
+     ProxyJump bastion.example.com
```
</div>

## Docker 配置

<div class="chat-transcript" markdown="1">
$ aider Dockerfile docker-compose.yml

已将 Dockerfile 和 docker-compose.yml 添加到对话

#### 设置非 root 用户并启用健康检查

```
+ USER appuser
+ HEALTHCHECK --interval=30s --timeout=3s \
+   CMD curl -f http://localhost:8000/health || exit 1
```

#### 暴露 5432 端口并添加 postgres 数据卷

```
  services:
    postgres:
      image: postgres:15
+     ports:
+       - "5432:5432"
+     volumes:
+       - pgdata:/var/lib/postgresql/data
```
</div>

## Git 配置

<div class="chat-transcript" markdown="1">
$ aider .gitconfig

已将 .gitconfig 添加到对话

#### 设置默认推送当前分支并启用彩色界面

```
+ [push]
+     default = current
+ [color]
+     ui = auto
```
</div>

## 系统配置
<div class="chat-transcript" markdown="1">
$ aider /etc/hosts  # 可能需要 sudo

已将 hosts 添加到对话

#### 通过指向 127.0.0.1 来屏蔽跟踪域名

```
+ 127.0.0.1   ads.example.com
+ 127.0.0.1   track.analytics.co
```
</div>


## 编辑器配置
<div class="chat-transcript" markdown="1">
$ aider .vimrc

已将 .vimrc 添加到对话

#### 启用行号并为 Python 设置 4 空格缩进

```
+ set number
+ autocmd FileType python set tabstop=4 shiftwidth=4 expandtab
```
</div>

## VSCode 配置
<div class="chat-transcript" markdown="1">
$ aider settings.json

已将 settings.json 添加到对话

#### 启用保存时自动格式化并设置默认格式化工具

```
+ "editor.formatOnSave": true,
+ "editor.defaultFormatter": "esbenp.prettier-vscode"
```
</div>

## Markdown 文档
<div class="chat-transcript" markdown="1">
$ aider README.md

已将 README.md 添加到对话


#### 添加包含 brew 和 pip 安装选项的安装章节

```
+ ## 安装
+ ```
+ # Homebrew
+ brew install cool-app-10k
+ 
+ # PyPI
+ pipx install cool-app-10k
+ ```
```
</div>

## XML 配置
<div class="chat-transcript" markdown="1">
$ aider pom.xml

已将 pom.xml 添加到对话

#### 添加测试范围的 JUnit 5 依赖

```
+ <dependency>
+     <groupId>org.junit.jupiter</groupId>
+     <artifactId>junit-jupiter-api</artifactId>
+     <version>5.9.2</version>
+     <scope>test</scope>
+ </dependency>
```
</div>



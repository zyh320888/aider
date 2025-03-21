---
parent: 配置
nav_order: 15
description: 如何使用yaml配置文件配置aider。
---

# YAML配置文件

aider的大多数选项都可以在`.aider.conf.yml`文件中设置。
Aider会在以下位置查找该文件：

- 您的主目录。
- 您的git仓库的根目录。
- 当前目录。

如果上述文件存在，它们将按照该顺序加载。最后加载的文件将优先生效。

您也可以指定`--config <文件名>`参数，这将只加载一个配置文件。

{% include keys.md %}

## 关于列表的说明

值列表可以指定为项目符号列表：

```
read:
  - CONVENTIONS.md
  - anotherfile.txt
  - thirdfile.py
```

或者列表可以使用逗号和方括号指定：

```
read: [CONVENTIONS.md, anotherfile.txt, thirdfile.py]
```

## YAML配置文件示例

以下是YAML配置文件的示例，您也可以
[从GitHub下载](https://github.com/Aider-AI/aider/blob/main/aider/website/assets/sample.aider.conf.yml)。

<!--[[[cog
from aider.args import get_sample_yaml
from pathlib import Path
text=get_sample_yaml()
Path("aider/website/assets/sample.aider.conf.yml").write_text(text)
cog.outl("```")
cog.out(text)
cog.outl("```")
]]]-->
```
##########################################################
# 示例 .aider.conf.yml
# 此文件列出了*所有*有效的配置项。
# 放置在您的家目录，或者您的git仓库的根目录。
##########################################################

# 注意：您只能将OpenAI和Anthropic API密钥放在yaml
# 配置文件中。所有API的密钥都可以存储在.env文件中
# https://aider.chat/docs/config/dotenv.html

##########
# 选项：

## 显示此帮助信息并退出
#help: xxx

#############
# 主模型：

## 指定用于主聊天的模型
#model: xxx

## 使用claude-3-opus-20240229模型进行主聊天
#opus: false

## 使用claude-3-5-sonnet-20241022模型进行主聊天
#sonnet: false

## 使用claude-3-5-haiku-20241022模型进行主聊天
#haiku: false

## 使用gpt-4-0613模型进行主聊天
#4: false

## 使用gpt-4o模型进行主聊天
#4o: false

## 使用gpt-4o-mini模型进行主聊天
#mini: false

## 使用gpt-4-1106-preview模型进行主聊天
#4-turbo: false

## 使用gpt-3.5-turbo模型进行主聊天
#35turbo: false

## 使用deepseek/deepseek-chat模型进行主聊天
#deepseek: false

## 使用o1-mini模型进行主聊天
#o1-mini: false

## 使用o1-preview模型进行主聊天
#o1-preview: false

########################
# API密钥和设置：

## 指定OpenAI API密钥
#openai-api-key: xxx

## 指定Anthropic API密钥
#anthropic-api-key: xxx

## 指定api基础url
#openai-api-base: xxx

## (已弃用，使用--set-env OPENAI_API_TYPE=<值>)
#openai-api-type: xxx

## (已弃用，使用--set-env OPENAI_API_VERSION=<值>)
#openai-api-version: xxx

## (已弃用，使用--set-env OPENAI_API_DEPLOYMENT_ID=<值>)
#openai-api-deployment-id: xxx

## (已弃用，使用--set-env OPENAI_ORGANIZATION=<值>)
#openai-organization-id: xxx

## 设置环境变量（用于控制API设置，可多次使用）
#set-env: xxx
## 指定多个值的方式：
#set-env:
#  - xxx
#  - yyy
#  - zzz

## 为提供者设置API密钥（例如：--api-key provider=<key>设置PROVIDER_API_KEY=<key>）
#api-key: xxx
## 指定多个值的方式：
#api-key:
#  - xxx
#  - yyy
#  - zzz

#################
# 模型设置：

## 列出与（部分）MODEL名称匹配的已知模型
#list-models: xxx

## 为未知模型指定带有aider模型设置的文件
#model-settings-file: .aider.model.settings.yml

## 为未知模型指定带有上下文窗口和成本的文件
#model-metadata-file: .aider.model.metadata.json

## 添加模型别名（可多次使用）
#alias: xxx
## 指定多个值的方式：
#alias:
#  - xxx
#  - yyy
#  - zzz

## 设置reasoning_effort API参数（默认：未设置）
#reasoning-effort: xxx

## 连接到模型时验证SSL证书（默认：True）
#verify-ssl: true

## API调用超时秒数（默认：None）
#timeout: xxx

## 指定LLM应使用的编辑格式（默认取决于模型）
#edit-format: xxx

## 为主聊天使用architect编辑格式
#architect: false

## 指定用于提交消息和聊天历史摘要的模型（默认取决于--model）
#weak-model: xxx

## 指定用于编辑任务的模型（默认取决于--model）
#editor-model: xxx

## 指定编辑器模型的编辑格式（默认：取决于编辑器模型）
#editor-edit-format: xxx

## 仅使用具有可用元数据的模型（默认：True）
#show-model-warnings: true

## 聊天历史的软标记限制，达到后开始摘要。如果未指定，默认为模型的max_chat_history_tokens。
#max-chat-history-tokens: xxx

#################
# 缓存设置：

## 启用提示缓存（默认：False）
#cache-prompts: false

## 以5分钟间隔ping的次数，以保持提示缓存活跃（默认：0）
#cache-keepalive-pings: false

###################
# 仓库映射设置：

## 建议用于仓库映射的标记数，使用0禁用
#map-tokens: xxx

## 控制仓库映射刷新的频率。选项：auto, always, files, manual（默认：auto）
#map-refresh: auto

## 未指定文件时的映射标记乘数（默认：2）
#map-multiplier-no-files: true

################
# 历史文件：

## 指定聊天输入历史文件（默认：.aider.input.history）
#input-history-file: .aider.input.history

## 指定聊天历史文件（默认：.aider.chat.history.md）
#chat-history-file: .aider.chat.history.md

## 恢复之前的聊天历史消息（默认：False）
#restore-chat-history: false

## 将与LLM的对话记录到此文件中（例如，.aider.llm.history）
#llm-history-file: xxx

##################
# 输出设置：

## 使用适合深色终端背景的颜色（默认：False）
#dark-mode: false

## 使用适合浅色终端背景的颜色（默认：False）
#light-mode: false

## 启用/禁用漂亮的彩色输出（默认：True）
#pretty: true

## 启用/禁用流式响应（默认：True）
#stream: true

## 设置用户输入的颜色（默认：#00cc00）
#user-input-color: #00cc00

## 设置工具输出的颜色（默认：None）
#tool-output-color: xxx

## 设置工具错误消息的颜色（默认：#FF2222）
#tool-error-color: #FF2222

## 设置工具警告消息的颜色（默认：#FFA500）
#tool-warning-color: #FFA500

## 设置助手输出的颜色（默认：#0088ff）
#assistant-output-color: #0088ff

## 设置补全菜单的颜色（默认：终端的默认文本颜色）
#completion-menu-color: xxx

## 设置补全菜单的背景颜色（默认：终端的默认背景颜色）
#completion-menu-bg-color: xxx

## 设置补全菜单中当前项目的颜色（默认：终端的默认背景颜色）
#completion-menu-current-color: xxx

## 设置补全菜单中当前项目的背景颜色（默认：终端的默认文本颜色）
#completion-menu-current-bg-color: xxx

## 设置markdown代码主题（默认：default，其他选项包括monokai, solarized-dark, solarized-light或Pygments内置样式，查看https://pygments.org/styles获取可用主题）
#code-theme: default

## 提交更改时显示差异（默认：False）
#show-diffs: false

###############
# Git设置：

## 启用/禁用查找git仓库（默认：True）
#git: true

## 启用/禁用将.aider*添加到.gitignore（默认：True）
#gitignore: true

## 指定aider忽略文件（默认：git根目录中的.aiderignore）
#aiderignore: .aiderignore

## 仅考虑git仓库当前子树中的文件
#subtree-only: false

## 启用/禁用LLM更改的自动提交（默认：True）
#auto-commits: true

## 启用/禁用当仓库发现有未提交更改时的提交（默认：True）
#dirty-commits: true

## 在git作者名称中归属aider代码更改（默认：True）
#attribute-author: true

## 在git提交者名称中归属aider提交（默认：True）
#attribute-committer: true

## 如果aider创作了更改，则在提交消息前加上'aider: '（默认：False）
#attribute-commit-message-author: false

## 在所有提交消息前加上'aider: '（默认：False）
#attribute-commit-message-committer: false

## 用合适的提交消息提交所有待处理的更改，然后退出
#commit: false

## 指定生成提交消息的自定义提示
#commit-prompt: xxx

## 执行不修改文件的试运行（默认：False）
#dry-run: false

## 跳过对git仓库的健全性检查（默认：False）
#skip-sanity-check-repo: false

## 启用/禁用监视文件以查找ai编码注释（默认：False）
#watch-files: false

########################
# 修复和提交：

## 整理并修复提供的文件，如果没有提供则修复有未提交更改的文件
#lint: false

## 为不同语言指定运行的lint命令，例如："python: flake8 --select=..."（可多次使用）
#lint-cmd: xxx
## 指定多个值的方式：
#lint-cmd:
#  - xxx
#  - yyy
#  - zzz

## 启用/禁用更改后自动整理（默认：True）
#auto-lint: true

## 指定运行测试的命令
#test-cmd: xxx

## 启用/禁用更改后自动测试（默认：False）
#auto-test: false

## 运行测试，修复发现的问题，然后退出
#test: false

############
# 分析：

## 为当前会话启用/禁用分析（默认：随机）
#analytics: xxx

## 指定记录分析事件的文件
#analytics-log: xxx

## 永久禁用分析
#analytics-disable: false

############
# 升级：

## 检查更新并在退出代码中返回状态
#just-check-update: false

## 启动时检查新的aider版本
#check-update: true

## 在新版本首次运行时显示发布说明（默认：None，询问用户）
#show-release-notes: xxx

## 从主分支安装最新版本
#install-main-branch: false

## 从PyPI升级aider到最新版本
#upgrade: false

## 显示版本号并退出
#version: xxx

########
# 模式：

## 指定发送给LLM的单个消息，处理回复然后退出（禁用聊天模式）
#message: xxx

## 指定包含要发送给LLM的消息的文件，处理回复然后退出（禁用聊天模式）
#message-file: xxx

## 在浏览器中运行aider（默认：False）
#gui: false

## 启用aider和Web UI之间的聊天自动复制/粘贴（默认：False）
#copy-paste: false

## 应用给定文件中的更改，而不是运行聊天（调试）
#apply: xxx

## 应用剪贴板内容作为使用主模型编辑器格式的编辑
#apply-clipboard-edits: false

## 执行所有启动活动，然后在接受用户输入前退出（调试）
#exit: false

## 打印仓库映射并退出（调试）
#show-repo-map: false

## 打印系统提示并退出（调试）
#show-prompts: false

#################
# 语音设置：

## 语音录制的音频格式（默认：wav）。webm和mp3需要ffmpeg
#voice-format: wav

## 使用ISO 639-1代码指定语音的语言（默认：auto）
#voice-language: en

## 指定语音录制的输入设备名称
#voice-input-device: xxx

#################
# 其他设置：

## 指定要编辑的文件（可多次使用）
#file: xxx
## 指定多个值的方式：
#file:
#  - xxx
#  - yyy
#  - zzz

## 指定只读文件（可多次使用）
#read: xxx
## 指定多个值的方式：
#read:
#  - xxx
#  - yyy
#  - zzz

## 在终端中使用VI编辑模式（默认：False）
#vim: false

## 指定在聊天中使用的语言（默认：None，使用系统设置）
#chat-language: xxx

## 对每个确认始终回答yes
#yes-always: false

## 启用详细输出
#verbose: false

## 在启动时加载并执行来自文件的/commands
#load: xxx

## 指定输入和输出的编码（默认：utf-8）
#encoding: utf-8

## 写入文件时使用的行尾（默认：platform）
#line-endings: platform

## 指定配置文件（默认：在git根目录、当前工作目录或主目录中查找.aider.conf.yml）
#config: xxx

## 指定要加载的.env文件（默认：git根目录中的.env）
#env-file: .env

## 启用/禁用建议shell命令（默认：True）
#suggest-shell-commands: true

## 启用/禁用带有历史和自动完成的高级输入（默认：True）
#fancy-input: true

## 启用/禁用多行输入模式，使用Meta-Enter提交（默认：False）
#multiline: false

## 启用/禁用检测并提供将URL添加到聊天的功能（默认：True）
#detect-urls: true

## 指定用于/editor命令的编辑器
#editor: xxx

## 安装tree_sitter_language_pack（实验性）
#install-tree-sitter-language-pack: false
```
<!--[[[end]]]-->

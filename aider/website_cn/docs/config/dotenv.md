---
parent: Configuration
nav_order: 20
description: 使用.env文件存储aider的LLM API密钥。
---

# 使用.env配置

您可以使用`.env`文件存储API密钥和其他与aider一起使用的模型设置。
您还可以在`.env`文件中设置许多常规aider选项。

Aider将在以下位置查找`.env`文件：

- 您的主目录。
- 您的git仓库根目录。
- 当前目录。
- 使用`--env-file <filename>`参数指定的位置。

如果上述文件存在，它们将按该顺序加载。最后加载的文件将优先。

{% include keys.md %}

## .env文件示例

以下是一个示例`.env`文件，您也可以
[从GitHub下载](https://github.com/Aider-AI/aider/blob/main/aider/website/assets/sample.env)。

<!--[[[cog
from aider.args import get_sample_dotenv
from pathlib import Path
text=get_sample_dotenv()
Path("aider/website/assets/sample.env").write_text(text)
cog.outl("```")
cog.out(text)
cog.outl("```")
]]]-->
```
##########################################################
# aider .env文件示例
# 放置在git仓库的根目录。
# 或使用`aider --env <fname>`指定。
##########################################################

#################
# LLM参数：
#
# 包括xxx_API_KEY参数和LLM需要的其他参数。
# 详情见https://aider.chat/docs/llms.html。

## OpenAI
#OPENAI_API_KEY=

## Anthropic
#ANTHROPIC_API_KEY=

##...

#############
# 主要模型：

## 指定用于主聊天的模型
#AIDER_MODEL=

## 使用claude-3-opus-20240229模型进行主聊天
#AIDER_OPUS=

## 使用claude-3-5-sonnet-20241022模型进行主聊天
#AIDER_SONNET=

## 使用claude-3-5-haiku-20241022模型进行主聊天
#AIDER_HAIKU=

## 使用gpt-4-0613模型进行主聊天
#AIDER_4=

## 使用gpt-4o模型进行主聊天
#AIDER_4O=

## 使用gpt-4o-mini模型进行主聊天
#AIDER_MINI=

## 使用gpt-4-1106-preview模型进行主聊天
#AIDER_4_TURBO=

## 使用gpt-3.5-turbo模型进行主聊天
#AIDER_35TURBO=

## 使用deepseek/deepseek-chat模型进行主聊天
#AIDER_DEEPSEEK=

## 使用o1-mini模型进行主聊天
#AIDER_O1_MINI=

## 使用o1-preview模型进行主聊天
#AIDER_O1_PREVIEW=

########################
# API密钥和设置：

## 指定OpenAI API密钥
#AIDER_OPENAI_API_KEY=

## 指定Anthropic API密钥
#AIDER_ANTHROPIC_API_KEY=

## 指定api基础url
#AIDER_OPENAI_API_BASE=

## (已弃用，使用--set-env OPENAI_API_TYPE=<value>)
#AIDER_OPENAI_API_TYPE=

## (已弃用，使用--set-env OPENAI_API_VERSION=<value>)
#AIDER_OPENAI_API_VERSION=

## (已弃用，使用--set-env OPENAI_API_DEPLOYMENT_ID=<value>)
#AIDER_OPENAI_API_DEPLOYMENT_ID=

## (已弃用，使用--set-env OPENAI_ORGANIZATION=<value>)
#AIDER_OPENAI_ORGANIZATION_ID=

## 设置环境变量（控制API设置，可多次使用）
#AIDER_SET_ENV=

## 为提供商设置API密钥（例如：--api-key provider=<key>设置PROVIDER_API_KEY=<key>）
#AIDER_API_KEY=

#################
# 模型设置：

## 列出与（部分）MODEL名称匹配的已知模型
#AIDER_LIST_MODELS=

## 指定带有未知模型的aider模型设置的文件
#AIDER_MODEL_SETTINGS_FILE=.aider.model.settings.yml

## 指定带有未知模型的上下文窗口和成本的文件
#AIDER_MODEL_METADATA_FILE=.aider.model.metadata.json

## 添加模型别名（可多次使用）
#AIDER_ALIAS=

## 设置reasoning_effort API参数（默认：未设置）
#AIDER_REASONING_EFFORT=

## 连接模型时验证SSL证书（默认：True）
#AIDER_VERIFY_SSL=true

## API调用的超时时间（秒）（默认：None）
#AIDER_TIMEOUT=

## 指定LLM应使用的编辑格式（默认取决于模型）
#AIDER_EDIT_FORMAT=

## 为主聊天使用architect编辑格式
#AIDER_ARCHITECT=

## 指定用于提交消息和聊天历史摘要的模型（默认取决于--model）
#AIDER_WEAK_MODEL=

## 指定用于编辑器任务的模型（默认取决于--model）
#AIDER_EDITOR_MODEL=

## 指定编辑器模型的编辑格式（默认：取决于编辑器模型）
#AIDER_EDITOR_EDIT_FORMAT=

## 仅使用具有可用元数据的模型（默认：True）
#AIDER_SHOW_MODEL_WARNINGS=true

## 聊天历史的软令牌限制，超过此限制后开始摘要。如果未指定，默认为模型的max_chat_history_tokens。
#AIDER_MAX_CHAT_HISTORY_TOKENS=

#################
# 缓存设置：

## 启用提示缓存（默认：False）
#AIDER_CACHE_PROMPTS=false

## 以5分钟间隔ping以保持提示缓存热度的次数（默认：0）
#AIDER_CACHE_KEEPALIVE_PINGS=false

###################
# 仓库映射设置：

## 建议用于仓库映射的令牌数，使用0禁用
#AIDER_MAP_TOKENS=

## 控制仓库映射刷新频率。选项：auto, always, files, manual（默认：auto）
#AIDER_MAP_REFRESH=auto

## 未指定文件时的映射令牌乘数（默认：2）
#AIDER_MAP_MULTIPLIER_NO_FILES=true

################
# 历史文件：

## 指定聊天输入历史文件（默认：.aider.input.history）
#AIDER_INPUT_HISTORY_FILE=.aider.input.history

## 指定聊天历史文件（默认：.aider.chat.history.md）
#AIDER_CHAT_HISTORY_FILE=.aider.chat.history.md

## 恢复以前的聊天历史消息（默认：False）
#AIDER_RESTORE_CHAT_HISTORY=false

## 将与LLM的对话记录到此文件（例如，.aider.llm.history）
#AIDER_LLM_HISTORY_FILE=

##################
# Output settings:

## 使用适合深色终端背景的颜色（默认：False）
#AIDER_DARK_MODE=false

## 使用适合浅色终端背景的颜色（默认：False）
#AIDER_LIGHT_MODE=false

## 启用/禁用美观、彩色输出（默认：True）
#AIDER_PRETTY=true

## 启用/禁用流式响应（默认：True）
#AIDER_STREAM=true

## 设置用户输入的颜色（默认：#00cc00）
#AIDER_USER_INPUT_COLOR=#00cc00

## 设置工具输出的颜色（默认：None）
#AIDER_TOOL_OUTPUT_COLOR=

## 设置工具错误消息的颜色（默认：#FF2222）
#AIDER_TOOL_ERROR_COLOR=#FF2222

## 设置工具警告消息的颜色（默认：#FFA500）
#AIDER_TOOL_WARNING_COLOR=#FFA500

## 设置助手输出的颜色（默认：#0088ff）
#AIDER_ASSISTANT_OUTPUT_COLOR=#0088ff

## 设置补全菜单的颜色（默认：终端的默认文本颜色）
#AIDER_COMPLETION_MENU_COLOR=

## 设置补全菜单的背景颜色（默认：终端的默认背景颜色）
#AIDER_COMPLETION_MENU_BG_COLOR=

## 设置补全菜单中当前项目的颜色（默认：终端的默认背景颜色）
#AIDER_COMPLETION_MENU_CURRENT_COLOR=

## 设置补全菜单中当前项目的背景颜色（默认：终端的默认文本颜色）
#AIDER_COMPLETION_MENU_CURRENT_BG_COLOR=

## 设置markdown代码主题（默认：default，其他选项包括monokai、solarized-dark、solarized-light或Pygments内置样式，查看https://pygments.org/styles了解可用主题）
#AIDER_CODE_THEME=default

## 提交更改时显示差异（默认：False）
#AIDER_SHOW_DIFFS=false

###############
# Git settings:

## 启用/禁用查找git仓库（默认：True）
#AIDER_GIT=true

## 启用/禁用将.aider*添加到.gitignore（默认：True）
#AIDER_GITIGNORE=true

## 指定aider忽略文件（默认：git根目录中的.aiderignore）
#AIDER_AIDERIGNORE=.aiderignore

## 仅考虑git仓库当前子树中的文件
#AIDER_SUBTREE_ONLY=false

## 启用/禁用LLM更改的自动提交（默认：True）
#AIDER_AUTO_COMMITS=true

## 启用/禁用在发现仓库脏时进行提交（默认：True）
#AIDER_DIRTY_COMMITS=true

## 在git作者名称中标注aider代码更改（默认：True）
#AIDER_ATTRIBUTE_AUTHOR=true

## 在git提交者名称中标注aider提交（默认：True）
#AIDER_ATTRIBUTE_COMMITTER=true

## 如果aider编写了更改，则在提交消息前加上'aider: '（默认：False）
#AIDER_ATTRIBUTE_COMMIT_MESSAGE_AUTHOR=false

## 在所有提交消息前加上'aider: '（默认：False）
#AIDER_ATTRIBUTE_COMMIT_MESSAGE_COMMITTER=false

## 使用合适的提交消息提交所有待处理的更改，然后退出
#AIDER_COMMIT=false

## 指定生成提交消息的自定义提示
#AIDER_COMMIT_PROMPT=

## 执行无修改文件的演示运行（默认：False）
#AIDER_DRY_RUN=false

## 跳过git仓库的健全性检查（默认：False）
#AIDER_SKIP_SANITY_CHECK_REPO=false

## 启用/禁用监视文件中的ai编码注释（默认：False）
#AIDER_WATCH_FILES=false

########################
# Fixing and committing:

## 对提供的文件或脏文件（如果未提供）进行lint和修复
#AIDER_LINT=false

## 为不同语言指定lint命令，例如："python: flake8 --select=..."（可多次使用）
#AIDER_LINT_CMD=

## 启用/禁用更改后自动lint（默认：True）
#AIDER_AUTO_LINT=true

## 指定运行测试的命令
#AIDER_TEST_CMD=

## 启用/禁用更改后自动测试（默认：False）
#AIDER_AUTO_TEST=false

## 运行测试，修复发现的问题然后退出
#AIDER_TEST=false

############
# Analytics:

## 为当前会话启用/禁用分析（默认：随机）
#AIDER_ANALYTICS=

## 指定记录分析事件的文件
#AIDER_ANALYTICS_LOG=

## 永久禁用分析
#AIDER_ANALYTICS_DISABLE=false

############
# Upgrading:

## 检查更新并在退出代码中返回状态
#AIDER_JUST_CHECK_UPDATE=false

## 启动时检查新的aider版本
#AIDER_CHECK_UPDATE=true

## 在新版本首次运行时显示发布说明（默认：None，询问用户）
#AIDER_SHOW_RELEASE_NOTES=

## 从主分支安装最新版本
#AIDER_INSTALL_MAIN_BRANCH=false

## 从PyPI升级aider到最新版本
#AIDER_UPGRADE=false

########
# Modes:

## 指定要发送给LLM的单个消息，处理回复然后退出（禁用聊天模式）
#AIDER_MESSAGE=

## 指定包含要发送给LLM的消息的文件，处理回复，然后退出（禁用聊天模式）
#AIDER_MESSAGE_FILE=

## 在浏览器中运行aider（默认：False）
#AIDER_GUI=false

## 启用aider和Web UI之间的自动复制/粘贴聊天（默认：False）
#AIDER_COPY_PASTE=false

## 应用给定文件中的更改，而不是运行聊天（调试）
#AIDER_APPLY=

## 应用剪贴板内容作为使用主模型编辑器格式的编辑
#AIDER_APPLY_CLIPBOARD_EDITS=false

## 执行所有启动活动，然后在接受用户输入前退出（调试）
#AIDER_EXIT=false

## 打印仓库映射并退出（调试）
#AIDER_SHOW_REPO_MAP=false

## 打印系统提示并退出（调试）
#AIDER_SHOW_PROMPTS=false

#################
# Voice settings:

## 语音录制的音频格式（默认：wav）。webm和mp3需要ffmpeg
#AIDER_VOICE_FORMAT=wav

## 使用ISO 639-1代码指定语音语言（默认：auto）
#AIDER_VOICE_LANGUAGE=en

## 指定语音录制的输入设备名称
#AIDER_VOICE_INPUT_DEVICE=

#################
# Other settings:

## 指定要编辑的文件（可多次使用）
#AIDER_FILE=

## 指定只读文件（可多次使用）
#AIDER_READ=

## 在终端中使用VI编辑模式（默认：False）
#AIDER_VIM=false

## 指定在聊天中使用的语言（默认：None，使用系统设置）
#AIDER_CHAT_LANGUAGE=

## 对每个确认始终回答是
#AIDER_YES_ALWAYS=

## 启用详细输出
#AIDER_VERBOSE=false

## 在启动时从文件加载并执行/命令
#AIDER_LOAD=

## 指定输入和输出的编码（默认：utf-8）
#AIDER_ENCODING=utf-8

## 写入文件时使用的行尾（默认：platform）
#AIDER_LINE_ENDINGS=platform

## 指定要加载的.env文件（默认：git根目录中的.env）
#AIDER_ENV_FILE=.env

## 启用/禁用建议shell命令（默认：True）
#AIDER_SUGGEST_SHELL_COMMANDS=true

## 启用/禁用带有历史记录和自动完成的花式输入（默认：True）
#AIDER_FANCY_INPUT=true

## 启用/禁用多行输入模式，使用Meta-Enter提交（默认：False）
#AIDER_MULTILINE=false

## 启用/禁用检测并提供将URL添加到聊天的选项（默认：True）
#AIDER_DETECT_URLS=true

## 指定/editor命令使用的编辑器
#AIDER_EDITOR=

## 安装tree_sitter_language_pack（实验性）
#AIDER_INSTALL_TREE_SITTER_LANGUAGE_PACK=false
```
<!--[[[end]]]-->

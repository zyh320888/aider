---
parent: Configuration
nav_order: 10
description: 关于aider所有设置的详细信息。
---

# 选项参考
{: .no_toc }

你可以使用 `aider --help` 查看所有可用选项，
或在下面查看它们。

- TOC
{:toc}

{% include keys.md %}

## 使用摘要

<!--[[[cog
from aider.args import get_md_help
cog.out(get_md_help())
]]]-->
```
usage: aider [-h] [--model] [--opus] [--sonnet] [--haiku] [--4]
             [--4o] [--mini] [--4-turbo] [--35turbo] [--deepseek]
             [--o1-mini] [--o1-preview] [--openai-api-key]
             [--anthropic-api-key] [--openai-api-base]
             [--openai-api-type] [--openai-api-version]
             [--openai-api-deployment-id] [--openai-organization-id]
             [--set-env] [--api-key] [--list-models]
             [--model-settings-file] [--model-metadata-file]
             [--alias] [--reasoning-effort]
             [--verify-ssl | --no-verify-ssl] [--timeout]
             [--edit-format] [--architect] [--weak-model]
             [--editor-model] [--editor-edit-format]
             [--show-model-warnings | --no-show-model-warnings]
             [--max-chat-history-tokens]
             [--cache-prompts | --no-cache-prompts]
             [--cache-keepalive-pings] [--map-tokens]
             [--map-refresh] [--map-multiplier-no-files]
             [--input-history-file] [--chat-history-file]
             [--restore-chat-history | --no-restore-chat-history]
             [--llm-history-file] [--dark-mode] [--light-mode]
             [--pretty | --no-pretty] [--stream | --no-stream]
             [--user-input-color] [--tool-output-color]
             [--tool-error-color] [--tool-warning-color]
             [--assistant-output-color] [--completion-menu-color]
             [--completion-menu-bg-color]
             [--completion-menu-current-color]
             [--completion-menu-current-bg-color] [--code-theme]
             [--show-diffs] [--git | --no-git]
             [--gitignore | --no-gitignore] [--aiderignore]
             [--subtree-only] [--auto-commits | --no-auto-commits]
             [--dirty-commits | --no-dirty-commits]
             [--attribute-author | --no-attribute-author]
             [--attribute-committer | --no-attribute-committer]
             [--attribute-commit-message-author | --no-attribute-commit-message-author]
             [--attribute-commit-message-committer | --no-attribute-commit-message-committer]
             [--commit] [--commit-prompt] [--dry-run | --no-dry-run]
             [--skip-sanity-check-repo]
             [--watch-files | --no-watch-files] [--lint]
             [--lint-cmd] [--auto-lint | --no-auto-lint]
             [--test-cmd] [--auto-test | --no-auto-test] [--test]
             [--analytics | --no-analytics] [--analytics-log]
             [--analytics-disable] [--just-check-update]
             [--check-update | --no-check-update]
             [--show-release-notes | --no-show-release-notes]
             [--install-main-branch] [--upgrade] [--version]
             [--message] [--message-file]
             [--gui | --no-gui | --browser | --no-browser]
             [--copy-paste | --no-copy-paste] [--apply]
             [--apply-clipboard-edits] [--exit] [--show-repo-map]
             [--show-prompts] [--voice-format] [--voice-language]
             [--voice-input-device] [--file] [--read] [--vim]
             [--chat-language] [--yes-always] [-v] [--load]
             [--encoding] [--line-endings] [-c] [--env-file]
             [--suggest-shell-commands | --no-suggest-shell-commands]
             [--fancy-input | --no-fancy-input]
             [--multiline | --no-multiline]
             [--detect-urls | --no-detect-urls] [--editor]
             [--install-tree-sitter-language-pack]

```

## 选项：

### `--help`
显示帮助信息并退出  
别名：
  - `-h`
  - `--help`

## 主要模型：

### `--model MODEL`
指定用于主聊天的模型  
环境变量：`AIDER_MODEL`  

### `--opus`
使用 claude-3-opus-20240229 模型进行主聊天  
环境变量：`AIDER_OPUS`  

### `--sonnet`
使用 claude-3-5-sonnet-20241022 模型进行主聊天  
环境变量：`AIDER_SONNET`  

### `--haiku`
使用 claude-3-5-haiku-20241022 模型进行主聊天  
环境变量：`AIDER_HAIKU`  

### `--4`
使用 gpt-4-0613 模型进行主聊天  
环境变量：`AIDER_4`  
别名：
  - `--4`
  - `-4`

### `--4o`
使用 gpt-4o 模型进行主聊天  
环境变量：`AIDER_4O`  

### `--mini`
使用 gpt-4o-mini 模型进行主聊天  
环境变量：`AIDER_MINI`  

### `--4-turbo`
使用 gpt-4-1106-preview 模型进行主聊天  
环境变量：`AIDER_4_TURBO`  

### `--35turbo`
使用 gpt-3.5-turbo 模型进行主聊天  
环境变量：`AIDER_35TURBO`  
别名：
  - `--35turbo`
  - `--35-turbo`
  - `--3`
  - `-3`

### `--deepseek`
使用 deepseek/deepseek-chat 模型进行主聊天  
环境变量：`AIDER_DEEPSEEK`  

### `--o1-mini`
使用 o1-mini 模型进行主聊天  
环境变量：`AIDER_O1_MINI`  

### `--o1-preview`
使用 o1-preview 模型进行主聊天  
环境变量：`AIDER_O1_PREVIEW`  

## API 密钥和设置：

### `--openai-api-key VALUE`
指定 OpenAI API 密钥  
环境变量：`AIDER_OPENAI_API_KEY`  

### `--anthropic-api-key VALUE`
指定 Anthropic API 密钥  
环境变量：`AIDER_ANTHROPIC_API_KEY`  

### `--openai-api-base VALUE`
指定 API 基础 URL  
环境变量：`AIDER_OPENAI_API_BASE`  

### `--openai-api-type VALUE`
（已弃用，请使用 --set-env OPENAI_API_TYPE=<value>）  
环境变量：`AIDER_OPENAI_API_TYPE`  

### `--openai-api-version VALUE`
（已弃用，请使用 --set-env OPENAI_API_VERSION=<value>）  
环境变量：`AIDER_OPENAI_API_VERSION`  

### `--openai-api-deployment-id VALUE`
（已弃用，请使用 --set-env OPENAI_API_DEPLOYMENT_ID=<value>）  
环境变量：`AIDER_OPENAI_API_DEPLOYMENT_ID`  

### `--openai-organization-id VALUE`
（已弃用，请使用 --set-env OPENAI_ORGANIZATION=<value>）  
环境变量：`AIDER_OPENAI_ORGANIZATION_ID`  

### `--set-env ENV_VAR_NAME=value`
设置环境变量（用于控制 API 设置，可多次使用）  
默认值：[]  
环境变量：`AIDER_SET_ENV`  

### `--api-key PROVIDER=KEY`
为提供商设置 API 密钥（例如：--api-key provider=<key> 设置 PROVIDER_API_KEY=<key>）  
默认值：[]  
环境变量：`AIDER_API_KEY`  

## 模型设置：

### `--list-models MODEL`
列出与（部分）MODEL 名称匹配的已知模型  
环境变量：`AIDER_LIST_MODELS`  
别名：
  - `--list-models MODEL`
  - `--models MODEL`

### `--model-settings-file MODEL_SETTINGS_FILE`
指定包含未知模型的 aider 模型设置的文件  
默认值：.aider.model.settings.yml  
环境变量：`AIDER_MODEL_SETTINGS_FILE`  

### `--model-metadata-file MODEL_METADATA_FILE`
指定包含未知模型的上下文窗口和成本的文件  
默认值：.aider.model.metadata.json  
环境变量：`AIDER_MODEL_METADATA_FILE`  

### `--alias ALIAS:MODEL`
添加模型别名（可多次使用）  
环境变量：`AIDER_ALIAS`  

### `--reasoning-effort VALUE`
设置 reasoning_effort API 参数（默认：未设置）  
环境变量：`AIDER_REASONING_EFFORT`  

### `--verify-ssl`
连接模型时验证 SSL 证书（默认：True）  
默认值：True  
环境变量：`AIDER_VERIFY_SSL`  
别名：
  - `--verify-ssl`
  - `--no-verify-ssl`

### `--timeout VALUE`
API 调用的超时时间（秒）（默认：None）  
环境变量：`AIDER_TIMEOUT`  

### `--edit-format EDIT_FORMAT`
指定 LLM 应使用的编辑格式（默认取决于模型）  
环境变量：`AIDER_EDIT_FORMAT`  
别名：
  - `--edit-format EDIT_FORMAT`
  - `--chat-mode EDIT_FORMAT`

### `--architect`
为主聊天使用 architect 编辑格式  
环境变量：`AIDER_ARCHITECT`  

### `--weak-model WEAK_MODEL`
指定用于提交消息和聊天历史摘要的模型（默认取决于 --model）  
环境变量：`AIDER_WEAK_MODEL`  

### `--editor-model EDITOR_MODEL`
指定用于编辑器任务的模型（默认取决于 --model）  
环境变量：`AIDER_EDITOR_MODEL`  

### `--editor-edit-format EDITOR_EDIT_FORMAT`
指定编辑器模型的编辑格式（默认取决于编辑器模型）  
环境变量：`AIDER_EDITOR_EDIT_FORMAT`  

### `--show-model-warnings`
仅使用具有可用元数据的模型（默认：True）  
默认值：True  
环境变量：`AIDER_SHOW_MODEL_WARNINGS`  
别名：
  - `--show-model-warnings`
  - `--no-show-model-warnings`

### `--max-chat-history-tokens VALUE`
聊天历史的软令牌限制，超过此限制后开始摘要。如果未指定，默认为模型的 max_chat_history_tokens。  
环境变量：`AIDER_MAX_CHAT_HISTORY_TOKENS`  

## Cache settings:

### `--cache-prompts`
启用提示缓存（默认：False）  
默认值：False  
环境变量：`AIDER_CACHE_PROMPTS`  
别名：
  - `--cache-prompts`
  - `--no-cache-prompts`

### `--cache-keepalive-pings VALUE`
以5分钟间隔ping以保持提示缓存热度的次数（默认：0）  
默认值：0  
环境变量：`AIDER_CACHE_KEEPALIVE_PINGS`  

## Repomap settings:

### `--map-tokens VALUE`
建议用于仓库映射的令牌数，使用0禁用  
环境变量：`AIDER_MAP_TOKENS`  

### `--map-refresh VALUE`
控制仓库映射刷新频率。选项：auto, always, files, manual（默认：auto）  
默认值：auto  
环境变量：`AIDER_MAP_REFRESH`  

### `--map-multiplier-no-files VALUE`
未指定文件时的映射令牌乘数（默认：2）  
默认值：2  
环境变量：`AIDER_MAP_MULTIPLIER_NO_FILES`  

## History Files:

### `--input-history-file INPUT_HISTORY_FILE`
指定聊天输入历史文件（默认：.aider.input.history）  
默认值：.aider.input.history  
环境变量：`AIDER_INPUT_HISTORY_FILE`  

### `--chat-history-file CHAT_HISTORY_FILE`
指定聊天历史文件（默认：.aider.chat.history.md）  
默认值：.aider.chat.history.md  
环境变量：`AIDER_CHAT_HISTORY_FILE`  

### `--restore-chat-history`
恢复之前的聊天历史消息（默认：False）  
默认值：False  
环境变量：`AIDER_RESTORE_CHAT_HISTORY`  
别名：
  - `--restore-chat-history`
  - `--no-restore-chat-history`

### `--llm-history-file LLM_HISTORY_FILE`
将与LLM的对话记录到此文件（例如，.aider.llm.history）  
环境变量：`AIDER_LLM_HISTORY_FILE`  

## Output settings:

### `--dark-mode`
使用适合深色终端背景的颜色（默认：False）  
默认值：False  
环境变量：`AIDER_DARK_MODE`  

### `--light-mode`
使用适合浅色终端背景的颜色（默认：False）  
默认值：False  
环境变量：`AIDER_LIGHT_MODE`  

### `--pretty`
启用/禁用美观、彩色输出（默认：True）  
默认值：True  
环境变量：`AIDER_PRETTY`  
别名：
  - `--pretty`
  - `--no-pretty`

### `--stream`
启用/禁用流式响应（默认：True）  
默认值：True  
环境变量：`AIDER_STREAM`  
别名：
  - `--stream`
  - `--no-stream`

### `--user-input-color VALUE`
设置用户输入的颜色（默认：#00cc00）  
默认值：#00cc00  
环境变量：`AIDER_USER_INPUT_COLOR`  

### `--tool-output-color VALUE`
设置工具输出的颜色（默认：None）  
环境变量：`AIDER_TOOL_OUTPUT_COLOR`  

### `--tool-error-color VALUE`
设置工具错误消息的颜色（默认：#FF2222）  
默认值：#FF2222  
环境变量：`AIDER_TOOL_ERROR_COLOR`  

### `--tool-warning-color VALUE`
设置工具警告消息的颜色（默认：#FFA500）  
默认值：#FFA500  
环境变量：`AIDER_TOOL_WARNING_COLOR`  

### `--assistant-output-color VALUE`
设置助手输出的颜色（默认：#0088ff）  
默认值：#0088ff  
环境变量：`AIDER_ASSISTANT_OUTPUT_COLOR`  

### `--completion-menu-color COLOR`
设置补全菜单的颜色（默认：终端的默认文本颜色）  
环境变量：`AIDER_COMPLETION_MENU_COLOR`  

### `--completion-menu-bg-color COLOR`
设置补全菜单的背景颜色（默认：终端的默认背景颜色）  
环境变量：`AIDER_COMPLETION_MENU_BG_COLOR`  

### `--completion-menu-current-color COLOR`
设置补全菜单中当前项目的颜色（默认：终端的默认背景颜色）  
环境变量：`AIDER_COMPLETION_MENU_CURRENT_COLOR`  

### `--completion-menu-current-bg-color COLOR`
设置补全菜单中当前项目的背景颜色（默认：终端的默认文本颜色）  
环境变量：`AIDER_COMPLETION_MENU_CURRENT_BG_COLOR`  

### `--code-theme VALUE`
设置markdown代码主题（默认：default，其他选项包括monokai、solarized-dark、solarized-light或Pygments内置样式，查看https://pygments.org/styles了解可用主题）  
默认值：default  
环境变量：`AIDER_CODE_THEME`  

### `--show-diffs`
提交更改时显示差异（默认：False）  
默认值：False  
环境变量：`AIDER_SHOW_DIFFS`  

## Git settings:

### `--git`
启用/禁用查找git仓库（默认：True）  
默认值：True  
环境变量：`AIDER_GIT`  
别名：
  - `--git`
  - `--no-git`

### `--gitignore`
启用/禁用将.aider*添加到.gitignore（默认：True）  
默认值：True  
环境变量：`AIDER_GITIGNORE`  
别名：
  - `--gitignore`
  - `--no-gitignore`

### `--aiderignore AIDERIGNORE`
指定aider忽略文件（默认：git根目录中的.aiderignore）  
默认值：.aiderignore  
环境变量：`AIDER_AIDERIGNORE`  

### `--subtree-only`
仅考虑git仓库当前子树中的文件  
默认值：False  
环境变量：`AIDER_SUBTREE_ONLY`  

### `--auto-commits`
启用/禁用LLM更改的自动提交（默认：True）  
默认值：True  
环境变量：`AIDER_AUTO_COMMITS`  
别名：
  - `--auto-commits`
  - `--no-auto-commits`

### `--dirty-commits`
启用/禁用在发现仓库脏时进行提交（默认：True）  
默认值：True  
环境变量：`AIDER_DIRTY_COMMITS`  
别名：
  - `--dirty-commits`
  - `--no-dirty-commits`

### `--attribute-author`
在git作者名称中标注aider代码更改（默认：True）  
默认值：True  
环境变量：`AIDER_ATTRIBUTE_AUTHOR`  
别名：
  - `--attribute-author`
  - `--no-attribute-author`

### `--attribute-committer`
在git提交者名称中标注aider提交（默认：True）  
默认值：True  
环境变量：`AIDER_ATTRIBUTE_COMMITTER`  
别名：
  - `--attribute-committer`
  - `--no-attribute-committer`

### `--attribute-commit-message-author`
如果aider编写了更改，则在提交消息前加上'aider: '（默认：False）  
默认值：False  
环境变量：`AIDER_ATTRIBUTE_COMMIT_MESSAGE_AUTHOR`  
别名：
  - `--attribute-commit-message-author`
  - `--no-attribute-commit-message-author`

### `--attribute-commit-message-committer`
在所有提交消息前加上'aider: '（默认：False）  
默认值：False  
环境变量：`AIDER_ATTRIBUTE_COMMIT_MESSAGE_COMMITTER`  
别名：
  - `--attribute-commit-message-committer`
  - `--no-attribute-commit-message-committer`

### `--commit`
使用合适的提交消息提交所有待处理的更改，然后退出  
默认值：False  
环境变量：`AIDER_COMMIT`  

### `--commit-prompt PROMPT`
指定生成提交消息的自定义提示  
环境变量：`AIDER_COMMIT_PROMPT`  

### `--dry-run`
执行无修改文件的演示运行（默认：False）  
默认值：False  
环境变量：`AIDER_DRY_RUN`  
别名：
  - `--dry-run`
  - `--no-dry-run`

### `--skip-sanity-check-repo`
跳过git仓库的健全性检查（默认：False）  
默认值：False  
环境变量：`AIDER_SKIP_SANITY_CHECK_REPO`  

### `--watch-files`
启用/禁用监视文件中的ai编码注释（默认：False）  
默认值：False  
环境变量：`AIDER_WATCH_FILES`  
别名：
  - `--watch-files`
  - `--no-watch-files`

## Fixing and committing:

### `--lint`
对提供的文件或脏文件（如果未提供）进行lint和修复  
默认值：False  
环境变量：`AIDER_LINT`  

### `--lint-cmd`
为不同语言指定lint命令，例如："python: flake8 --select=..."（可多次使用）  
默认值：[]  
环境变量：`AIDER_LINT_CMD`  

### `--auto-lint`
启用/禁用更改后自动lint（默认：True）  
默认值：True  
环境变量：`AIDER_AUTO_LINT`  
别名：
  - `--auto-lint`
  - `--no-auto-lint`

### `--test-cmd VALUE`
指定运行测试的命令  
默认值：[]  
环境变量：`AIDER_TEST_CMD`  

### `--auto-test`
启用/禁用更改后自动测试（默认：False）  
默认值：False  
环境变量：`AIDER_AUTO_TEST`  
别名：
  - `--auto-test`
  - `--no-auto-test`

### `--test`
运行测试，修复发现的问题然后退出  
默认值：False  
环境变量：`AIDER_TEST`  

## Analytics:

### `--analytics`
为当前会话启用/禁用分析（默认：随机）  
环境变量：`AIDER_ANALYTICS`  
别名：
  - `--analytics`
  - `--no-analytics`

### `--analytics-log ANALYTICS_LOG_FILE`
指定记录分析事件的文件  
环境变量：`AIDER_ANALYTICS_LOG`  

### `--analytics-disable`
永久禁用分析  
默认值：False  
环境变量：`AIDER_ANALYTICS_DISABLE`  

## Upgrading:

### `--just-check-update`
检查更新并在退出代码中返回状态  
默认值：False  
环境变量：`AIDER_JUST_CHECK_UPDATE`  

### `--check-update`
启动时检查新的aider版本  
默认值：True  
环境变量：`AIDER_CHECK_UPDATE`  
别名：
  - `--check-update`
  - `--no-check-update`

### `--show-release-notes`
在新版本首次运行时显示发布说明（默认：None，询问用户）  
环境变量：`AIDER_SHOW_RELEASE_NOTES`  
别名：
  - `--show-release-notes`
  - `--no-show-release-notes`

### `--install-main-branch`
从主分支安装最新版本  
默认值：False  
环境变量：`AIDER_INSTALL_MAIN_BRANCH`  

### `--upgrade`
从PyPI升级aider到最新版本  
默认值：False  
环境变量：`AIDER_UPGRADE`  
别名：
  - `--upgrade`
  - `--update`

### `--version`
显示版本号并退出  

## Modes:

### `--message COMMAND`
指定要发送给LLM的单个消息，处理回复然后退出（禁用聊天模式）  
环境变量：`AIDER_MESSAGE`  
别名：
  - `--message COMMAND`
  - `--msg COMMAND`
  - `-m COMMAND`

### `--message-file MESSAGE_FILE`
指定包含要发送给LLM的消息的文件，处理回复，然后退出（禁用聊天模式）  
环境变量：`AIDER_MESSAGE_FILE`  
别名：
  - `--message-file MESSAGE_FILE`
  - `-f MESSAGE_FILE`

### `--gui`
在浏览器中运行aider（默认：False）  
默认值：False  
环境变量：`AIDER_GUI`  
别名：
  - `--gui`
  - `--no-gui`
  - `--browser`
  - `--no-browser`

### `--copy-paste`
启用aider和Web UI之间的自动复制/粘贴聊天（默认：False）  
默认值：False  
环境变量：`AIDER_COPY_PASTE`  
别名：
  - `--copy-paste`
  - `--no-copy-paste`

### `--apply FILE`
应用给定文件中的更改，而不是运行聊天（调试）  
环境变量：`AIDER_APPLY`  

### `--apply-clipboard-edits`
应用剪贴板内容作为使用主模型编辑器格式的编辑  
默认值：False  
环境变量：`AIDER_APPLY_CLIPBOARD_EDITS`  

### `--exit`
执行所有启动活动，然后在接受用户输入前退出（调试）  
默认值：False  
环境变量：`AIDER_EXIT`  

### `--show-repo-map`
打印仓库映射并退出（调试）  
默认值：False  
环境变量：`AIDER_SHOW_REPO_MAP`  

### `--show-prompts`
打印系统提示并退出（调试）  
默认值：False  
环境变量：`AIDER_SHOW_PROMPTS`  

## Voice settings:

### `--voice-format VOICE_FORMAT`
语音录制的音频格式（默认：wav）。webm和mp3需要ffmpeg  
默认值：wav  
环境变量：`AIDER_VOICE_FORMAT`  

### `--voice-language VOICE_LANGUAGE`
使用ISO 639-1代码指定语音语言（默认：auto）  
默认值：en  
环境变量：`AIDER_VOICE_LANGUAGE`  

### `--voice-input-device VOICE_INPUT_DEVICE`
指定语音录制的输入设备名称  
环境变量：`AIDER_VOICE_INPUT_DEVICE`  

## Other settings:

### `--file FILE`
指定要编辑的文件（可多次使用）  
环境变量：`AIDER_FILE`  

### `--read FILE`
指定只读文件（可多次使用）  
环境变量：`AIDER_READ`  

### `--vim`
在终端中使用VI编辑模式（默认：False）  
默认值：False  
环境变量：`AIDER_VIM`  

### `--chat-language CHAT_LANGUAGE`
指定在聊天中使用的语言（默认：None，使用系统设置）  
环境变量：`AIDER_CHAT_LANGUAGE`  

### `--yes-always`
对每个确认始终回答是  
环境变量：`AIDER_YES_ALWAYS`  

### `--verbose`
启用详细输出  
默认值：False  
环境变量：`AIDER_VERBOSE`  
别名：
  - `-v`
  - `--verbose`

### `--load LOAD_FILE`
在启动时从文件加载并执行/命令  
环境变量：`AIDER_LOAD`  

### `--encoding VALUE`
指定输入和输出的编码（默认：utf-8）  
默认值：utf-8  
环境变量：`AIDER_ENCODING`  

### `--line-endings VALUE`
写入文件时使用的行尾（默认：platform）  
默认值：platform  
环境变量：`AIDER_LINE_ENDINGS`  

### `--config CONFIG_FILE`
指定配置文件（默认：在git根目录、当前工作目录或主目录中搜索.aider.conf.yml）  
别名：
  - `-c CONFIG_FILE`
  - `--config CONFIG_FILE`

### `--env-file ENV_FILE`
指定要加载的.env文件（默认：git根目录中的.env）  
默认值：.env  
环境变量：`AIDER_ENV_FILE`  

### `--suggest-shell-commands`
启用/禁用建议shell命令（默认：True）  
默认值：True  
环境变量：`AIDER_SUGGEST_SHELL_COMMANDS`  
别名：
  - `--suggest-shell-commands`
  - `--no-suggest-shell-commands`

### `--fancy-input`
启用/禁用带有历史记录和自动完成的花式输入（默认：True）  
默认值：True  
环境变量：`AIDER_FANCY_INPUT`  
别名：
  - `--fancy-input`
  - `--no-fancy-input`

### `--multiline`
启用/禁用多行输入模式，使用Meta-Enter提交（默认：False）  
默认值：False  
环境变量：`AIDER_MULTILINE`  
别名：
  - `--multiline`
  - `--no-multiline`

### `--detect-urls`
启用/禁用检测并提供将URL添加到聊天的选项（默认：True）  
默认值：True  
环境变量：`AIDER_DETECT_URLS`  
别名：
  - `--detect-urls`
  - `--no-detect-urls`

### `--editor VALUE`
指定/editor命令使用的编辑器  
环境变量：`AIDER_EDITOR`  

### `--install-tree-sitter-language-pack`
安装tree_sitter_language_pack（实验性）  
默认值：False  
环境变量：`AIDER_INSTALL_TREE_SITTER_LANGUAGE_PACK`  
<!--[[[end]]]-->

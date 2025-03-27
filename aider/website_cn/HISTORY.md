---
title: Release history
nav_order: 925
highlight_image: /assets/blame.jpg
description: Release notes and stats on aider writing its own code.
---

# Release history

Aider 编写了其大部分代码，通常每个版本中的新代码有 70-80% 是由 Aider 自身编写的。
这些[统计数据基于 aider 仓库的 git 提交历史](/docs/faq.html#how-are-the-aider-wrote-xx-of-code-stats-computed)。

{% include blame.md %}

## Release notes

<!--[[[cog
# This page is a copy of HISTORY.md, adding the front matter above.
text = open("HISTORY.md").read()
text = text.replace("# Release history", "")
cog.out(text)
]]]-->


### Aider v0.79.0

- 添加了对 Gemini 2.5 Pro 模型的支持。
- 添加了对 DeepSeek V3 0324 模型的支持。
- 新增 `/context` 命令，可自动识别需要为特定请求编辑的文件。
- 为 `/editor` 命令添加了 `/edit` 别名。
- 为 Claude 3.7 Sonnet 模型添加了"过度热情"模式，以尝试让其在请求范围内工作。
- Aider 在此版本中编写了 65% 的代码。

### Aider v0.78.0

- 为 OpenRouter Sonnet 3.7 添加了思考令牌支持。
- 添加了切换模型类型的命令：由 csala 贡献的 `/editor-model` 用于编辑器模型，`/weak-model` 用于弱模型。
- 添加了模型设置验证，如果模型不支持，则忽略 `--reasoning-effort` 和 `--thinking-tokens`。
- 添加了 `--check-model-accepts-settings` 标志（默认：true）以强制使用不受支持的模型设置。
- 在模型设置数据中注明了哪些模型支持 reasoning_effort 和 thinking_tokens 设置。
- 使用 NoInsetMarkdown 改进了 markdown 输出中的代码块渲染，提供更好的内边距。
- 添加了 `--git-commit-verify` 标志（默认：False）以控制是否绕过 git 提交钩子。
- 由 shladnik 修复了 `/ask`、`/code` 和 `/architect` 命令的自动完成功能。
- 由 Marco Mayer 添加了在多行模式下处于 vi 正常/导航模式时按 enter 键的类 vi 行为。
- 由 lentil32 为 Bedrock 模型添加了 AWS_PROFILE 支持，允许使用 AWS 配置文件而不是显式凭证。
- 由 mopemope 增强了 `--aiderignore` 参数，可以解析绝对和相对路径。
- 改进了平台信息处理，优雅地处理检索错误。
- Aider 在此版本中编写了 92% 的代码。

### Aider v0.77.1

- 更新依赖以获取 litellm 对 Ollama 的修复。
- 添加了对 `openrouter/google/gemma-3-27b-it` 模型的支持。
- 更新了帮助文档的排除模式。

### Aider v0.77.0

- 通过采用 [tree-sitter-language-pack](https://github.com/Goldziher/tree-sitter-language-pack/) 大幅提升了[支持的编程语言](https://aider.chat/docs/languages.html)。
  - 130 种新语言支持 linter。
  - 20 种新语言支持 repo-map。
- 添加了 `/think-tokens` 命令，可以设置思考令牌预算，支持人类可读格式（8k、10.5k、0.5M）。
- 添加了 `/reasoning-effort` 命令，控制模型推理水平。
- 在不带参数调用时，`/think-tokens` 和 `/reasoning-effort` 命令会显示当前设置。
- 在模型信息中显示思考令牌预算和推理努力程度。
- 将 `--thinking-tokens` 参数更改为接受带有人类可读格式的字符串值。
- 添加了 `--auto-accept-architect` 标志（默认：true），无需确认即可自动接受架构师编码器格式的更改。
- 添加了对 `cohere_chat/command-a-03-2025` 和 `gemini/gemma-3-27b-it` 的支持。
- 裸 `/drop` 命令现在保留通过 args.read 提供的原始只读文件。
- 修复了一个错误：即使在命令行中已指定默认模型，过时的 `--shortcut` 开关也会设置默认模型。
- 改进了 AutoCompleter，要求至少 3 个字符才能自动完成，以减少干扰。
- Aider 在此版本中编写了 72% 的代码。

### Aider v0.76.2

- 修复了加载模型缓存文件时处理 JSONDecodeError 的问题。
- 修复了检索 git 用户配置时处理 GitCommandError 的问题。
- Aider 在此版本中编写了 75% 的代码。

### Aider v0.76.1

- 由 Yutaka Matsubara 添加了 ignore_permission_denied 选项到文件观察器，防止访问受限文件时出错。
- Aider 在此版本中编写了 0% 的代码。

### Aider v0.76.0

- 改进了对思考/推理模型的支持：
  - 添加了 `--thinking-tokens` CLI 选项，控制支持思考的模型的令牌预算。
  - 显示 LLM 返回的思考/推理内容。
  - 增强了对推理标签的处理，以更好地清理模型响应。
  - 为 `remove_reasoning` 设置添加了弃用警告，现已被 `reasoning_tag` 取代。
- Aider 现在会在完成最后一个请求并需要您输入时通知您：
  - 添加了 [LLM 响应就绪时的通知](https://aider.chat/docs/usage/notifications.html)，使用 `--notifications` 标志。
  - 使用 `--notifications-command` 指定桌面通知命令。
- 添加了对 QWQ 32B 的支持。
- 切换到 `tree-sitter-language-pack` 以获取 tree sitter 支持。
- 改进了对用户输入提示中 EOF（Ctrl+D）的错误处理。
- 添加了辅助函数，确保十六进制颜色值有 # 前缀。
- 修复了读取已暂存文件时处理 Git 错误的问题。
- 改进了模型信息请求的 SSL 验证控制。
- 使用更清晰的警告消息改进了空 LLM 响应处理。
- 由 Akira Komamura 修复了 Git 身份检索，以尊重全局配置。
- 主动提供安装 Bedrock 和 Vertex AI 模型的依赖项。
- 弃用模型快捷参数（如 --4o、--opus），转而使用 --model 标志。
- Aider 在此版本中编写了 85% 的代码。

### Aider v0.75.3

- 支持 OpenRouter 上的 V3 免费版：`--model openrouter/deepseek/deepseek-chat:free`。

### Aider v0.75.2

- 添加了对 OpenRouter、Bedrock 和 Vertex AI 上 Claude 3.7 Sonnet 模型的支持。
- 将 OpenRouter 上的默认模型更新为 Claude 3.7 Sonnet。
- 添加了对 GPT-4.5-preview 模型的支持。
- 添加了对 OpenRouter 上 Claude 3.7 Sonnet:beta 的支持。
- 修复了 weak_model_name 模式，使其与某些模型的主模型名称模式匹配。

### Aider v0.75.1

- 添加了对 `openrouter/anthropic/claude-3.7-sonnet` 的支持。

### Aider v0.75.0

- 对 Claude 3.7 Sonnet 的基本支持
  - 使用 `--model sonnet` 使用新的 3.7
  - 思考支持即将推出。
- 修复了 `/editor` 命令的错误。
- Aider 在此版本中编写了 46% 的代码。

### Aider v0.74.3

- 降级 streamlit 依赖以避免线程错误。
- 添加了对 tree-sitter 语言包的支持。
- 添加了 openrouter/o3-mini-high 模型配置。
- 由 Lucas Shadler 为 Kotlin 项目支持添加了 build.gradle.kts 到特殊文件。

### Aider v0.74.2

- 防止多个缓存预热线程同时激活。
- 修复了多行输入的续行提示符 ". "。
- 由 Warren Krewenki 添加了 HCL (Terraform) 语法支持。

### Aider v0.74.1

- 通过发送魔术字符串 "Formatting re-enabled." 使 o1 和 o3-mini 生成 markdown。
- 修复了多行输入的 bug，不应包含 ". " 续行提示符。

### Aider v0.74.0

- 动态更改 Ollama 上下文窗口以容纳当前聊天。
- 更好地支持 o3-mini、DeepSeek V3 和 R1、o1-mini、o1，特别是通过第三方 API 提供商。
- 从 R1 响应中删除 `<think>` 标签，用于提交消息（和其他弱模型用途）。
- 现在可以在模型设置中指定 `use_temperature: <float>`，而不仅仅是 true/false。
- 完整的 docker 容器现在包含用于 Bedrock 的 `boto3`。
- Docker 容器现在将 `HOME=/app` 设置为正常的项目挂载点，以保留 `~/.aider`。
- 修复了创建不正确文件名（如 `python`、`php` 等）的错误。
- 修复了 `--timeout` 的问题。
- 修复了 `/model` 现在正确报告弱模型未更改的问题。
- 修复了多行模式在确认提示时按 ^C 后仍然保持的问题。
- 观察文件现在完全忽略忽略文件中命名的顶级目录，以减少触及操作系统观察限制的可能性。有助于忽略像 `node_modules` 这样的巨型子树。
- 当在本地文件中提供模型元数据时，启动更快速。
- 改进了 .gitignore 处理：
  - 无论如何配置，都遵守已经生效的忽略规则。
  - 仅在文件存在时检查 .env。
- 在处理一组确认时，Yes/No 提示现在接受 All/Skip 作为 Y/N 的别名。
- Aider 在此版本中编写了 77% 的代码。

### Aider v0.73.0

- 全面支持 o3-mini：`aider --model o3-mini`
- 新的 `--reasoning-effort` 参数：low、medium、high。
- 改进了上下文窗口大小限制的处理，提供更好的消息和 Ollama 特定指导。
- 使用 `remove_reasoning: tagname` 模型设置添加了从响应中删除特定模型推理标签的支持。
- 由 xqyz 添加了在创建新文件时自动创建父目录的功能。
- 支持 OpenRouter 上的 R1 免费版：`--model openrouter/deepseek/deepseek-r1:free`
- Aider 在此版本中编写了 69% 的代码。

### Aider v0.72.3

- 由 miradnanali 强制用户/助手交替顺序，避免 R1 错误。
- 不区分大小写的模型名称匹配，同时保留原始大小写。

### Aider v0.72.2
- 加强防范用户/助手交替顺序问题，这些问题会导致 R1 错误。

### Aider v0.72.1
- 修复 `openrouter/deepseek/deepseek-r1` 的模型元数据。

### Aider v0.72.0
- 支持 DeepSeek R1。
  - 使用快捷方式：`--model r1`
  - 也可通过 OpenRouter：`--model openrouter/deepseek/deepseek-r1`
- 由 Paul Walker 添加了 Kotlin 语法对仓库映射的支持。
- 由 Titusz Pan 添加了 `--line-endings` 用于文件写入。
- 为 GPT-4o 模型添加了 examples_as_sys_msg=True，提高基准分数。
- 更新了所有依赖项，以获取 litellm 对 o1 系统消息的支持。
- 修复了在反映 lint/test 错误时的轮流问题。
- Aider 在此版本中编写了 52% 的代码。

### Aider v0.71.1

- 修复了 Docker 镜像中的权限问题。
- 添加了只读文件通知。
- 修复：Unicode 错误的 ASCII 回退。
- 修复：repomap 计算中的整数索引用于列表切片。

### Aider v0.71.0

- 添加了帮助 DeepSeek 在 `/ask` 和 `/code` 之间交替时更好地工作的提示。
- 流式处理漂亮的 LLM 响应更流畅、更快速，尤其是对于长回复。
- 对不支持流式处理的模型自动关闭流式处理
  - 现在可以在 `/model o1` 和支持流式处理的模型之间切换
- 即使在编辑带有三反引号围栏的文件时，漂亮输出仍然保持启用
- 裸 `/ask`、`/code` 和 `/architect` 命令现在会切换聊天模式。
- 增加了 repomap 的默认大小。
- 将聊天历史记录令牌限制从 4k 增加到 8k。
- 如果终端很简陋，则关闭花哨输入和监视文件。
- 添加了对自定义语音格式和输入设备设置的支持。
- 由 apaz-cli 禁用 Streamlit 电子邮件提示。
- Docker 容器现在以非 root 用户运行。
- 由 Aaron Weisberg 修复了 lint 命令处理嵌套空格字符串的问题。
- 添加了将命令输出添加到聊天时的令牌计数反馈。
- 改进了大型音频文件的错误处理，支持自动格式转换。
- 由 Krazer 改进了 git 仓库索引错误的处理。
- 通过 ASCII 回退改进了控制台输出中的 Unicode 处理。
- 将 AssertionError、AttributeError 添加到 git 错误处理。
- Aider 在此版本中编写了 60% 的代码。

### Aider v0.70.0

- 全面支持 o1 模型。
- 监视文件现在遵循 `--subtree-only`，只监视该子树。
- 改进了监视文件的提示，使其与更多模型更可靠地工作。
- 通过 uv 新增安装方法，包括一键安装。
- 支持 openrouter/deepseek/deepseek-chat 模型。
- 当通过 `/load` 或 `--load` 尝试交互式命令时，提供更好的错误处理。
- 如果绝对路径比相对路径短，则使用绝对路径显示只读文件。
- 询问 10% 的用户是否选择加入分析。
- 修复了自动建议的 bug。
- 优雅地处理 git 路径名中的 Unicode 错误。
- Aider 在此版本中编写了 74% 的代码。

### Aider v0.69.1

- 修复了模型元数据中的 gemini 模型名称。
- 当用户发表 AI 评论时，显示有关 AI! 和 AI? 的提示。
- 支持在未安装 git 的情况下运行。
- 改进了 Windows 上的环境变量设置消息。

### Aider v0.69.0

- [监视文件](https://aider.chat/docs/usage/watch.html)改进：
  - 使用 `# ... AI?` 注释触发 aider 并询问有关代码的问题。
  - 现在监视*所有*文件，而不仅仅是某些源文件。
  - 在任何文本文件中使用 `# AI comments`、`// AI comments` 或 `-- AI comments` 给 aider 指令。
- 全面支持 Gemini Flash 2.0 Exp：
  - `aider --model flash` 或 `aider --model gemini/gemini-2.0-flash-exp`
- 由 @miradnanali 添加的[新 `--multiline` 标志和 `/multiline-mode` 命令](https://aider.chat/docs/usage/commands.html#entering-multi-line-chat-messages)使 ENTER 成为软换行，META-ENTER 发送消息。
- `/copy-context <instructions>` 现在在[将代码上下文复制到剪贴板](https://aider.chat/docs/usage/copypaste.html#copy-aiders-code-context-to-your-clipboard-paste-into-the-web-ui)时接受可选的"说明"。
- 改进了剪贴板错误处理，提供有用的需求安装信息。
- 询问 5% 的用户是否选择加入分析。
- `/voice` 现在允许在发送前编辑转录文本。
- 在 Y/N 提示中禁用自动完成。
- Aider 在此版本中编写了 68% 的代码。

### Aider v0.68.0

- [Aider 可与 LLM Web 聊天界面配合使用](https://aider.chat/docs/usage/copypaste.html)。
  - 新的 `--copy-paste` 模式。
  - 新的 `/copy-context` 命令。
- [从命令行或 yaml 配置文件设置所有提供商的 API 密钥和其他环境变量](https://aider.chat/docs/config/aider_conf.html#storing-llm-keys)。
  - 新的 `--api-key provider=key` 设置。
  - 新的 `--set-env VAR=value` 设置。
- 为 `--watch-files` 添加了 bash 和 zsh 支持。
- 缺少 Gemini 和 Bedrock 模型依赖项时，提供更好的错误消息。
- Control-D 现在正确退出程序。
- 当 API 提供商返回硬错误时，不计算令牌成本。
- 修复了监视文件对没有 tree-sitter 支持的文件也能正常工作的 bug。
- 修复了 o1 模型可以用作弱模型的 bug。
- 更新了 shell 命令提示。
- 为所有 Coders 添加了文档字符串。
- 重新组织了命令行参数，改进了帮助消息和分组。
- 使用确切的 `sys.python` 进行自我升级。
- 添加了实验性 Gemini 模型。
- Aider 在此版本中编写了 71% 的代码。

### Aider v0.67.0

- [在您的 IDE 或编辑器中使用 aider](https://aider.chat/docs/usage/watch.html)。
  - 运行 `aider --watch-files`，它将监视您添加到源文件中的指令。
  - 一行 `# ...` 或 `// ...` 注释，以 "AI" 开头或结尾的是给 aider 的指令。
  - 当 aider 看到 "AI!" 时，它会读取并遵循 AI 注释中的所有指令。
- 支持新的 Amazon Bedrock Nova 模型。
- 当 `/run` 或 `/test` 有非零退出代码时，在下一条消息提示中预填 "Fix that"。
- `/diff` 现在调用 `git diff` 使用您首选的差异工具。
- 添加了对进程暂停的 Ctrl-Z 支持。
- 如果花哨符号引发 unicode 错误，spinner 现在会回退到 ASCII 艺术。
- `--read` 现在扩展 `~` 家目录。
- 在分析中启用异常捕获。
- [Aider 在此版本中编写了 61% 的代码。](https://aider.chat/HISTORY.html)

### Aider v0.66.0

- 为 Sonnet 和 Gemini 模型提供 PDF 支持。
- 由 @preynal 添加了 `--voice-input-device` 以选择语音录制的音频输入设备。
- 添加了 `--timeout` 选项来配置 API 调用超时。
- 运行 shell 命令时将 cwd 设置为仓库根目录。
- 添加了 Ctrl-Up/Down 键盘快捷键，用于按消息历史记录导航。
- 改进了对失败的 .gitignore 文件操作的错误处理。
- 改进了输入历史文件权限的错误处理。
- 改进了分析文件访问的错误处理。
- 删除了关于在 VSCode 中禁用 pretty 的虚假警告。
- 删除了对 Dart 的损坏支持。
- 修复了在聊天消息中发现 URL 时的错误。
- 更好地处理 __version__ 导入错误。
- 改进了 `/drop` 命令，支持非 glob 模式的子字符串匹配。
- Aider 在此版本中编写了 82% 的代码。

### Aider v0.65.1

- 修复了 `--alias` 的错误。

### Aider v0.65.0

- 添加了 `--alias` 配置，用于定义[自定义模型别名](https://aider.chat/docs/config/model-aliases.html)。
- 添加了 `--[no-]detect-urls` 标志，用于禁用检测和提供爬取聊天中发现的 URL。
- Ollama 模型现在默认使用 8k 上下文窗口。
- 由 @malkoG 添加了 [Dart 语言的 RepoMap 支持](https://aider.chat/docs/languages.html)。
- 询问 2.5% 的用户是否选择加入[分析](https://aider.chat/docs/more/analytics.html)。
- 跳过建议那些与聊天中已有文件同名的文件。
- `/editor` 返回并在提示中预填文件内容，因此您可以使用 `/editor` 撰写以 `/commands` 等开头的消息。
- 增强了分析的错误处理。
- 改进了 UnknownEditFormat 异常的处理，提供有用的文档链接。
- 更新依赖以获取 grep-ast 0.4.0 对 Dart 语言的支持。
- Aider 在此版本中编写了 81% 的代码。

### Aider v0.64.1

- 禁用 OpenRouter 上 o1 的流式处理。

### Aider v0.64.0

- 由 @thehunmonkgroup 添加了 [`/editor` 命令](https://aider.chat/docs/usage/commands.html)，用于打开系统编辑器编写提示。
- 全面支持 `gpt-4o-2024-11-20`。
- 默认情况下流式处理 o1 模型。
- `/run` 和建议的 shell 命令现在不那么神秘，会确认它们"将 XX 行输出添加到聊天中"。
- 询问 1% 的用户是否选择加入[分析](https://aider.chat/docs/more/analytics.html)。
- 添加了支持[可选多行输入标签](https://aider.chat/docs/usage/commands.html#entering-multi-line-chat-messages)及其匹配的闭合标签。
- 改进了[模型设置配置](https://aider.chat/docs/config/adv-model-settings.html#global-extra-params)，支持 `litellm.completion()` 的全局 `extra_params`。
- 架构师模式现在会询问是否添加 LLM 建议的文件。
- 修复了模糊模型名称匹配中的错误。
- 添加了 Timeout 异常来处理 API 提供商超时。
- 添加了 `--show-release-notes` 控制在新版本首次运行时显示发行说明。
- 在模型元数据下载失败时保存空字典到缓存文件，以延迟重试。
- 改进了错误处理和代码格式化。
- Aider 在此版本中编写了 74% 的代码。

###  Aider v0.63.2

- 修复了当 litellm 提供商信息缺失时，模糊模型名称匹配中的错误。
- 修改了模型元数据文件加载，允许覆盖资源文件。
- 允许使用 `--read` 递归加载目录。
- 更新了依赖版本以获取 litellm 对 ollama 模型的修复。
- 添加了指数退避重试，在处理编辑器文件锁时写入文件。
- 更新了 Qwen 2.5 Coder 32B 模型配置。

### Aider v0.63.1

- 修复了 git ignored file handling.
- 改进了 git operations 的错误处理。

### Aider v0.63.0

- 支持 Qwen 2.5 Coder 32B.
- `/web` 命令只是将页面添加到聊天中，不会触发 LLM 响应。
- 改进了用户首选聊天语言的提示。
- 改进了 LiteLLM exceptions 的处理。
- 修复了在报告缓存统计时重复计算令牌的问题。
- 修复了 LLM 创建新文件的问题。
- 其他小错误修复。
- Aider 在此版本中编写了 55% 的代码。

### Aider v0.62.0

- 全面支持 Claude 3.5 Haiku
  - 在 [aider 的代码编辑排行榜](https://aider.chat/docs/leaderboards/) 上得分 75%。
  - 几乎与 Sonnet 一样好，但成本低得多。
  - 使用 `--haiku` 启动它。
- 轻松应用来自 ChatGPT、Claude 或其他 web 应用的文件编辑
  - 通过其 web 应用与 ChatGPT 或 Claude 聊天。
  - 给它您的源文件并请求所需的更改。
  - 使用 web 应用的"复制响应"按钮复制 LLM 的整个回复。
  - 运行 `aider --apply-clipboard-edits file-to-edit.js`。
  - Aider 将用 LLM 的更改编辑您的文件。
- 修复了创建新文件的 bug。
- Aider 在此版本中编写了 84% 的代码。  

### Aider v0.61.0

- 加载和保存 aider 斜杠命令到文件：
  - `/save <fname>` 命令将创建一个包含 `/add` 和 `/read-only` 命令的文件，以在聊天中重新创建当前文件上下文。
  - `/load <fname>` 将重播文件中的命令。
  - 您可以使用 `/load` 运行任意一组斜杠命令，而不仅仅是 `/add` 和 `/read-only`。
  - 使用 `--load <fname>` 在启动时运行命令列表，然后再开始交互式聊天。
- 匿名、选择性加入的[分析](https://aider.chat/docs/more/analytics.html)，不共享个人数据。
- Aider 遵循 litellm 的 `supports_vision` 属性为模型启用图像支持。
- 修复了差异模式灵活处理模型使用错误文件名的情况。
- 以排序顺序显示 `/add` 和 `/read-only` 的文件名。
- 新的 `--no-fancy-input` 开关禁用提示工具包输入，现在仍可通过 `--no-pretty` 使用。
- 使用 `--no-browser` 或 `--no-gui` 覆盖浏览器配置。
- 在发生错误时提供打开文档 URL 的选项。
- 正确支持所有 o1 模型，无论提供商如何。
- 改进了输入提示上方文件名的布局。
- 更好地处理损坏的 repomap 标签缓存。
- 改进了 API 错误的处理，特别是在访问弱模型时。
- Aider 在此版本中编写了 68% 的代码。

### Aider v0.60.1

- 为 Sonnet 10/22 启用图像支持。
- 以排序顺序显示文件名。

### Aider v0.60.0

- 完全支持 Sonnet 10/22，这是 aider 代码编辑基准测试中的最新技术水平模型。
  - Aider 默认使用 Sonnet 10/22。
- 由 @jbellis 改进了聊天提示上方添加和只读文件的格式。
- 通过更灵活地解析 o1 模型不符合标准的代码编辑回复，改进了对其支持。
- 纠正了差异编辑格式提示，只替换第一个匹配项。
- 加强了整体编辑格式提示，要求提供干净的文件名。
- 现在提供将 `.env` 添加到 `.gitignore` 文件的选项。
- 附带一个小型模型元数据 json 文件，以处理尚未在 litellm 中更新的模型。
- 为 azure 上的 o1 模型提供了模型设置。
- 修复了在 `/help` RAG 结果中正确包含 URL 的问题。
- Aider 在此版本中编写了 49% 的代码。

### Aider v0.59.1

- 检查 yaml 配置中过时的 `yes: true`，显示有用的错误信息。
- 为 openrouter/anthropic/claude-3.5-sonnet:beta 提供模型设置。

### Aider v0.59.0

- 对 `/read-only` 的改进：
  - 现在支持 shell 风格的整个文件系统的自动完成。
  - 仍然像 `/add` 一样自动完成 repo 文件的完整路径。
  - 现在支持 glob 模式，如 `src/**/*.py`。
- 将 `--yes` 重命名为 `--yes-always`。
  - 现在使用 `AIDER_YES_ALWAYS` 环境变量和 `yes-always:` yaml 键。
  - 现有的 YAML 和 .env 文件需要更新。
  - 在命令行上仍可以缩写为 `--yes`。
- 配置文件现在使用标准 YAML 列表语法，每行一个 `  - list entries`。
- `/settings` 现在包括在启动时会打印的相同公告行。
- 现在在启动时对 `--editor-model` 进行健全性检查，与主模型和弱模型相同。
- 添加了 `--skip-sanity-check-repo` 开关以在大型仓库中加速启动。
- 修复了架构师模式正确处理 Control-C 的问题。
- Repo-map 现在是确定性的，具有改进的缓存逻辑。
- 改进了提交消息提示。
- Aider 在此版本中编写了 77% 的代码。

### Aider v0.58.1

- 修复了缓存预热 ping 导致后续用户消息触发 LLM 请求紧密循环的错误。

### Aider v0.58.0

- [使用一对架构师/编辑器模型进行改进的编码](https://aider.chat/2024/09/26/architect.html)
  - 使用 o1-preview 等强大的推理模型作为您的架构师。
  - 使用更便宜、更快的模型如 gpt-4o 作为您的编辑器。
- 新的 `--o1-preview` 和 `--o1-mini` 快捷方式。
- 支持新的 Gemini 002 模型。
- 更好地支持 Qwen 2.5 模型。
- 许多确认问题现在可以通过 "(D)on't ask again" 响应在会话的剩余部分跳过。
- `/read-only` 的自动完成现在支持整个文件系统。
- 新的完成菜单颜色设置。
- 新的 `/copy` 命令将最后的 LLM 响应复制到剪贴板。
- 将 `/clipboard` 重命名为 `/paste`。
- 现在在抓取 URL 时会跟随 HTTP 重定向。
- 由 @mbailey 添加的新 `--voice-format` 开关，以 wav/mp3/webm 格式发送语音音频。
- ModelSettings 接受 `extra_params` 字典，指定要传递给 `litellm.completion()` 的任何额外内容。
- 在 vim 模式下支持光标形状。
- 众多 bug 修复。
- Aider 在此版本中编写了 53% 的代码。

### Aider v0.57.1

- 修复了 aider-chat[help] 和 [playwright] 之间的依赖冲突。

### Aider v0.57.0

- 支持 OpenAI o1 模型：
  - o1-preview 现在与差异编辑格式配合良好。
  - 使用差异格式的 o1-preview 现在与使用整体编辑格式的 SOTA 排行榜结果相匹配。
  - `aider --model o1-mini`
  - `aider --model o1-preview`
- 在 Windows 上，`/run` 正确使用 PowerShell 或 cmd.exe。
- 由 @jalammar 添加对新的 08-2024 Cohere 模型的支持。
- 现在可以通过 `/read-only` 递归添加目录。
- 如果 `--no-pretty` 或 Windows 控制台不可用，用户输入提示现在会回退到简单的 `input()`。
- 改进了启动时对 git 仓库的健全性检查。
- 改进了提示缓存分块策略。
- 删除了 "No changes made to git tracked files"。
- 修复了许多特殊情况崩溃的 bug。
- 更新了所有依赖版本。
- Aider 在此版本中编写了 70% 的代码。

### Aider v0.56.0

- 由 @fry69 为通过 OpenRouter 的 Sonnet 启用提示缓存。
- 为通过 VertexAI 和 DeepSeek V2.5 的 Sonnet 启用 8k 输出令牌。
- 新的 `/report` 命令可打开浏览器，预填 GitHub 问题。
- 新的 `--chat-language` 开关设置口语语言。
- 现在 `--[no-]suggest-shell-commands` 既控制提示，也控制提供执行 shell 命令。
- 在启动时检查关键导入，如果依赖不可用则提供有用的错误消息。
- 由 @fry69 将 `--models` 重命名为 `--list-models`。
- 修复了许多特殊情况崩溃的 bug。
- Aider 在此版本中编写了 56% 的代码。

### Aider v0.55.0

- 在 Windows 上自我更新时只打印 pip 命令，不运行它。
- 将许多错误消息转换为警告消息。
- 添加了 `--tool-warning-color` 设置。
- 在任何 `/command` 中全面捕获并处理 git 错误。
- 捕获并处理 `/add` 中的 glob 错误，写入文件时的错误。
- 禁用了 typescript 的内置 linter。
- 捕获并处理不支持漂亮输出的终端。
- 捕获并处理 playwright 和 pandoc 错误。
- 捕获 `/voice` 转录异常，显示 WAV 文件以便用户可以恢复它。
- Aider 在此版本中编写了 53% 的代码。

### Aider v0.54.12

- 切换到 `vX.Y.Z.dev` 版本命名。

### Aider v0.54.11

- 改进了 Windows 上打印的 pip 命令输出。

### Aider v0.54.10

- 修复了平台信息中的测试命令 bug。

### Aider v0.54.9

- 在 repomap 中包含重要的 devops 文件。
- 向用户打印带引号的 pip 安装命令。
- 采用 setuptools_scm 提供带有 git 哈希的开发版本。
- 与 LLM 共享活动测试和 lint 命令。
- 捕获并处理创建新文件、读取现有文件的大多数错误。
- 捕获并处理大多数 git 错误。
- 为 shell 命令添加了 --verbose 调试输出。

### Aider v0.54.8

- 启动生活质量改进：
  - 对 git 仓库进行健全性检查，在出现问题时优雅退出。
  - 在模型健全性检查后暂停确认，允许用户查看警告。
- 修复了 Windows 上 shell 命令的 bug。
- 当 LLM 创建新文件时，由 @ozapinq 不进行文件名模糊匹配。
- 通过新的崩溃报告 -> GitHub 问题功能提交的众多角落案例 bug 修复。
- 崩溃报告现在包括 python 版本、操作系统等。

### Aider v0.54.7

- 提供提交预填充了未捕获异常信息的 GitHub 问题的选项。
- 修复了无限输出的 bug。

### Aider v0.54.6

- 新的 `/settings` 命令显示活动设置。
- 只有在 `--verbose` 时才显示缓存预热状态更新。

### Aider v0.54.5

- 修复了 Windows 上的 shell 命令 bug。
- 拒绝在 $HOME 中创建 git 仓库，警告用户。
- 在当前会话中不再询问用户已经表示不添加到聊天的文件。
- 添加了 `--update` 作为 `--upgrade` 的别名。

### Aider v0.54.4

- 修复了 `/model` 命令的自动完成问题。
- 修复了主目录特殊情况。

### Aider v0.54.3

- 为 docker 镜像添加了 `watchdog<5` 依赖。

### Aider v0.54.2

- 当用户在其主目录中启动 aider 时，帮助他们在子目录中查找/创建仓库。
- 添加了缺失的 `pexpect` 依赖。

### Aider v0.54.0

- 添加了 `gemini/gemini-1.5-pro-exp-0827` 和 `gemini/gemini-1.5-flash-exp-0827` 的模型设置。
- 在可用 pty 的环境中，shell 和 `/run` 命令现在可以是交互式的。
- 可选择与 LLM 共享建议的 shell 命令的输出。
- 新的 `--[no-]suggest-shell-commands` 开关配置 shell 命令。
- 大型/单体仓库中自动完成的性能改进。
- 新的 `--upgrade` 开关从 pypi 安装最新版本的 aider。
- 修复了 `--show-prompt` 的 bug。
- 对所有模型禁用 `/undo` 时自动回复 LLM。
- 从 `/web` 输出中移除了分页器。
- Aider 在此版本中编写了 64% 的代码。

### Aider v0.53.0

- [防止提示缓存过期](https://aider.chat/docs/usage/caching.html#preventing-cache-expiration)，使用 `--cache-keepalive-pings`。
  - 每 5 分钟 ping 一次 API 以保持缓存温暖。
- 现在您可以批量接受/拒绝一系列的添加 URL 和运行 shell 确认。
- 改进了从 S/R 块与聊天中文件的文件名匹配。
- 在代码聊天模式下为 Sonnet 提供更强的编辑提示。
- 为 LLM 指定完整文件路径提供更强的提示。
- 改进了 shell 命令提示。
- 弱模型现在使用 `extra_headers`，支持 Anthropic beta 功能。
- 新的 `--install-main-branch` 更新到 aider.
- 改进了尝试将非 git 子目录添加到聊天时的错误消息。
- 使用 `--verbose` 显示模型元数据信息。
- 当 LLMs 环境变量未设置时改进警告。
- 修复了包含 `\_` 的 Windows 文件名问题。
- Aider 在此版本中编写了 59% 的代码。

### Aider v0.52.1

- 修复了应用编辑时的 NameError。

### Aider v0.52.0

- Aider 现在提供运行 shell 命令的选项：
  - 启动浏览器查看更新的 html/css/js。
  - 安装新的依赖项。
  - 运行数据库迁移。
  - 运行程序以测试更改。
  - 运行新的测试用例。
- `/read` 和 `/drop` 现在将 `~` 扩展到主目录。
- 在 aider 提示符处显示活动聊天模式。
- 新的 `/reset` 命令，用于 `/drop` 文件和 `/clear` 聊天历史记录。
- 新的 `--map-multiplier-no-files` 控制聊天中没有文件时的 repo 映射大小乘数。
  - 将默认乘数减少到 2。
- 修复和改进自动提交排序的问题。
- 改进了令牌报告和确认对话框的格式。
- 默认 OpenAI 模型现在是 `gpt-4o-2024-08-06`。
- 更新依赖以获取 litellm 错误修复。
- Aider 在此版本中编写了 68% 的代码。

### Aider v0.51.0

- 使用 `--cache-prompts` 为 Anthropic 模型提供提示缓存。
  - 缓存系统提示、仓库映射和 `/read-only` 文件。
- 在大型/单体仓库或启用缓存时，仓库映射重新计算的频率降低。
  - 使用 `--map-refresh <always|files|manual|auto>` 进行配置。
- 改进了缓存的成本估算逻辑。
- 改进了对 Jupyter Notebook `.ipynb` 文件的编辑性能。
- 使用 `--verbose` 显示加载了哪个配置 yaml 文件。
- 更新了依赖版本。
- 错误修复：正确加载 `.aider.models.metadata.json` 数据。
- 错误修复：使用 `--msg /ask ...` 导致异常。
- 错误修复：litellm 对图像的分词器错误。
- Aider 在此版本中编写了 56% 的代码。

### Aider v0.50.1

- 修复了提供商 API 异常的问题。

### Aider v0.50.0

- 除了 Anthropic 的模型外，DeepSeek Coder、Mistral 模型也支持无限输出。
- 新的 `--deepseek` 开关用于使用 DeepSeek Coder。
- DeepSeek Coder 使用 8k 令牌输出。
- 新的 `--chat-mode <mode>` 开关以 ask/help/code 模式启动。
- 新的 `/code <message>` 命令在 `ask` 模式下请求代码编辑。
- 如果页面永不空闲，网页抓取器更加健壮。
- 改进了无限输出的令牌和成本报告。
- 改进和修复了 `/read` 只读文件的问题。
- 由 @branchvincent 将 `setup.py` 切换为 `pyproject.toml`。
- 修复了在 `/ask` 期间添加的文件的持久化问题。
- 修复了 `/tokens` 中聊天历史大小的错误。
- Aider 在此版本中编写了 66% 的代码。

### Aider v0.49.1

- 修复了 `/help` 的错误。

### Aider v0.49.0

- 添加 `/read` 和 `--read` 将只读文件添加到聊天上下文，包括 git 仓库外的文件。
- `/diff` 现在显示您的请求产生的所有更改的差异，包括 lint 和测试修复。
- 新的 `/clipboard` 命令从剪贴板粘贴图像或文本，替代 `/add-clipboard-image`。
- 现在显示使用 `/web` 添加 URL 时抓取的 markdown。
- 在[脚本化 aider](https://aider.chat/docs/scripting.html) 时，消息现在可以包含聊天内的 `/` 命令。
- docker 镜像中的 Aider 现在建议使用正确的命令更新到最新版本。
- 在 API 错误上改进重试（在 Sonnet 宕机期间很容易测试）。
- 添加了 `--mini` 用于 `gpt-4o-mini`。
- 保持会话成本准确，即使在使用 `/ask` 和 `/help` 时。
- 仓库映射计算的性能改进。
- `/tokens` 现在显示活跃模型。
- 增强的提交消息归属选项：
  - 新的 `--attribute-commit-message-author` 在提交消息前加上"aider: "，如果 aider 是更改的作者，替代 `--attribute-commit-message`。
  - 新的 `--attribute-commit-message-committer` 在所有提交消息前加上"aider: "。
- Aider 在此版本中编写了 61% 的代码。

### Aider v0.48.1

- 添加了 `openai/gpt-4o-2024-08-06`。
- 解决了使用 `extra_headers` 时 litellm 移除 OpenRouter 应用标头的问题。
- 在仓库映射处理期间改进了进度指示。
- 更正了升级 docker 容器到最新 aider 版本的说明。
- 移除了提交差异上过时的 16k 令牌限制，使用每个模型的限制。

### Aider v0.48.0

- 大型/单体仓库的性能改进。
- 添加了 `--subtree-only` 以限制 aider 到当前目录子树。
  - 应该有助于大型/单体仓库的性能。
- 新的 `/add-clipboard-image` 从剪贴板添加图像到聊天。
- 使用 `--map-tokens 1024` 对任何模型使用仓库映射。
- 支持 Sonnet 的 8k 输出窗口。
  - [Aider 已经支持 Sonnet 的无限输出。](https://aider.chat/2024/07/01/sonnet-not-lazy.html)
- 解决 litellm 重试 API 服务器错误的 bug。
- 升级依赖项，获取 litellm 错误修复。
- Aider 在此版本中编写了 44% 的代码。

### Aider v0.47.1

- 改进了常规提交提示。

### Aider v0.47.0

- [提交消息](https://aider.chat/docs/git.html#commit-messages)改进：
  - 在提交消息提示中添加了 Conventional Commits 准则。
  - 添加了 `--commit-prompt` 以自定义提交消息提示。
  - 添加了强大模型作为提交消息（和聊天摘要）的后备。
- [Linting](https://aider.chat/docs/usage/lint-test.html) 改进：
  - 修复 lint 错误前询问。
  - 改进了对仓库中所有脏文件的 `--lint` 性能。
  - 改进了 lint 流程，现在在 linting 前进行代码编辑自动提交。
  - 修复了正确处理子进程编码的问题（也适用于 `/run`）。
- 改进了 [docker 支持](https://aider.chat/docs/install/docker.html)：
  - 解决了使用 `docker run --user xxx` 时的权限问题。
  - 新的 `paulgauthier/aider-full` docker 镜像，包含所有额外功能。
- 切换到代码和询问模式不再总结聊天历史。
- 添加了 aider 对每个版本贡献的图表。
- 为没有完成覆盖的 `/commands` 提供通用自动完成。
- 修复了 OCaml 标签文件。
- 修复了 `/run` 添加到聊天确认逻辑中的错误。
- Aider 在此版本中编写了 58% 的代码。

### Aider v0.46.1

- 将谷歌 numpy 依赖降级回 1.26.4。

### Aider v0.46.0

- 新的 `/ask <question>` 命令，询问关于代码的问题，但不做任何更改。
- 新的 `/chat-mode <mode>` 命令切换聊天模式：
  - ask: 询问关于代码的问题，但不做任何更改。
  - code: 请求对代码进行更改（使用最佳编辑格式）。
  - help: 获取关于使用 aider 的帮助（用法、配置、故障排除）。
- 在 `.aider.conf.yml` 中添加 `file: CONVENTIONS.md` 以始终加载特定文件。
  - 或者 `file: [file1, file2, file3]` 以始终加载多个文件。
- 增强了令牌使用和成本报告。现在在流式传输时也能工作。
- `/add` 和 `/drop` 的文件名自动完成现在不区分大小写。
- 提交消息改进：
  - 更新了提交消息提示以使用祈使语气。
  - 如果弱模型无法生成提交消息，回退到主模型。
- 阻止 aider 多次询问是否将同一 URL 添加到聊天中。
- 更新和修复 `--no-verify-ssl`：
  - 修复了 v0.42.0 中的回归。
  - 当 `/web` 抓取网站时禁用 SSL 证书验证。
- 改进了 `/web` 抓取功能中的错误处理和报告。
- 修复了 Elm 的 tree-sitter scm 文件中的语法错误（由 @cjoach 提供）。
- 处理将文本流式传输到终端时的 UnicodeEncodeError。
- 更新依赖项到最新版本。
- Aider 在此版本中编写了 45% 的代码。

### Aider v0.45.1

- 在使用 3.5-turbo 的任何地方将 4o-mini 用作弱模型。

### Aider v0.45.0

- GPT-4o mini 使用整体编辑格式的得分与原始 GPT 3.5 相似。
- Aider 在 Windows 上更好地提供将文件添加到聊天的选项。
- 修复了 `/undo` 与新文件或新仓库的边缘情况。
- 现在在 `--verbose` 输出中显示 API 密钥的最后 4 个字符。
- 修复了多个 `.env` 文件的优先级问题。
- 修复了在安装 pandoc 时优雅处理 HTTP 错误的问题。
- Aider 在此版本中编写了 42% 的代码。

### Aider v0.44.0

- 默认 pip 安装尺寸减少了 3-12 倍。
- 添加了 3 个包额外功能，aider 将在需要时提供安装：
  - `aider-chat[help]`
  - `aider-chat[browser]`
  - `aider-chat[playwright]`
- 改进了检测用户聊天消息中 URL 的正则表达式。
- 修复了在 `/add` 中包含绝对路径时的 globbing 逻辑。
- 简化了 `--models` 的输出。
- `--check-update` 开关重命名为 `--just-check-updated`。
- `--skip-check-update` 开关重命名为 `--[no-]check-update`。
- Aider 在此版本中编写了 29% 的代码（157/547 行）。

### Aider v0.43.4

- 将 scipy 添加回主要 requirements.txt。

### Aider v0.43.3

- 将 build-essentials 添加回主要 Dockerfile。

### Aider v0.43.2

- 将 HuggingFace 嵌入依赖移至 [hf-embed] 额外功能。
- 添加了 [dev] 额外功能。

### Aider v0.43.1

- 用仅 CPU 版本替换 torch 要求，因为 GPU 版本太大。

### Aider v0.43.0

- 使用 `/help <question>` [询问有关使用 aider 的帮助](https://aider.chat/docs/troubleshooting/support.html)，自定义设置，故障排除，使用 LLM 等。
- 允许多次使用 `/undo`。
- 所有配置/环境/yml/json 文件现在从主目录、git 根目录、当前工作目录和命名命令行开关加载。
- 新的 `$HOME/.aider/caches` 目录用于应用范围的可消耗缓存。
- 默认 `--model-settings-file` 现在是 `.aider.model.settings.yml`。
- 默认 `--model-metadata-file` 现在是 `.aider.model.metadata.json`。
- 修复了使用 `--no-git` 启动时影响的错误。
- Aider 在此版本中编写了 424 行编辑中的 9%。

### Aider v0.42.0

- 性能发布：
  - 启动速度提升 5 倍！
  - 大型 git 仓库中的自动完成速度更快（用户报告约 100 倍加速）！

### Aider v0.41.0

- [允许 Claude 3.5 Sonnet 流式返回 >4k 令牌！](https://aider.chat/2024/07/01/sonnet-not-lazy.html)
  - 它是第一个能够编写如此大型连贯、有用的代码编辑的模型。
  - 一次完成大型重构或生成多个新代码文件。
- 如果环境中设置了 `ANTHROPIC_API_KEY`，aider 现在默认使用 `claude-3-5-sonnet-20240620`。
- [为 3.5 Sonnet 和通过 OpenRouter 的 GPT-4o 和 3.5 Sonnet 启用图像支持](https://aider.chat/docs/usage/images-urls.html)（由 @yamitzky 提供）。
- 添加了 `--attribute-commit-message` 以在 aider 的提交消息前缀添加 "aider:"。
- 修复了一行提交消息质量的回归。
- 在 Anthropic 的 `overloaded_error` 上自动重试。
- 更新了依赖版本。

### Aider v0.40.6

- 修复了 `/undo`，使其无论 `--attribute` 设置如何都能工作。

### Aider v0.40.5

- 更新版本以获取最新的 litellm，修复与 Gemini 的流式问题
  - https://github.com/BerriAI/litellm/issues/4408

### Aider v0.40.1

- 改进了 repomap 的上下文感知能力。
- 恢复了正确的 `--help` 功能。

### Aider v0.40.0

- 改进了提示，阻止 Sonnet 浪费令牌输出不变的代码 (#705)。
- 改进了令牌限制错误的错误信息。
- 选项可以禁止在 [git 作者和提交者名称](https://aider.chat/docs/git.html#commit-attribution) 中添加 "(aider)"。
- 使用 `--model-settings-file` 自定义每个模型的设置，如 repo-map 的使用（由 @caseymcc 提供）。
- 改进了 python 代码的 flake8 linter 调用。


### Aider v0.39.0

- 使用 `--sonnet` 获取 Claude 3.5 Sonnet，它是 [aider 的 LLM 代码编辑排行榜](https://aider.chat/docs/leaderboards/#claude-35-sonnet-takes-the-top-spot) 上的顶级模型。
- 所有 `AIDER_xxx` 环境变量现在可以在 `.env` 中设置（由 @jpshack-at-palomar 提供）。
- 使用 `--llm-history-file` 记录发送到 LLM 的原始消息（由 @daniel-vainsencher 提供）。
- 提交消息不再添加 "aider:" 前缀。相反，git 作者和提交者名称添加 "(aider)"。

### Aider v0.38.0

- 使用 `--vim` 在聊天中[获取 vim 按键绑定](https://aider.chat/docs/usage/commands.html#vi)。
- 通过 `.aider.models.json` 文件[添加 LLM 元数据](https://aider.chat/docs/llms/warnings.html#specifying-context-window-size-and-token-costs)（由 @caseymcc 提供）。
- 令牌限制错误的[更详细错误消息](https://aider.chat/docs/troubleshooting/token-limits.html)。
- 单行提交消息，不包含最近的聊天消息。
- 确保 `--commit --dry-run` 不做任何事情。
- 让 playwright 等待网络空闲以更好地抓取 js 网站。
- 文档更新，移至 website/ 子目录。
- 将 tests/ 移至 aider/tests/。

### Aider v0.37.0

- 仓库映射现在基于聊天历史文本以及添加到聊天的文件进行优化。
- 当没有文件添加到聊天时，改进了提示以请求 LLM 文件建议。
- Aider 会注意到你是否将 URL 粘贴到聊天中，并提供抓取它的选项。
- 仓库映射的性能改进，特别是在大型仓库中。
- Aider 不会提供添加像 `make` 或 `run` 这样可能只是词语的裸文件名。
- 如果已经设置，正确覆盖提交的 `GIT_EDITOR` 环境变量。
- 检测 `/voice` 支持的音频采样率。
- 其他小错误修复。

### Aider v0.36.0

- [Aider 现在可以对你的代码进行 linting 并修复任何错误](https://aider.chat/2024/05/22/linting.html)。
  - Aider 在每次 LLM 编辑后自动进行 linting 和修复。
  - 你可以使用聊天中的 `/lint` 或命令行上的 `--lint` 手动对文件进行 lint-and-fix。
  - Aider 为所有支持的 tree-sitter 语言包含内置的基本 linter。
  - 你还可以配置 aider 使用 `--lint-cmd` 来使用你喜欢的 linter。
- Aider 额外支持运行测试和修复问题。
  - 使用 `--test-cmd` 配置你的测试命令。
  - 使用 `/test` 或从命令行使用 `--test` 运行测试。
  - Aider 将自动尝试修复任何测试失败。

### Aider v0.35.0

- Aider 现在默认使用 GPT-4o。
  - GPT-4o 在 [aider LLM 代码编辑排行榜](https://aider.chat/docs/leaderboards/) 上以 72.9% 的成绩排名第一，而 Opus 为 68.4%。
  - GPT-4o 在 [aider 的重构排行榜](https://aider.chat/docs/leaderboards/#code-refactoring-leaderboard) 上以 62.9% 的成绩排名第二，而 Opus 为 72.3%。
- 添加了 `--restore-chat-history` 在启动时恢复先前的聊天历史，以便你可以继续最后的对话。
- 改进了使用差异编辑格式的 LLM 的反射反馈。
- 改进了对 `httpx` 错误的重试。

### Aider v0.34.0

- 更新了提示，使用更自然的表述方式来描述文件、git 仓库等。移除了对读写/只读术语的依赖。
- 重构了提示，统一了不同编辑格式的表述方式。
- 增强了提示中使用的预设助手回复。
- 为 `openrouter/anthropic/claude-3-opus`、`gpt-3.5-turbo` 添加了明确的模型设置。
- 添加了 `--show-prompts` 调试选项。
- 错误修复：捕获并重试所有 litellm 异常。


### Aider v0.33.0

- 使用 `DEEPSEEK_API_KEY` 和 `deepseek/deepseek-chat` 等添加了对 [Deepseek 模型](https://aider.chat/docs/llms.html#deepseek) 的原生支持，而不是作为通用的 OpenAI 兼容 API。

### Aider v0.32.0

- [Aider LLM 代码编辑排行榜](https://aider.chat/docs/leaderboards/) 对流行模型根据其编辑代码的能力进行排名。
  - 排行榜包括 GPT-3.5/4 Turbo、Opus、Sonnet、Gemini 1.5 Pro、Llama 3、Deepseek Coder 和 Command-R+。
- Gemini 1.5 Pro 现在默认使用新的差异风格编辑格式（diff-fenced），使其能够更好地处理更大的代码库。
- 通过在差异编辑格式中对系统消息进行更灵活的配置，支持 Deepseek-V2。
- 改进了对模型 API 错误的重试处理。
- 基准测试输出结果采用 YAML 格式，与排行榜兼容。

### Aider v0.31.0

- [Aider 现在也支持在浏览器中进行 AI 结对编程！](https://aider.chat/2024/05/02/browser.html) 使用 `--browser` 开关启动实验性的基于浏览器的 aider 版本。
- 在聊天过程中使用 `/model <n>` 切换模型，使用 `/models <query>` 搜索可用模型列表。

### Aider v0.30.1

- 添加缺失的 `google-generativeai` 依赖

### Aider v0.30.0

- 添加了 [Gemini 1.5 Pro](https://aider.chat/docs/llms.html#free-models) 作为推荐的免费模型。
- 允许对"整体"编辑格式使用仓库映射。
- 添加了 `--models <MODEL-NAME>` 用于搜索可用模型。
- 添加了 `--no-show-model-warnings` 以静默模型警告。

### Aider v0.29.2

- 改进了[模型警告](https://aider.chat/docs/llms.html#model-warnings)，用于未知或不熟悉的模型

### Aider v0.29.1

- 添加了对 groq/llama3-70b-8192 的更好支持

### Aider v0.29.0

- 添加了对[直接连接到 Anthropic、Cohere、Gemini 和许多其他 LLM 提供商](https://aider.chat/docs/llms.html)的支持。
- 添加了 `--weak-model <model-name>` 选项，允许您指定用于提交消息和聊天历史摘要的模型。
- 用于处理流行模型的新命令行开关：
  - `--4-turbo-vision`
  - `--opus`
  - `--sonnet`
  - `--anthropic-api-key`
- 改进了"整体"和"差异"后端，以更好地支持 [Cohere 的免费使用 Command-R+ 模型](https://aider.chat/docs/llms.html#cohere)。
- 允许从文件系统的任何位置使用 `/add` 添加图片。
- 修复了在分离的 HEAD 状态下在仓库中操作时的崩溃问题。
- 修复：在 CLI 和 python 脚本中使用相同的默认模型。

### Aider v0.28.0

- 添加了对新的 `gpt-4-turbo-2024-04-09` 和 `gpt-4-turbo` 模型的支持。
  - 在 Exercism 基准测试中得分为 61.7%，与 `gpt-4-0613` 相当，但比 `gpt-4-preview-XXXX` 模型差。请参阅[最近的 Exercism 基准测试结果](https://aider.chat/2024/03/08/claude-3.html)。
  - 在重构/懒惰基准测试中得分为 34.1%，明显比 `gpt-4-preview-XXXX` 模型差。请参阅[最近的重构基准测试结果](https://aider.chat/2024/01/25/benchmarks-0125.html)。
  - Aider 继续默认使用 `gpt-4-1106-preview`，因为它在两项基准测试中表现最佳，尤其在重构/懒惰基准测试中表现显著更好。

### Aider v0.27.0

- 改进了对 typescript 的 repomap 支持，由 @ryanfreckleton 贡献。
- 错误修复：仅对上次提交的文件执行 /undo，不覆盖其他脏文件
- 错误修复：当未设置 OpenAI API 密钥时显示清晰的错误消息。
- 错误修复：捕获没有 tags.scm 文件的罕见语言的错误。

### Aider v0.26.1

- 修复了在某些环境中解析 git 配置时的错误。

### Aider v0.26.0

- 默认使用 GPT-4 Turbo。
- 添加了 `-3` 和 `-4` 开关，用于使用 GPT 3.5 或 GPT-4（非 Turbo）。
- 错误修复，避免将本地 git 错误反映回 GPT。
- 改进了启动时打开 git 仓库的逻辑。

### Aider v0.25.0

- 如果用户向聊天中添加过多代码，会发出警告。
  - https://aider.chat/docs/faq.html#how-can-i-add-all-the-files-to-the-chat
- 明确拒绝将与 `.aiderignore` 匹配的文件添加到聊天中
  - 防止随后对这些文件进行 git 提交时出现的错误。
- 添加了 `--openai-organization-id` 参数。
- 如果编辑无法应用，向用户展示 FAQ 链接。
- 将过去的文章作为 https://aider.chat/blog/ 的一部分。

### Aider v0.24.1

- 修复了启用 --no-steam 时成本计算的错误

### Aider v0.24.0

- 新的 `/web <url>` 命令，它会抓取网址内容，将其转换为相当干净的 markdown 并添加到聊天中。
- 更新了所有 OpenAI 模型名称、价格信息
- 默认的 GPT 3.5 模型现在是 `gpt-3.5-turbo-0125`。
- 修复了 `!` 作为 `/run` 别名的错误。

### Aider v0.23.0

- 添加了对 `--model gpt-4-0125-preview` 和 OpenAI 的别名 `--model gpt-4-turbo-preview` 的支持。`--4turbo` 开关目前仍然是 `--model gpt-4-1106-preview` 的别名。
- 新的 `/test` 命令，它运行命令并在退出状态非零时将输出添加到聊天中。
- 改进了 markdown 的终端流式传输。
- 添加了 `/quit` 作为 `/exit` 的别名。
- 添加了 `--skip-check-update` 以跳过启动时的更新检查。
- 添加了 `--openrouter` 作为 `--openai-api-base https://openrouter.ai/api/v1` 的快捷方式。
- 修复了阻止使用环境变量 `OPENAI_API_BASE, OPENAI_API_TYPE, OPENAI_API_VERSION, OPENAI_API_DEPLOYMENT_ID` 的错误。

### Aider v0.22.0

- 改进了统一差异编辑格式。
- 添加了 ! 作为 /run 的别名。
- /add 和 /drop 的自动完成现在对带空格的文件名正确加引号。
- /undo 命令会请求 GPT 不要只是重试被撤销的编辑。

### Aider v0.21.1

- 修复了统一差异编辑格式的错误。
- 添加了 --4turbo 和 --4 作为 --4-turbo 的别名。

### Aider v0.21.0

- 支持 python 3.12。
- 改进了统一差异编辑格式。
- 新的 `--check-update` 参数用于检查是否有可用更新并以状态码退出。

### Aider v0.20.0

- 将图片添加到聊天中以自动使用 GPT-4 Vision，由 @joshuavial 贡献

- 错误修复：
  - 改进了 `/run` 命令输出的 Unicode 编码，由 @ctoth 贡献
  - 防止在 Windows 上错误的自动提交，由 @ctoth 贡献

### Aider v0.19.1

- 移除了多余的调试输出。

### Aider v0.19.0

- [由于新的统一差异编辑格式，显著减少了 GPT-4 Turbo 的"懒惰"编码](https://aider.chat/docs/unified-diffs.html)
  - 在新的"懒惰基准测试"中，得分从 20% 提高到 61%。
  - Aider 现在默认对 `gpt-4-1106-preview` 使用统一差异。
- 新的 `--4-turbo` 命令行开关，作为 `--model gpt-4-1106-preview` 的快捷方式。

### Aider v0.18.1

- 升级到新的 openai python 客户端 v1.3.7。

### Aider v0.18.0

- 改进了 GPT-4 和 GPT-4 Turbo 的提示。
  - GPT-4 Turbo (`gpt-4-1106-preview`) 的编辑错误大大减少。
  - 六月版 GPT-4 (`gpt-4-0613`) 的基准测试结果显著提高。性能从 47%/64% 跃升至 51%/71%。
- 修复了一个错误，该错误导致聊天中的文件同时被标记为只读和可读写，有时会使 GPT 混淆。
- 修复了错误，以正确处理带有子模块的仓库。

### Aider v0.17.0

- 支持 OpenAI 新的 11/06 模型：
  - gpt-4-1106-preview 带有 128k 上下文窗口
  - gpt-3.5-turbo-1106 带有 16k 上下文窗口
- [OpenAI 新的 11/06 模型的基准测试](https://aider.chat/docs/benchmarks-1106.html)
- 简化了 [aider 脚本编写的 API，添加了文档](https://aider.chat/docs/faq.html#can-i-script-aider)
- 要求更简洁的 SEARCH/REPLACE 块。[基准测试](https://aider.chat/docs/benchmarks.html)得分为 63.9%，没有回归。
- 改进了对 elisp 的仓库映射支持。
- 修复了当对匹配 `.gitignore` 的文件使用 `/add` 时的崩溃错误
- 修复了各种错误，以捕获和处理 unicode 解码错误。

### Aider v0.16.3

- 修复了对 C# 的仓库映射支持。

### Aider v0.16.2

- 修复了 docker 镜像。

### Aider v0.16.1

- 更新了 tree-sitter 依赖项，以简化 pip 安装过程

### Aider v0.16.0

- [使用 tree-sitter 改进仓库映射](https://aider.chat/docs/repomap.html)
- 从"编辑块"切换到"搜索/替换块"，减少了格式错误的编辑块。[基准测试](https://aider.chat/docs/benchmarks.html)得分为 66.2%，没有回归。
- 改进了对针对同一文件的多个编辑的格式错误编辑块的处理。[基准测试](https://aider.chat/docs/benchmarks.html)得分为 65.4%，没有回归。
- 修复了正确处理格式错误的 `/add` 通配符的问题。


### Aider v0.15.0

- 添加了对 `.aiderignore` 文件的支持，指示 aider 忽略 git 仓库的部分内容。
- 新的 `--commit` 命令行参数，它仅使用由 gpt-3.5 生成的合理提交消息提交所有待处理的更改。
- 为 [aider docker 镜像](https://aider.chat/docs/install/docker.html) 添加了通用 ctags 和多种架构支持
- `/run` 和 `/git` 现在接受完整的 shell 命令，例如：`/run (cd subdir; ls)`
- 恢复了缺失的 `--encoding` 命令行开关。

### Aider v0.14.2

- 轻松[从 docker 镜像运行 aider](https://aider.chat/docs/install/docker.html)
- 修复了聊天历史摘要的错误。
- 修复了 `soundfile` 包不可用时的错误。

### Aider v0.14.1

- /add 和 /drop 处理绝对文件名和带引号的文件名
- /add 检查文件是否在 git 仓库（或根目录）内
- 如果需要，提醒用户聊天中的文件路径都是相对于 git 仓库的
- 修复了在仓库子目录中启动 aider 时的 /add 错误
- 如果请求的模型不可用，显示 api/key 支持的模型

### Aider v0.14.0

- [通过 OpenRouter 支持 Claude2 和其他 LLM](https://aider.chat/docs/faq.html#accessing-other-llms-with-openrouter)，由 @joshuavial 贡献
- [运行 aider 基准测试套件](https://github.com/Aider-AI/aider/tree/main/benchmark) 的文档
- Aider 现在需要 Python >= 3.9


### Aider v0.13.0

- [只对 GPT 尝试编辑的脏文件进行 git 提交](https://aider.chat/docs/faq.html#how-did-v0130-change-git-usage)
- 将聊天历史作为提示/上下文发送给 Whisper 语音转录
- 添加了 `--voice-language` 开关，限制 `/voice` 转录为特定语言
- 延迟绑定导入 `sounddevice`，因为它会减慢 aider 启动速度
- 改进了命令行和 yml 配置设置的 --foo/--no-foo 开关处理

### Aider v0.12.0

- [语音转代码](https://aider.chat/docs/usage/voice.html)支持，允许您使用语音进行编码。
- 修复了 /diff 导致崩溃的错误。
- 改进了 gpt-4 的提示，重构了 editblock coder。
- [基准测试](https://aider.chat/docs/benchmarks.html)得分为 gpt-4/diff 的 63.2%，没有回归。

### Aider v0.11.1

- 初始创建仓库映射时添加了进度条。
- 修复了向空仓库添加新文件时的错误提交消息。
- 修复了脏提交时待处理聊天历史摘要的边缘情况。
- 修复了使用 `--no-pretty` 时未定义 `text` 的边缘情况。
- 修复了仓库重构后的 /commit 错误，添加了测试覆盖。
- [基准测试](https://aider.chat/docs/benchmarks.html)得分为 gpt-3.5/whole 的 53.4%（无回归）。

### Aider v0.11.0

- 自动摘要聊天历史，避免耗尽上下文窗口。
- 使用 `--no-stream` 运行时提供更多关于美元成本的详细信息
- 增强了 GPT-3.5 提示，防止在回复中跳过/省略代码（51.9% [基准测试](https://aider.chat/docs/benchmarks.html)，无回归）
- 防止 GPT-3.5 或非 OpenAI 模型建议使用星号包围的文件名。
- 将 GitRepo 代码从 Coder 类中重构出来。

### Aider v0.10.1

- /add 和 /drop 始终使用相对于 git 根目录的路径
- 鼓励 GPT 使用"将文件添加到聊天中"之类的语言，以要求用户允许编辑它们。

### Aider v0.10.0

- 添加了 `/git` 命令，可在 aider 聊天中运行 git。
- 使用 Meta-ENTER（在某些环境中为 Esc+ENTER）输入多行聊天消息。
- 创建一个包含 `.aider*` 的 `.gitignore`，以防止用户意外将 aider 文件添加到 git 中。
- 检查 pypi 是否有更新版本并通知用户。
- 更新了键盘中断逻辑，使得 2 秒内按 2 次 ^C 总是强制 aider 退出。
- 如果 GPT 创建了错误的编辑块，提供详细错误信息，要求重试。
- 如果 aider 检测到它在 VSCode 终端内运行，则强制使用 `--no-pretty`。
- [基准测试](https://aider.chat/docs/benchmarks.html)得分为 gpt-4/diff 的 64.7%（无回归）


### Aider v0.9.0

- 支持在[Azure](https://aider.chat/docs/faq.html#azure)中使用OpenAI模型
- 添加了`--show-repo-map`选项
- 改进了重试连接OpenAI API时的输出显示
- 从`--verbose`输出中隐藏了API密钥
- 错误修复：识别并添加用户或GPT提到的子目录中的文件
- [基准测试](https://aider.chat/docs/benchmarks.html)得分为gpt-3.5-turbo/whole的53.8%（无回归）

### Aider v0.8.3

- 添加了`--dark-mode`和`--light-mode`选项，用于选择针对终端背景优化的颜色
- 安装文档链接到由@joshuavial开发的[NeoVim插件](https://github.com/joshuavial/aider.nvim)
- 重新组织了`--help`输出
- 修复/改进了整体编辑格式，可能改善了GPT-3.5的代码编辑
- 修复了关于带有Unicode字符的git文件名的错误并添加了测试
- 修复了在OpenAI返回InvalidRequest时aider抛出异常的问题
- 修复/改进了/add和/drop命令，使其能够递归选择目录
- 修复了使用"whole"编辑格式时的实时差异输出

### Aider v0.8.2

- 禁用了gpt-4的通用可用性（它正在推出，尚未100%可用）

### Aider v0.8.1

- 如果没有找到git仓库，询问是否创建一个，以便更好地跟踪GPT的代码更改
- 现在在`/add`和`/drop`命令中支持通配符
- 将`--encoding`传递给ctags，要求它返回`utf-8`
- 更加健壮地处理文件路径，避免Windows 8.3文件名问题
- 添加了[FAQ](https://aider.chat/docs/faq.html)
- 将GPT-4标记为普遍可用
- 修复了带有缺失文件名的whole coder的实时差异显示
- 修复了多文件聊天的问题
- 修复了editblock coder提示中的问题

### Aider v0.8.0

- [比较GPT-3.5和GPT-4代码编辑能力的基准测试](https://aider.chat/docs/benchmarks.html)
- 改进了Windows支持：
  - 修复了与Windows路径分隔符相关的错误
  - 添加了在Windows上运行所有测试的CI步骤
- 改进了Unicode编码/解码处理：
  - 默认明确使用utf-8编码读取/写入文本文件（主要有益于Windows）
  - 添加了`--encoding`开关以指定其他编码
  - 优雅地处理解码错误
- 添加了`--code-theme`开关，用于控制代码块的pygments样式（由@kwmiebach贡献）
- 当ctags被禁用时提供更好的状态消息，解释原因

### Aider v0.7.2:

- 修复了一个错误，允许aider编辑包含三重反引号围栏的文件。

### Aider v0.7.1:

- 修复了GPT-3.5聊天中流式差异显示的错误

### Aider v0.7.0:

- 优雅地处理上下文窗口耗尽的情况，包括提供有用的提示。
- 添加了`--message`选项，用于给GPT一条指令，然后在它回复并执行任何编辑后退出。
- 添加了`--no-stream`选项，用于禁用GPT响应的流式显示。
  - 非流式响应包括令牌使用信息。
  - 根据OpenAI公布的价格显示成本信息。
- 基于Execism的python仓库开发的编程任务套件的编码能力基准测试工具。
  - https://github.com/exercism/python
- 为支持新的函数调用API进行了重大重构。
- 为3.5实现了基于函数的代码编辑后端的初始版本。
  - 初步实验表明，使用函数使3.5在编码方面的能力下降。
- 限制GPT返回格式错误的编辑响应时的自动重试次数。

### Aider v0.6.2

* 支持`gpt-3.5-turbo-16k`以及所有OpenAI聊天模型
* 改进了在gpt-4省略代码编辑中的前导空格时进行纠正的能力
* 添加了`--openai-api-base`选项，以支持API代理等

### Aider v0.5.0

- 添加了对`gpt-3.5-turbo`和`gpt-4-32k`的支持。
- 添加了`--map-tokens`选项，为仓库映射设置令牌预算，以及基于PageRank的算法，用于优先考虑要包含在映射中的文件和标识符。
- 添加了聊天命令`/tokens`，用于报告上下文窗口令牌使用情况。
- 添加了聊天命令`/clear`，用于清除对话历史记录。
<!--[[[end]]]-->

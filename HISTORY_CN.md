# 发布历史

### Aider v0.79.0

- 添加了对 Gemini 2.5 Pro 模型的支持。
- 添加了对 DeepSeek V3 0324 模型的支持。
- 添加了新的 `/context` 命令，可自动识别需要为特定请求编辑的文件。
- 添加了 `/edit` 作为 `/editor` 命令的别名。
- 为 Claude 3.7 Sonnet 模型添加了"过度热情"模式，尝试让其在请求范围内工作。
- Aider 编写了此版本 65% 的代码。

### Aider v0.78.0

- 添加了对 OpenRouter Sonnet 3.7 思考令牌的支持。
- 由 csala 添加了在模型类型之间切换的命令：使用 `/editor-model` 切换到编辑器模型，使用 `/weak-model` 切换到弱模型。
- 添加了模型设置验证，以忽略模型不支持的 `--reasoning-effort` 和 `--thinking-tokens`。
- 添加了 `--check-model-accepts-settings` 标志（默认值：true）以强制使用不支持的模型设置。
- 在模型设置数据中注明了哪些模型支持 reasoning_effort 和 thinking_tokens 设置。
- 使用 NoInsetMarkdown 改进了 markdown 输出中代码块的渲染，增加了更好的内边距。
- 添加了 `--git-commit-verify` 标志（默认值：False）来控制是否绕过 git commit 钩子。
- 由 shladnik 修复了 `/ask`、`/code` 和 `/architect` 命令的自动完成功能。
- 由 Marco Mayer 添加了在多行模式下处于 vi 正常/导航模式时按回车键的类 vi 行为。
- 由 lentil32 添加了对 Bedrock 模型的 AWS_PROFILE 支持，允许使用 AWS 配置文件而不是显式凭证。
- 由 mopemope 增强了 `--aiderignore` 参数以解析绝对和相对路径。
- 改进了平台信息处理，优雅地处理检索错误。
- Aider 编写了此版本 92% 的代码。

### 主分支

- 添加了模型设置验证，以忽略模型不支持的 `--reasoning-effort` 和 `--thinking-tokens`。
- 添加了 `--check-model-accepts-settings` 标志（默认值：true）以强制使用不支持的模型设置。
- 在模型设置数据中注明了哪些模型支持 reasoning_effort 和 thinking_tokens 设置。
- 使用 NoInsetMarkdown 改进了 markdown 输出中代码块的渲染，增加了更好的内边距。
- 添加了 `--git-commit-verify` 标志（默认值：False）来控制是否绕过 git commit 钩子。
- Aider 编写了此版本 90% 的代码。

### Aider v0.77.1

- 更新依赖项以获取针对 Ollama 的 litellm 修复。
- 添加了对 `openrouter/google/gemma-3-27b-it` 模型的支持。
- 更新了文档的排除模式。

### Aider v0.77.0

- 通过采用 [tree-sitter-language-pack](https://github.com/Goldziher/tree-sitter-language-pack/) 大幅提升了[支持的编程语言](https://aider.chat/docs/languages.html)数量。
  - 130 种新语言支持 linter。
  - 20 种新语言支持 repo-map。
- 添加了 `/think-tokens` 命令，用于设置思考令牌预算，支持人类可读格式（8k、10.5k、0.5M）。
- 添加了 `/reasoning-effort` 命令来控制模型推理级别。
- `/think-tokens` 和 `/reasoning-effort` 命令在不带参数调用时显示当前设置。
- 在模型信息中显示思考令牌预算和推理努力程度。
- 修改了 `--thinking-tokens` 参数，使其接受带有人类可读格式的字符串值。
- 添加了 `--auto-accept-architect` 标志（默认值：true），以自动接受来自架构师代码格式的更改，无需确认。
- 添加了对 `cohere_chat/command-a-03-2025` 和 `gemini/gemma-3-27b-it` 的支持。
- 现在裸 `/drop` 命令会保留通过 args.read 提供的原始只读文件。
- 修复了一个 bug，即使在命令行中已经指定模型，默认模型也会被已弃用的 `--shortcut` 开关设置。
- 改进了 AutoCompleter，要求 3 个字符才能自动完成，以减少噪音。
- Aider 编写了此版本 72% 的代码。

### Aider v0.76.2

- 修复了加载模型缓存文件时的 JSONDecodeError 处理。
- 修复了检索 git 用户配置时的 GitCommandError 处理。
- Aider 编写了此版本 75% 的代码。

### Aider v0.76.1

- 由 Yutaka Matsubara 添加了 ignore_permission_denied 选项到文件监视器，以防止访问受限文件时出现错误。
- Aider 编写了此版本 0% 的代码。

### Aider v0.76.0

- 改进了对思考/推理模型的支持：
  - 添加了 `--thinking-tokens` CLI 选项，用于控制支持思考的模型的令牌预算。
  - 显示 LLM 返回的思考/推理内容。
  - 增强了对推理标签的处理，以更好地清理模型响应。
  - 为 `remove_reasoning` 设置添加了弃用警告，现已被 `reasoning_tag` 替代。
- Aider 将在完成最后一个请求并需要您的输入时通知您：
  - 通过 `--notifications` 标志添加了 [LLM 响应就绪时的通知](https://aider.chat/docs/usage/notifications.html)。
  - 使用 `--notifications-command` 指定桌面通知命令。
- 添加了对 QWQ 32B 的支持。
- 切换到 `tree-sitter-language-pack` 获取 tree sitter 支持。
- 改进了 EOF（Ctrl+D）在用户输入提示中的错误处理。
- 添加了帮助函数，确保十六进制颜色值带有 # 前缀。
- 修复了读取暂存文件时的 Git 错误处理。
- 改进了模型信息请求的 SSL 验证控制。
- 改进了空 LLM 响应处理，提供更清晰的警告消息。
- 由 Akira Komamura 修复了 Git 身份检索以尊重全局配置。
- 为 Bedrock 和 Vertex AI 模型提供安装依赖项的选项。
- 弃用了模型快捷参数（如 --4o、--opus），改为使用 --model 标志。
- Aider 编写了此版本 85% 的代码。

### Aider v0.75.3

- 支持 OpenRouter 上的 V3 免费版：`--model openrouter/deepseek/deepseek-chat:free`。

### Aider v0.75.2

- 在 OpenRouter、Bedrock 和 Vertex AI 上添加了对 Claude 3.7 Sonnet 模型的支持。
- 更新了 OpenRouter 上的默认模型为 Claude 3.7 Sonnet。
- 添加了对 GPT-4.5-preview 模型的支持。
- 添加了对 OpenRouter 上的 Claude 3.7 Sonnet:beta 的支持。
- 修复了某些模型的 weak_model_name 模式，使其与主模型名称模式匹配。

### Aider v0.75.1

- 添加了对 `openrouter/anthropic/claude-3.7-sonnet` 的支持。

### Aider v0.75.0

- 对 Claude 3.7 Sonnet 的基本支持
  - 使用 `--model sonnet` 来使用新的 3.7 版本
  - 思考支持即将推出
- 修复了 `/editor` 命令的 bug。
- Aider 编写了此版本 46% 的代码。

### Aider v0.74.3

- 降级 streamlit 依赖项以避免线程 bug。
- 添加了对 tree-sitter 语言包的支持。
- 添加了 openrouter/o3-mini-high 模型配置。
- 由 Lucas Shadler 添加了 build.gradle.kts 到 Kotlin 项目支持的特殊文件。

### Aider v0.74.2

- 防止多个缓存预热线程同时活跃。
- 修复了多行输入的续行提示 ". "。
- 由 Warren Krewenki 添加了 HCL (Terraform) 语法支持。

### Aider v0.74.1

- 让 o1 和 o3-mini 通过发送魔法字符串 "Formatting re-enabled." 生成 markdown。
- 修复了多行输入的 bug，不应包含 ". " 续行提示。

### Aider v0.74.0

- 动态更改 Ollama 上下文窗口以容纳当前聊天。
- 更好地支持 o3-mini、DeepSeek V3 和 R1、o1-mini、o1，尤其是通过第三方 API 提供商。
- 移除提交消息中 R1 响应的 `<think>` 标签（以及其他弱模型用途）。
- 现在可以在模型设置中指定 `use_temperature: <float>`，而不仅仅是 true/false。
- 完整的 docker 容器现在包含用于 Bedrock 的 `boto3`。
- Docker 容器现在设置 `HOME=/app`，这是正常的项目挂载点，以持久化 `~/.aider`。
- 修复了创建错误文件名（如 `python`、`php` 等）的 bug。
- 修复了 `--timeout` 的 bug。
- 修复了 `/model` 命令，现在正确报告弱模型未更改。
- 修复了多行模式在确认提示中按 ^C 后的持久性 bug。
- 监视文件现在完全忽略忽略文件中命名的顶级目录，以减少触及操作系统监视限制的可能性。有助于忽略像 `node_modules` 这样的庞大子树。
- 当更多提供商和模型元数据在本地文件中提供时，启动更快。
- 改进了 .gitignore 处理：
  - 无论如何配置，都尊重已经生效的忽略。
  - 仅在文件存在时检查 .env。
- 是/否提示现在接受全部/跳过作为 Y/N 的别名，即使不处理一组确认。
- Aider 编写了此版本 77% 的代码。

### Aider v0.73.0

- 全面支持 o3-mini：`aider --model o3-mini`
- 新的 `--reasoning-effort` 参数：low、medium、high。
- 改进了上下文窗口大小限制的处理，提供更好的消息和 Ollama 特定指导。
- 添加了通过 `remove_reasoning: tagname` 模型设置移除模型特定推理标签的支持。
- 由 xqyz 添加了自动创建父目录功能。
- 支持 OpenRouter 上的 R1 免费版：`--model openrouter/deepseek/deepseek-r1:free`
- Aider 编写了此版本 69% 的代码。

### Aider v0.72.3

- 由 miradnanali 强制执行用户/助手轮流顺序以避免 R1 错误。
- 不区分大小写的模型名称匹配，同时保留原始大小写。

### Aider v0.72.2
- 强化用户/助手轮流顺序问题的处理，以避免 R1 错误。

### Aider v0.72.1
- 修复 `openrouter/deepseek/deepseek-r1` 的模型元数据。

### Aider v0.72.0
- 支持 DeepSeek R1。
  - 使用快捷方式：`--model r1`
  - 也可通过 OpenRouter：`--model openrouter/deepseek/deepseek-r1`
- 由 Paul Walker 添加了 Kotlin 语法对 repo map 的支持。
- 由 Titusz Pan 添加了用于文件写入的 `--line-endings`。
- 为 GPT-4o 模型添加了 examples_as_sys_msg=True，提高了基准分数。
- 更新所有依赖项，以获取对 o1 系统消息的 litellm 支持。
- 修复了在反映 lint/test 错误时的轮流问题。
- Aider 编写了此版本 52% 的代码。

### Aider v0.71.1

- 修复 Docker 镜像中的权限问题。
- 添加了只读文件公告。
- 修复：Unicode 错误的 ASCII 回退。
- 修复：repomap 计算中的整数索引列表切片。

### Aider v0.71.0

- 添加提示以帮助 DeepSeek 在 `/ask` 和 `/code` 之间交替时更好地工作。
- 流式传输漂亮的 LLM 响应更平滑、更快速，尤其对长回复。
- 对不支持流式传输的模型自动关闭流式传输
  - 现在可以在 `/model o1` 和流式模型之间切换
- 即使在编辑包含三反引号围栏的文件时，也保持漂亮输出
- 裸 `/ask`、`/code` 和 `/architect` 命令现在会切换聊天模式。
- 增加了 repomap 的默认大小。
- 将最大聊天历史令牌限制从 4k 增加到 8k。
- 如果终端很简陋，则关闭花哨的输入和监视文件。
- 添加了对自定义语音格式和输入设备设置的支持。
- 由 apaz-cli 禁用了 Streamlit 电子邮件提示。
- Docker 容器以非 root 用户运行。
- 由 Aaron Weisberg 修复了 lint 命令对嵌套空格字符串的处理。
- 添加了将命令输出添加到聊天时的令牌计数反馈。
- 改进了大型音频文件的错误处理，支持自动格式转换。
- 由 Krazer 改进了 git repo 索引错误的处理。
- 改进了控制台输出中的 Unicode 处理，添加 ASCII 回退。
- 添加了对 git 错误处理的 AssertionError 和 AttributeError 支持。
- Aider 编写了此版本 60% 的代码。

### Aider v0.70.0

- 完全支持 o1 模型。
- 监视文件现在遵守 `--subtree-only`，只监视该子树。
- 改进了监视文件的提示，使其与更多模型更可靠地工作。
- 通过 uv 提供新的安装方法，包括单行安装。
- 支持 openrouter/deepseek/deepseek-chat 模型。
- 当通过 `/load` 或 `--load` 尝试交互式命令时，提供更好的错误处理。
- 如果绝对路径比相对路径短，则显示带有绝对路径的只读文件。
- 询问 10% 的用户是否选择加入分析。
- 修复了自动建议的 bug。
- 优雅处理 git 路径名中的 Unicode 错误。
- Aider 编写了此版本 74% 的代码。

### Aider v0.69.1

- 修复了模型元数据中的 gemini 模型名称。
- 当用户发表 AI 评论时显示关于 AI! 和 AI? 的提示。
- 支持在未安装 git 的情况下运行。
- 改进了 Windows 上的环境变量设置消息。

### Aider v0.69.0

- [监视文件](https://aider.chat/docs/usage/watch.html) 改进：
  - 使用 `# ... AI?` 注释触发 aider 并询问有关代码的问题。
  - 现在监视*所有*文件，而不仅仅是某些源文件。
  - 在任何文本文件中使用 `# AI comments`、`// AI comments` 或 `-- AI comments` 给 aider 指令。
- 全面支持 Gemini Flash 2.0 Exp：
  - `aider --model flash` 或 `aider --model gemini/gemini-2.0-flash-exp`
- [新的 `--multiline` 标志和 `/multiline-mode` 命令](https://aider.chat/docs/usage/commands.html#entering-multi-line-chat-messages) 由 @miradnanali 提供，使 ENTER 成为软换行，META-ENTER 发送消息。
- 在[将代码上下文复制到剪贴板](https://aider.chat/docs/usage/copypaste.html#copy-aiders-code-context-to-your-clipboard-paste-into-the-web-ui)时，`/copy-context <instructions>` 现在接受可选的"指令"。
- 改进了剪贴板错误处理，提供有用的需求安装信息。
- 询问 5% 的用户是否选择加入分析。
- `/voice` 现在允许在发送前编辑转录文本。
- 在 Y/N 提示中禁用自动完成。
- Aider 编写了此版本 68% 的代码。

### Aider v0.68.0

- [Aider 现在可与 LLM 网络聊天界面配合使用](https://aider.chat/docs/usage/copypaste.html)。
  - 新的 `--copy-paste` 模式。
  - 新的 `/copy-context` 命令。
- [从命令行或 yaml 配置文件设置所有提供商的 API 密钥和其他环境变量](https://aider.chat/docs/config/aider_conf.html#storing-llm-keys)。
  - 新的 `--api-key provider=key` 设置。
  - 新的 `--set-env VAR=value` 设置。
- 为 `--watch-files` 添加了 bash 和 zsh 支持。
- 当缺少 Gemini 和 Bedrock 模型的依赖项时提供更好的错误消息。
- Control-D 现在可以正确退出程序。
- 当 API 提供商返回硬错误时不计算令牌成本。
- 修复了使监视文件适用于没有 tree-sitter 支持的文件的 bug。
- 修复了使 o1 模型可用作弱模型的 bug。
- 更新了 shell 命令提示。
- 为所有 Coders 添加了文档字符串。
- 重新组织了命令行参数，改进了帮助消息和分组。
- 使用精确的 `sys.python` 进行自我升级。
- 添加了实验性 Gemini 模型。
- Aider 编写了此版本 71% 的代码。

### Aider v0.67.0

- [在您的 IDE 或编辑器中使用 aider](https://aider.chat/docs/usage/watch.html)。
  - 运行 `aider --watch-files`，它将监视您添加到源文件中的指令。
  - 以 "AI" 开头或结尾的单行 `# ...` 或 `// ...` 注释是给 aider 的指令。
  - 当 aider 看到 "AI!" 时，它会阅读并执行 AI 注释中的所有指令。
- 支持新的 Amazon Bedrock Nova 模型。
- 当 `/run` 或 `/test` 有非零退出代码时，在下一条消息提示中预填 "修复那个"。
- `/diff` 现在调用 `git diff` 使用您首选的差异工具。
- 添加了对进程挂起的 Ctrl-Z 支持。
- 如果奇特符号引发 unicode 错误，微调器现在会退回到 ASCII 艺术。
- `--read` 现在扩展 `~` 主目录。
- 在分析中启用异常捕获。
- [Aider 编写了此版本 61% 的代码。](https://aider.chat/HISTORY.html)

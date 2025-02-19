---
parent: 故障排除
nav_order: 10
---

# 文件编辑问题

当大语言模型（LLM）返回的代码修改无法正确应用到本地文件时，aider 可能会显示类似"Failed to apply edit to *filename*"（无法将编辑应用到文件）的错误提示。

这通常是因为 LLM 没有严格遵守系统提示的格式要求。Aider 会尽力引导 LLM 遵循正确的格式规范，并尝试自动修复那些"接近正确"的编辑格式。

当遇到此类问题时，可以尝试以下解决方案：

## 控制文件数量

尽管现在许多 LLM 支持很大的上下文窗口，但过多的无关代码或对话内容会干扰模型的判断。当上下文长度超过 25k token 后，大多数模型的格式遵循能力会显著下降。

- 仅添加需要编辑的关键文件到对话中。Aider 会自动包含[代码仓库的全局结构](https://aider.chat/docs/repomap.html)，其他相关代码会通过该机制自动引用
- 使用 `/drop` 命令移除当前不需要的文件，减少干扰因素
- 使用 `/clear` 命令清空对话历史，帮助模型集中注意力
- 使用 `/tokens` 命令查看当前各消息的 token 使用量

## 选用更强大的模型

优先考虑使用 GPT-4o（推荐）、Claude 3.5 Sonnet、DeepSeek V3 或 DeepSeek R1 等高性能模型。这些模型在格式遵循和代码理解方面表现最佳。

能力较弱的模型（特别是本地部署的小模型）往往难以严格遵守系统提示的格式要求。大多数本地模型仅能勉强配合 aider 工作，编辑错误可能难以完全避免。

## 本地模型的注意事项

使用本地模型时需特别注意：
- [Ollama 的上下文窗口设置](https://aider.chat/docs/llms/ollama.html#setting-the-context-window-size)：默认值过小，超限时会静默截断数据
- 量化模型因能力受限，更易出现编辑格式问题

## 切换完整编辑格式

如果正在使用其他编辑格式，可尝试改用完整文件编辑格式：
```bash
aider --edit-format whole
```
通过启动信息确认当前使用的编辑格式：
```
Aider v0.50.2-dev
Models: claude-3-5-sonnet-20240620 with ♾️ diff edit format
```

## 启用架构师模式

使用以下命令启用[架构师模式](../usage/modes.md#architect-mode-and-the-editor-model)：
```bash
aider --architect
```
或直接在对话中使用：
```
/chat-mode architect
```
该模式采用两阶段编辑流程：先由主模型提出修改方案，再由专用编辑模型处理文件修改。这种分工机制能显著提升编辑可靠性，特别适用于那些格式遵循能力较弱的模型。

## 更多帮助

{% include help.md %}

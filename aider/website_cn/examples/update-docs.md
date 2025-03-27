---
parent: 聊天记录示例
---
# 使用aider自动更新文档

在这个聊天记录中，用户要求根据代码中main()函数的最新版本自动更新使用文档。

<div class="chat-transcript" markdown="1">

> $ aider ./README.md aider/main.py  
> 已将README.md添加到聊天中  
> 已将aider/main.py添加到聊天中  

#### main()中的命令行参数已更新。更新readme以准确描述它们。  

```markdown
README.md
<<<<<<< ORIGINAL
- `--history-file HISTORY_FILE`: Specify the chat input history file (default: .aider.history). Override the default with the environment variable `AIDER_HISTORY_FILE`.
- `--model MODEL`: Specify the model to use for the main chat (default: gpt-4). Override the default with the environment variable `AIDER_MODEL`.
- `-3`: Use gpt-3.5-turbo model for the main chat (basically won't work). No environment variable override.
- `--no-pretty`: Disable pretty, colorized output. Override the default with the environment variable `AIDER_PRETTY` (default: 1 for enabled, 0 for disabled).
- `--show-diffs`: Show diffs when committing changes (default: False). Override the default with the environment variable `AIDER_SHOW_DIFFS` (default: 0 for False, 1 for True).
- `--no-auto-commits`: Disable auto commit of changes. Override the default with the environment variable `AIDER_AUTO_COMMITS` (default: 1 for enabled, 0 for disabled).
=======
- `--input-history-file INPUT_HISTORY_FILE`: Specify the chat input history file (default: .aider.input.history). Override the default with the environment variable `AIDER_INPUT_HISTORY_FILE`.
- `--chat-history-file CHAT_HISTORY_FILE`: Specify the chat history file (default: .aider.chat.history.md). Override the default with the environment variable `AIDER_CHAT_HISTORY_FILE`.
- `--model MODEL`: Specify the model to use for the main chat (default: gpt-4). Override the default with the environment variable `AIDER_MODEL`.
- `-3`: Use gpt-3.5-turbo model for the main chat (basically won't work). No environment variable override.
- `--no-pretty`: Disable pretty, colorized output. Override the default with the environment variable `AIDER_PRETTY` (default: 1 for enabled, 0 for disabled).
- `--apply FILE`: Apply the changes from the given file instead of running the chat (debug).
- `--no-auto-commits`: Disable auto commit of changes. Override the default with the environment variable `AIDER_AUTO_COMMITS` (default: 1 for enabled, 0 for disabled).
- `--show-diffs`: Show diffs when committing changes (default: False). Override the default with the environment variable `AIDER_SHOW_DIFFS` (default: 0 for False, 1 for True).
- `--yes`: Always say yes to every confirmation (default: False).
>>>>>>> UPDATED
```

> 已应用编辑到README.md  
> 提交024f45e aider: 更新了main()中的命令行参数并更新README.md以准确描述它们。  

</div>

---
parent: 更多信息
nav_order: 400
description: 你可以通过命令行或Python脚本对aider进行脚本化操作。
---

# 脚本化Aider

你可以通过命令行或Python脚本对aider进行脚本化操作。

## 命令行

Aider接受`--message`参数，你可以用它提供自然语言指令。aider会执行该指令，将修改应用到文件后退出。例如：

```bash
aider --message "写一个打印hello的脚本" hello.js
```

或者编写简单的shell脚本对多个文件应用相同指令：

```bash
for FILE in *.py ; do
    aider --message "为所有函数添加描述性文档字符串" $FILE
done
```

使用`aider --help`查看所有[命令行选项](/docs/config/options.html)，这些选项对脚本编写特别有用：

```
--stream, --no-stream
                      启用/禁用流式响应（默认：True）[环境变量：
                      AIDER_STREAM]
--message COMMAND, --msg COMMAND, -m COMMAND
                      指定要发送给GPT的单个消息，处理回复后退出
                      （禁用聊天模式）[环境变量: AIDER_MESSAGE]
--message-file MESSAGE_FILE, -f MESSAGE_FILE
                      指定包含要发送给GPT消息的文件，处理回复后退出
                      （禁用聊天模式）[环境变量: AIDER_MESSAGE_FILE]
--yes                 始终确认所有提示[环境变量: AIDER_YES]
--auto-commits, --no-auto-commits
                      启用/禁用GPT修改的自动提交（默认：True）[环境变量:
                      AIDER_AUTO_COMMITS]
--dirty-commits, --no-dirty-commits
                      启用/禁用仓库不洁时的提交（默认：True）[环境变量:
                      AIDER_DIRTY_COMMITS]
--dry-run, --no-dry-run
                      执行试运行不实际修改文件（默认：False）[环境变量:
                      AIDER_DRY_RUN]
--commit              使用合适的提交信息提交所有暂存变更，然后退出
                      [环境变量: AIDER_COMMIT]
```

## Python

你也可以通过Python脚本操作aider：

```python
from aider.coders import Coder
from aider.models import Model

# 这是要添加到聊天中的文件列表
fnames = ["greeting.py"]

model = Model("gpt-4-turbo")

# 创建编码器对象
coder = Coder.create(main_model=model, fnames=fnames)

# 执行一个指令并返回
coder.run("写一个打印hello world的脚本")

# 发送另一个指令
coder.run("改成说goodbye")

# 也可以执行聊天中的"/"命令
coder.run("/tokens")

```

查看[Coder.create()和Coder.__init__()方法](https://github.com/Aider-AI/aider/blob/main/aider/coders/base_coder.py)了解所有支持的参数。

可以通过以下方式设置等效于`--yes`的参数：

```python
from aider.io import InputOutput
io = InputOutput(yes=True)
# ...
coder = Coder.create(model=model, fnames=fnames, io=io)
```

{: .note }
Python脚本API尚未官方支持或文档化，未来版本可能不兼容变更。

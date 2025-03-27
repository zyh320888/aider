---
parent: 聊天记录示例
---

# 遵守NO_COLOR环境变量

用户将[no-color.org](https://no-color.org)网站上的NO_COLOR环境变量协议规范粘贴到aider聊天中。

Aider找出需要编辑的文件，并请求许可进行更改。
然后，如果设置了NO_COLOR，它会禁用所有颜色和美化打印功能，使工具符合规范。

然后用户要求添加一个测试用例，aider也添加了这个测试用例。

<div class="chat-transcript" markdown="1">

> $ aider  
> 使用git仓库: .git  
> 使用/help查看聊天内容命令。  

#### 默认情况下向其输出添加ANSI颜色的命令行软件应检查NO_COLOR环境变量，当该变量存在且不为空字符串（无论其值如何）时，应防止添加ANSI颜色。  

要实现此功能，我们需要修改`aider/io.py`文件。请将其设为*可读写*，以便我提供必要的更改。

> aider/io.py  
> 将这些文件添加到聊天中？y  

很好！现在，我将进行必要的更改，以检查`NO_COLOR`环境变量，并在其存在且不为空字符串时禁用ANSI颜色。

```python
aider/io.py
<<<<<<< ORIGINAL
import os
=======
import os
import os.path
>>>>>>> UPDATED
```

```python
aider/io.py
<<<<<<< ORIGINAL
    def __init__(
        self,
        pretty=True,
        yes=False,
        input_history_file=None,
        chat_history_file=None,
        input=None,
        output=None,
        user_input_color="blue",
        tool_output_color=None,
        tool_error_color="red",
    ):
        self.user_input_color = user_input_color
        self.tool_output_color = tool_output_color
        self.tool_error_color = tool_error_color
        self.input = input
        self.output = output
        self.pretty = pretty
        self.yes = yes
        self.input_history_file = input_history_file
        if chat_history_file is not None:
            self.chat_history_file = Path(chat_history_file)
        else:
            self.chat_history_file = None

        if pretty:
            self.console = Console()
        else:
            self.console = Console(force_terminal=True, no_color=True)
=======
    def __init__(
        self,
        pretty=True,
        yes=False,
        input_history_file=None,
        chat_history_file=None,
        input=None,
        output=None,
        user_input_color="blue",
        tool_output_color=None,
        tool_error_color="red",
    ):
        no_color = os.environ.get("NO_COLOR")
        if no_color is not None and no_color != "":
            pretty = False

        self.user_input_color = user_input_color if pretty else None
        self.tool_output_color = tool_output_color if pretty else None
        self.tool_error_color = tool_error_color if pretty else None
        self.input = input
        self.output = output
        self.pretty = pretty
        self.yes = yes
        self.input_history_file = input_history_file
        if chat_history_file is not None:
            self.chat_history_file = Path(chat_history_file)
        else:
            self.chat_history_file = None

        self.console = Console(force_terminal=not pretty, no_color=not pretty)
>>>>>>> UPDATED
```

这些更改将使软件检查`NO_COLOR`环境变量，并在该变量存在且不为空字符串时禁用ANSI颜色。

> 已应用编辑到aider/io.py  
> 已应用编辑到aider/io.py  
> 提交3218242 aider: 添加了对NO_COLOR环境变量的检查以禁用ANSI颜色。  

</div>
<div class="chat-transcript" markdown="1">
#### 添加一个测试

为了添加`NO_COLOR`环境变量的测试，我们将在`tests/test_io.py`文件中创建一个新的测试函数。由于这个文件不存在，我们将首先创建它。

```python
tests/test_io.py
<<<<<<< ORIGINAL
=======
import os
import unittest
from unittest.mock import patch
from aider.io import InputOutput

class TestInputOutput(unittest.TestCase):
    def test_no_color_environment_variable(self):
        with patch.dict(os.environ, {"NO_COLOR": "1"}):
            io = InputOutput()
            self.assertFalse(io.pretty)

if __name__ == "__main__":
    unittest.main()
>>>>>>> UPDATED
```

这个测试函数检查当设置`NO_COLOR`环境变量时，`InputOutput`类的`pretty`属性是否设置为`False`。

> 允许创建新文件tests/test_io.py？y  
> 将tests/test_io.py添加到git？y  
> 已应用编辑到tests/test_io.py  
> 提交52a9df5 aider: 添加了一个测试函数，用于检查当设置`NO_COLOR`环境变量时，`InputOutput`类的`pretty`属性是否设置为`False`。  

</div>
<div class="chat-transcript" markdown="1">
#### /run pytest

> ============================= test session starts ==============================  
> platform darwin -- Python 3.11.3, pytest-7.3.1, pluggy-1.0.0  
> rootdir: /Users/gauthier/Projects/aider  
> collected 25 items  
>   
> tests/test_coder.py ......                                               [ 24%]  
> tests/test_commands.py .                                                 [ 28%]  
> tests/test_io.py .                                                       [ 32%]  
> tests/test_main.py ....                                                  [ 48%]  
> tests/test_repomap.py ...                                                [ 60%]  
> tests/test_utils.py ..........                                           [100%]  
>   
> ============================== 25 passed in 1.41s ==============================
>  
> 将输出添加到聊天中？y


</div>

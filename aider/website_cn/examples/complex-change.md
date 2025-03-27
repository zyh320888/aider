---
parent: 聊天记录示例
nav_order: 3
---

# 复杂的多文件更改，包含调试过程

这是一个相当复杂的代码更改的聊天记录。用户尝试更新测试以使用`prompt_toolkit`提供的输入模拟。这需要对多个源文件进行更改。

一些值得注意的事项：
  - 初始更改未能正常工作，因此用户提供错误消息和`prompt_toolkit`文档的片段，协作调试并解决问题。
  - 用户使用编辑器在聊天外部编辑文件。`aider`注意到这些带外更改并提供提交它们的选项。
  - 在某一点，用户按下`^C`中断LLM响应，因为它不是一个有用的回应。用户提供澄清，并在下一个回复中获得更好的结果。

<div class="chat-transcript" markdown="1">

> $ aider tests/test_main.py aider/getinput.py  
> 已将tests/test_main.py添加到聊天中  
> 已将aider/getinput.py添加到聊天中  

#### 在main测试中，我们能否使用prompt_toolkit输入模拟函数，而不是使用/dev/null发送无输入？  

是的，我们可以使用`prompt_toolkit.input`模块来模拟测试中的输入。以下是如何修改`tests/test_main.py`文件：

```python
tests/test_main.py
<<<<<<< ORIGINAL
import os
import sys
import tempfile
from unittest import TestCase
from aider.main import main
import subprocess
=======
import os
import tempfile
from unittest import TestCase
from aider.main import main
import subprocess
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput
>>>>>>> UPDATED
```

现在，更新测试以使用`create_pipe_input`和`DummyOutput`：

```python
tests/test_main.py
<<<<<<< ORIGINAL
            with open(os.devnull, "r") as dev_null:
                save_stdin = sys.stdin
                sys.stdin = dev_null
                main([])
                sys.stdin = save_stdin
=======
            pipe_input = create_pipe_input()
            save_stdin = sys.stdin
            sys.stdin = pipe_input
            main([], input=pipe_input, output=DummyOutput())
            sys.stdin = save_stdin
            pipe_input.close()
>>>>>>> UPDATED
```

```python
tests/test_main.py
<<<<<<< ORIGINAL
            with open(os.devnull, "r") as dev_null:
                save_stdin = sys.stdin
                sys.stdin = dev_null
                main(["foo.txt"])
                sys.stdin = save_stdin
                self.assertTrue(os.path.exists("foo.txt"))
=======
            pipe_input = create_pipe_input()
            save_stdin = sys.stdin
            sys.stdin = pipe_input
            main(["foo.txt"], input=pipe_input, output=DummyOutput())
            sys.stdin = save_stdin
            pipe_input.close()
            self.assertTrue(os.path.exists("foo.txt"))
>>>>>>> UPDATED
```

```python
tests/test_main.py
<<<<<<< ORIGINAL
            with open(os.devnull, "r") as dev_null:
                save_stdin = sys.stdin
                sys.stdin = dev_null
                main(["--yes", "foo.txt"])
                sys.stdin = save_stdin
                self.assertTrue(os.path.exists("foo.txt"))
=======
            pipe_input = create_pipe_input()
            save_stdin = sys.stdin
            sys.stdin = pipe_input
            main(["--yes", "foo.txt"], input=pipe_input, output=DummyOutput())
            sys.stdin = save_stdin
            pipe_input.close()
            self.assertTrue(os.path.exists("foo.txt"))
>>>>>>> UPDATED
```

这些更改将使用`prompt_toolkit`的输入模拟函数替代`/dev/null`的使用。

> 已应用编辑到tests/test_main.py  
> 已应用编辑到tests/test_main.py  
> 已应用编辑到tests/test_main.py  
> 已应用编辑到tests/test_main.py  
> 提交c177e29 aider: 在测试中用prompt_toolkit的输入模拟函数替代了/dev/null的使用。  


> Git 仓库有未提交的更改。  
> 建议的提交消息：  
> 在test_main.py中添加了sys模块的导入语句。  
> 在聊天继续之前提交 [y/n/commit message]? y  
> 提交6724fcd 在test_main.py中添加了sys模块的导入语句。  


</div>
<div class="chat-transcript" markdown="1">
#### /add aider/main.py  

> 已将aider/main.py添加到聊天中  


#### 我收到这个错误：FAILED tests/test_main.py::TestMain::test_main_with_empty_git_dir_new_file - TypeError: main() got an unexpected keyword argument 'input'  

我为造成的混淆道歉。看来我在`aider/main.py`中的`main()`函数定义中犯了一个错误。`main()`函数应该接受`input`和`output`关键字参数。以下是修复方法：

```python
aider/main.py
<<<<<<< ORIGINAL
def main(args=None):
    if args is None:
        args = sys.argv[1:]
=======
def main(args=None, input=None, output=None):
    if args is None:
        args = sys.argv[1:]
    if input is None:
        input = sys.stdin
    if output is None:
        output = sys.stdout
>>>>>>> UPDATED
```

现在，`main()`函数将接受`input`和`output`关键字参数，测试应该能通过了。

> 已应用编辑到aider/main.py  
> 提交79dfba9 aider: 修复main()函数以接受input和output关键字参数。  

</div>
<div class="chat-transcript" markdown="1">
#### 我们需要将这些传递给InputOutput和prompt_toolkit，对吧？  

是的，您说得对。我们需要将`input`和`output`参数传递给`InputOutput`类，然后传递给`prompt_toolkit.prompt()`函数。以下是如何修改`aider/getinput.py`和`aider/main.py`文件：

在`aider/getinput.py`中，更新`InputOutput`类以接受`input`和`output`参数：

```python
aider/getinput.py
<<<<<<< ORIGINAL
class InputOutput:
    def __init__(self, pretty, yes, input_history_file, chat_history_file):
=======
class InputOutput:
    def __init__(self, pretty, yes, input_history_file, chat_history_file, input=None, output=None):
        self.input = input
        self.output = output
>>>>>>> UPDATED
```

现在，更新`get_input()`方法中的`prompt()`函数调用，以使用`input`和`output`参数：

```python
aider/getinput.py
<<<<<<< ORIGINAL
            line = prompt(
                show,
                completer=completer_instance,
                history=FileHistory(self.input_history_file),
                style=style,
                reserve_space_for_menu=4,
                complete_style=CompleteStyle.MULTI_COLUMN,
            )
=======
            line = prompt(
                show,
                completer=completer_instance,
                history=FileHistory(self.input_history_file),
                style=style,
                reserve_space_for_menu=4,
                complete_style=CompleteStyle.MULTI_COLUMN,
                input=self.input,
                output=self.output,
            )
>>>>>>> UPDATED
```

在`aider/main.py`中，将`input`和`output`参数传递给`InputOutput`类：

```python
aider/main.py
<<<<<<< ORIGINAL
    io = InputOutput(args.pretty, args.yes, args.input_history_file, args.chat_history_file)
=======
    io = InputOutput(args.pretty, args.yes, args.input_history_file, args.chat_history_file, input=input, output=output)
>>>>>>> UPDATED
```

这些更改将确保`input`和`output`参数被传递给`InputOutput`类，然后传递给`prompt_toolkit.prompt()`函数。

> 已应用编辑到aider/getinput.py  
> 已应用编辑到aider/getinput.py  
> 已应用编辑到aider/main.py  
> 提交cea9d2a aider: 更新InputOutput类以接受input和output参数，并将它们传递给prompt_toolkit.prompt()函数。  

</div>
<div class="chat-transcript" markdown="1">
#### FAILED tests/test_main.py::TestMain::test_main_with_empty_git_dir_new_file - TypeError: prompt() got an unexpected keyword argument 'input'  

我为造成的混淆道歉。看来我在`prompt_toolkit.prompt()`函数调用中犯了一个错误。`prompt()`函数接受`stdin`和`stdout`参数，而不是`input`和`output`。以下是修复方法：

更新`aider/getinput.py`中`get_input()`方法中的`prompt()`函数调用：

```python
aider/getinput.py
<<<<<<< ORIGINAL
            input=self.input,
            output=self.output,
=======
            stdin=self.input,
            stdout=self.output,
>>>>>>> UPDATED
```

这些更改将确保`input`和`output`参数被正确地传递给`prompt_toolkit.prompt()`函数。

> 已应用编辑到aider/getinput.py  
> 提交55d3540 aider: 修复`get_input()`方法中的`prompt()`函数调用，传递`stdin`和`stdout`参数，而不是`input`和`output`。  

</div>
<div class="chat-transcript" markdown="1">
#### prompt_toolkit.shortcuts.prompt(message: AnyFormattedText | None = None, *, history: History | None = None, editing_mode: EditingMode | None = None, refresh_interval: float | None = None, vi_mode: bool | None = None, lexer: Lexer | None = None, completer: Completer | None = None, complete_in_thread: bool | None = None, is_password: bool | None = None, key_bindings: KeyBindingsBase | None = None, bottom_toolbar: AnyFormattedText | None = None, style: BaseStyle | None = None, color_depth: ColorDepth | None = None, cursor: AnyCursorShapeConfig = None, include_default_pygments_style: FilterOrBool | None = None, style_transformation: StyleTransformation | None = None, swap_light_and_dark_colors: FilterOrBool | None = None, rprompt: AnyFormattedText | None = None, multiline: FilterOrBool | None = None, prompt_continuation: PromptContinuationText | None = None, wrap_lines: FilterOrBool | None = None, enable_history_search: FilterOrBool | None = None, search_ignore_case: FilterOrBool | None = None, complete_while_typing: FilterOrBool | None = None, validate_while_typing: FilterOrBool | None = None, complete_style: CompleteStyle | None = None, auto_suggest: AutoSuggest | None = None, validator: Validator | None = None, clipboard: Clipboard | None = None, mouse_support: FilterOrBool | None = None, input_processors: list[Processor] | None = None, placeholder: AnyFormattedText | None = None, reserve_space_for_menu: int | None = None, enable_system_prompt: FilterOrBool | None = None, enable_suspend: FilterOrBool | None = None, enable_open_in_editor: FilterOrBool | None = None, tempfile_suffix: str | Callable[[], str] | None = None, tempfile: str | Callable[[], str] | None = None, default: str = '', accept_default: bool = False, pre_run: Callable[[], None] | None = None) → str  

我为之前的混淆道歉。看来`prompt_toolkit.prompt()`函数不直接接受`stdin`和`stdout`参数。相反，我们需要使用`prompt_toolkit`中的`Application`类创建一个具有所需输入和输出的自定义应用程序。以下是如何修改`aider/getinput.py`文件：

首先，导入必要的类和函数从`prompt_tool

> ^C 键盘中断  

</div>
<div class="chat-transcript" markdown="1">
#### class prompt_toolkit.shortcuts.PromptSession(message: AnyFormattedText = '', *, multiline: FilterOrBool = False, wrap_lines: FilterOrBool = True, is_password: FilterOrBool = False, vi_mode: bool = False, editing_mode: EditingMode = <EditingMode.EMACS: 'EMACS'>, complete_while_typing: FilterOrBool = True, validate_while_typing: FilterOrBool = True, enable_history_search: FilterOrBool = False, search_ignore_case: FilterOrBool = False, lexer: Lexer | None = None, enable_system_prompt: FilterOrBool = False, enable_suspend: FilterOrBool = False, enable_open_in_editor: FilterOrBool = False, validator: Validator | None = None, completer: Completer | None = None, complete_in_thread: bool = False, reserve_space_for_menu: int = 8, complete_style: CompleteStyle = <CompleteStyle.COLUMN: 'COLUMN'>, auto_suggest: AutoSuggest | None = None, style: BaseStyle | None = None, style_transformation: StyleTransformation | None = None, swap_light_and_dark_colors: FilterOrBool = False, color_depth: ColorDepth | None = None, cursor: AnyCursorShapeConfig = None, include_default_pygments_style: FilterOrBool = True, history: History | None = None, clipboard: Clipboard | None = None, prompt_continuation: PromptContinuationText | None = None, rprompt: AnyFormattedText = None, bottom_toolbar: AnyFormattedText = None, mouse_support: FilterOrBool = False, input_processors: list[Processor] | None = None, placeholder: AnyFormattedText | None = None, key_bindings: KeyBindingsBase | None = None, erase_when_done: bool = False, tempfile_suffix: str | Callable[[], str] | None = '.txt', tempfile: str | Callable[[], str] | None = None, refresh_interval: float = 0, input: Input | None = None, output: Output | None = None)  

感谢您提供`PromptSession`类信息。我们可以使用`PromptSession`类创建一个具有所需输入和输出的自定义会话。以下是如何修改`aider/getinput.py`文件：

首先，从`prompt_toolkit.shortcuts`导入`PromptSession`类：

```python
aider/getinput.py
<<<<<<< ORIGINAL
from prompt_toolkit import prompt
=======
from prompt_toolkit.shortcuts import PromptSession
>>>>>>> UPDATED
```

现在，更新`get_input()`方法以使用`PromptSession`类：

```python
aider/getinput.py
<<<<<<< ORIGINAL
            line = prompt(
                show,
                completer=completer_instance,
                history=FileHistory(self.input_history_file),
                style=style,
                reserve_space_for_menu=4,
                complete_style=CompleteStyle.MULTI_COLUMN,
                input=self.input,
                output=self.output,
            )
=======
            session = PromptSession(
                message=show,
                completer=completer_instance,
                history=FileHistory(self.input_history_file),
                style=style,
                reserve_space_for_menu=4,
                complete_style=CompleteStyle.MULTI_COLUMN,
                input=self.input,
                output=self.output,
            )
            line = session.prompt()
>>>>>>> UPDATED
```

这些更改将确保`input`和`output`参数被正确地传递给`prompt_toolkit`的`PromptSession`类。

> 已应用编辑到aider/getinput.py  
> 已应用编辑到aider/getinput.py  
> 提交ac92cca aider: 用`PromptSession()`替换`prompt()`，以正确传递input和output参数。  

</div>
<div class="chat-transcript" markdown="1">
#### 在测试中尝试使用create_input(StringIO(''))  


我理解您想在测试中使用`create_input(StringIO(''))`。但是，我需要更多关于您想将此更改应用到哪些测试用例以及如何使用它的信息。请提供更多详细信息或示例。


#### 那些当前使用create_pipe_input()的  

我明白您想将`create_pipe_input()`替换为`create_input(StringIO(''))`在测试用例中。以下是对`tests/test_main.py`文件的更改：

```python
tests/test_main.py
<<<<<<< ORIGINAL
from prompt_toolkit.input import create_pipe_input
=======
from prompt_toolkit.input import create_input
from io import StringIO
>>>>>>> UPDATED
```

```python
tests/test_main.py
<<<<<<< ORIGINAL
            pipe_input = create_pipe_input()
=======
            pipe_input = create_input(StringIO(''))
>>>>>>> UPDATED
```

```python
tests/test_main.py
<<<<<<< ORIGINAL
            pipe_input = create_pipe_input()
=======
            pipe_input = create_input(StringIO(''))
>>>>>>> UPDATED
```

```python
tests/test_main.py
<<<<<<< ORIGINAL
            pipe_input = create_pipe_input()
=======
            pipe_input = create_input(StringIO(''))
>>>>>>> UPDATED
```

这些更改将在测试用例中用`create_input(StringIO(''))`替换`create_pipe_input()`的使用。

> 已应用编辑到tests/test_main.py  
> 已应用编辑到tests/test_main.py  
> 已应用编辑到tests/test_main.py  
> 已应用编辑到tests/test_main.py  
> 提交4bb043f aider: 在测试用例中用`create_input(StringIO(''))`替换了`create_pipe_input()`的使用。  

</div>
<div class="chat-transcript" markdown="1">
#### 很好，这样可以了！  

我很高兴这些更改对您有效！如果您有任何其他请求或需要进一步的帮助，请随时提问。


</div>

---
parent: 聊天记录示例
nav_order: 4
---

# 创建"黑盒"测试用例

这个记录展示了aider创建黑盒测试用例的过程，**在没有访问被测试函数源代码或仓库中任何其他代码的情况下**。

相反，aider完全依靠[基于ctags的仓库高级地图](https://aider.chat/docs/ctags.html)来操作，该地图提供了仓库中所有符号和函数签名的详细信息。仅使用地图中的元数据，LLM能够弄清楚如何调用要测试的方法，以及如何实例化测试准备所需的多个类对象。

具体来说，aider能够利用仓库地图来：

  - 找到用户想要测试的`cmd_add()`函数的函数签名。
  - 确定它是`Command`类的一个方法，因此测试用例需要实例化一个实例来进行测试。
  - 识别创建`Command`实例需要传入`InputOutput`和`Coder`实例。
  - 确定实例化`InputOutput`实例所需的参数。
  - 决定`Coder`类看起来足够复杂，可以使用`MagickMock`。

`cmd_add()`方法的定义没有类型注解，因此aider做出了合理但不正确的猜测，认为它接受文件的`list`。用户调用`/run`命令来运行新的单元测试，这基于这种误解抛出了一个错误。

LLM审查了错误消息，并修复了对`cmd_add()`的调用，正确地传递了一个包含以空格分隔的文件名列表的`str`。测试随后在下一次`/run`中通过。

<div class="chat-transcript" markdown="1">

> $ aider tests/test_commands.py  
> 创建空文件tests/test_commands.py  
> 已将tests/test_commands.py添加到聊天中  
> 文件未在.git中跟踪：  
> - tests/test_commands.py  
>  
> 添加它们？y  
> 已将tests/test_commands.py添加到git仓库  
> 提交b9cea2c 已将新文件添加到git仓库：tests/test_commands.py  
> 使用git仓库：.git  

#### 添加一个测试cmd_add的测试，传入'foo.txt'和'bar.txt'，并确保测试后它们都已创建。在临时目录中运行测试。  

我将在`tests/test_commands.py`文件中添加一个名为`test_cmd_add`的新测试方法。这个测试将创建一个临时目录，将当前工作目录更改为该临时目录，然后以'foo.txt'和'bar.txt'作为参数调用`cmd_add`方法。之后，它将检查这两个文件是否已在临时目录中创建。

这是代码更改：

```python
tests/test_commands.py
<<<<<<< ORIGINAL
=======
import os
import tempfile
from unittest import TestCase
from unittest.mock import MagicMock
from aider.commands import Commands
from aider.io import InputOutput

class TestCommands(TestCase):
    def test_cmd_add(self):
        # Create a temporary directory and change the current working directory
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)

            # Initialize the Commands and InputOutput objects
            io = InputOutput(pretty=False, yes=True)
            coder = MagicMock()
            commands = Commands(io, coder)

            # Call the cmd_add method with 'foo.txt' and 'bar.txt'
            commands.cmd_add(["foo.txt", "bar.txt"])

            # Check if both files have been created in the temporary directory
            self.assertTrue(os.path.exists("foo.txt"))
            self.assertTrue(os.path.exists("bar.txt"))
>>>>>>> UPDATED
```

这个测试将确保`cmd_add`方法在当前工作目录中创建指定的文件。

> 已应用编辑到tests/test_commands.py  
> 提交e2d5212 aider: 添加了一个测试方法`test_cmd_add`，它创建一个临时目录，使用'foo.txt'和'bar.txt'调用`cmd_add`方法，并检查这两个文件是否已在临时目录中创建。  

</div>
<div class="chat-transcript" markdown="1">
#### /run pytest tests/test_commands.py

> ```  
> ============================= test session starts ==============================  
> platform darwin -- Python 3.11.3, pytest-7.3.1, pluggy-1.0.0  
> rootdir: /Users/gauthier/Projects/aider  
> collected 1 item  
>   
> tests/test_commands.py F                                                 [100%]  
>   
> =================================== FAILURES ===================================  
> __________________________ TestCommands.test_cmd_add ___________________________  
>   
> self = <tests.test_commands.TestCommands testMethod=test_cmd_add>  
>   
>     def test_cmd_add(self):  
>         # Create a temporary directory and change the current working directory  
>         with tempfile.TemporaryDirectory() as tmpdir:  
>             os.chdir(tmpdir)  
>   
>             # Initialize the Commands and InputOutput objects  
>             io = InputOutput(pretty=False, yes=True)  
>             coder = MagicMock()  
>             commands = Commands(io, coder)  
>   
>             # Call the cmd_add method with 'foo.txt' and 'bar.txt'  
> >           commands.cmd_add(["foo.txt", "bar.txt"])  
>   
> /Users/gauthier/Projects/aider/tests/test_commands.py:20:  
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _  
>   
> self = <aider.commands.Commands object at 0x10b412b50>  
> args = ['foo.txt', 'bar.txt']  
>   
>     def cmd_add(self, args):  
>         "Add matching files to the chat session"  
>   
>         added_fnames = []  
>         files = self.coder.get_all_relative_files()  
> >       for word in args.split():  
> E       AttributeError: 'list' object has no attribute 'split'  
>   
> /Users/gauthier/Projects/aider/aider/commands.py:161: AttributeError  
> =========================== short test summary info ============================  
> FAILED tests/test_commands.py::TestCommands::test_cmd_add - AttributeError: '...  
> ============================== 1 failed in 0.34s ===============================  
> ```  
>
> 将输出添加到聊天中？[y/n] (y): y  

看起来`aider/commands.py`中的`cmd_add`方法需要一个字符串作为输入，但在测试中，我们传递的是一个列表。我将更新测试以传递字符串而不是列表。

这是代码更改：

```python
tests/test_commands.py
<<<<<<< ORIGINAL
            # Call the cmd_add method with 'foo.txt' and 'bar.txt'
            commands.cmd_add(["foo.txt", "bar.txt"])
=======
            # Call the cmd_add method with 'foo.txt' and 'bar.txt' as a single string
            commands.cmd_add("foo.txt bar.txt")
>>>>>>> UPDATED
```

现在，使用更新后的测试方法再次运行测试：

```
pytest tests/test_commands.py
```

> 已应用编辑到tests/test_commands.py  
> 提交d1551b4 aider: 更新测试，在调用`cmd_add`方法时传递字符串而不是列表。  

</div>
<div class="chat-transcript" markdown="1">
#### /run pytest tests/test_commands.py

> ```  
> ============================= test session starts ==============================  
> platform darwin -- Python 3.11.3, pytest-7.3.1, pluggy-1.0.0  
> rootdir: /Users/gauthier/Projects/aider  
> collected 1 item  
>   
> tests/test_commands.py .                                                 [100%]  
>   
> ============================== 1 passed in 0.38s ===============================  
> ```  

</div>

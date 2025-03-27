---
parent: 聊天记录示例
---

# 使用aider编辑asciinema投射文件

用户需要对`asciinema`屏幕录制文件中的转义序列进行一些繁琐的编辑。

<div class="chat-transcript" markdown="1">

> $ aider hello.cast  
> 已将hello.cast添加到聊天中  

#### 当"hello.py> "提示符显示时，它包含了一些转义代码，用于在提示符下方添加几个空行，然后将光标带回上方。删除所有这些内容。只显示提示符后跟一个空格，并在之后留下光标显示。  

```python
hello.cast
<<<<<<< ORIGINAL
[19.534013, "o", "\u001b[?2004h\u001b[?1l\u001b[?25l\u001b[0m\u001b[?7l\u001b[0m\u001b[J\u001b[0;38;5;28mhello.py>  \u001b[0m\r\r\n\r\r\n\r\r\n\u001b[0;38;5;28m                                                                \r\u001b[64C \r\u001b[3A\u001b[10C\u001b[?7h\u001b[0m\u001b[?12l\u001b[?25h"]
=======
[19.534013, "o", "\u001b[?2004h\u001b[?1l\u001b[?25l\u001b[0m\u001b[?7l\u001b[0m\u001b[J\u001b[0;38;5;28mhello.py> \u001b[0m\u001b[?7h\u001b[0m\u001b[?12l\u001b[?25h"]
>>>>>>> UPDATED
```

> 已应用编辑到hello.cast  
> 提交a3fa4d2 aider: 删除转义代码以正确显示提示符和光标。  


</div>

---
title: 使用ctags提升GPT-4对代码库的理解
excerpt: 使用ctags构建"代码库地图"以增强GPT-4理解大型代码库的能力。
highlight_image: /assets/robot-flowchart.png
nav_exclude: true
---
{% if page.date %}
<p class="post-date">{{ page.date | date: "%B %d, %Y" }}</p>
{% endif %}

# 使用ctags提升GPT-4对代码库的理解

![机器人流程图](/assets/robot-flowchart.png)


## 更新

Aider不再使用ctags构建代码库地图。
请参阅关于
[使用tree-sitter构建更好的代码库地图](https://aider.chat/docs/repomap.html)
的较新文章。

-------

GPT-4在"自包含"的编码任务中非常有用，
比如生成全新代码或修改没有依赖关系的纯函数。

但使用GPT-4修改或扩展
大型、复杂的现有代码库是困难的。
要修改这样的代码，GPT需要理解连接其子系统的依赖关系和API。
我们需要在要求GPT完成编码任务时以某种方式提供这种"代码上下文"。具体来说，我们需要：

  - 帮助GPT理解整个代码库，使其
能够理解具有复杂依赖关系的代码的含义，并生成
尊重和利用现有抽象的新代码。
  - 以高效方式向GPT传递所有这些"代码上下文"，
使其适合8k-token的上下文窗口。

为解决这些问题，`aider`现在
向GPT发送**整个git仓库的简洁地图**，
其中包括
所有声明的变量和带有调用签名的函数。
这个*代码库地图*是使用`ctags`自动构建的，后者
从源文件中提取符号定义。历史上，
ctags由IDE和编辑器生成和索引，以
帮助人类搜索和导航大型代码库。
相反，我们将使用ctags帮助GPT更好地理解、导航
和编辑更大代码库中的代码。

要了解这有多有效，这个
[聊天记录](https://aider.chat/examples/add-test.html)
展示了GPT-4创建黑盒测试用例，**而没有给予它
被测试函数的源代码或仓库中任何其他
代码的访问权限。**
仅使用代码库地图中的元数据，GPT能够弄清楚如何
调用要测试的方法，以及如何实例化多个
为测试做准备所需的类对象。

要使用本文讨论的技术与GPT-4一起编码：


  - 安装[aider](https://aider.chat/docs/install.html)。
  - 安装universal ctags。
  - 在您的仓库内运行`aider`，它应该显示"Repo-map: universal-ctags using 1024 tokens"。

## 问题：代码上下文

GPT-4在"自包含"的编码任务中表现出色，如编写或
修改没有外部依赖的纯函数。
GPT可以轻松处理像"编写
斐波那契函数"或"使用列表
推导式重写循环"这样的请求，因为它们不需要讨论中代码之外的上下文。

大多数实际代码并非纯粹和自包含的，它与
仓库中许多不同文件的代码交织在一起并依赖于它们。
如果您要求GPT"将Foo类中的所有print语句切换为
使用BarLog日志系统"，它需要看到带有
print语句的Foo类代码，同时还需要理解项目的BarLog
子系统。

一个简单的解决方案是**发送整个代码库**给GPT，连同
每个变更请求。现在GPT拥有所有上下文！但这对于即使是
中等规模的仓库也行不通，因为它们无法适应8k-token的上下文窗口。

一个更好的方法是有选择性，
**手动选择要发送的文件**。
对于上面的例子，您可以发送包含
Foo类的文件和包含BarLog日志子系统的文件。
这种方法效果相当好，`aider`也支持 —— 您
可以手动指定要"添加到与GPT的聊天"中的文件。

但手动确定正确的
文件集来添加到聊天中并不理想。
而且发送整个文件是一种笨重的方式来传递代码上下文，
浪费宝贵的8k上下文窗口。
GPT不需要看到BarLog的整个实现，
它只需要足够理解它以便使用它。
如果您
仅仅为了传递上下文而发送许多文件代码，可能很快就会用完上下文窗口。

## 使用代码库地图提供上下文

最新版本的`aider`随每个变更请求向GPT发送**代码库地图**。该地图包含仓库中所有文件的列表，以及每个文件中定义的符号。可调用的函数和方法还包括它们的签名。

这里是
aider仓库地图的示例，只显示
[main.py](https://github.com/Aider-AI/aider/blob/main/aider/main.py)
和
[io.py](https://github.com/Aider-AI/aider/blob/main/aider/io.py)
的地图：

```
aider/
   ...
   main.py:
      function
         main (args=None, input=None, output=None)
      variable
         status
   ...
   io.py:
      class
         FileContentCompleter
         InputOutput
      FileContentCompleter
         member
            __init__ (self, fnames, commands)
            get_completions (self, document, complete_event)
      InputOutput
         member
            __init__ (self, pretty, yes, input_history_file=None, chat_history_file=None, input=None, output=None)
            ai_output (self, content)
            append_chat_history (self, text, linebreak=False, blockquote=False)
            confirm_ask (self, question, default="y")
            get_input (self, fnames, commands)
            prompt_ask (self, question, default=None)
            tool (self, *messages, log_only=False)
            tool_error (self, message)
   ...
```

这样映射仓库提供了一些好处：

  - GPT可以看到仓库各处的变量、类、方法和函数签名。仅这一点可能就足以解决许多任务。例如，它可能可以从地图中显示的详细信息了解如何使用模块导出的API。
  - 如果需要查看更多代码，GPT可以使用地图自行确定需要查看哪些文件。然后GPT会请求查看这些特定文件，`aider`会自动将它们添加到聊天上下文中（经用户批准）。

当然，对于大型仓库，即使只是地图也可能太大，无法适应上下文窗口。然而，这种映射方法使得与GPT-4协作处理比以前的方法更大的代码库成为可能。它还减少了手动选择要添加到聊天上下文中的文件的需要，使GPT能够自主识别与任务相关的文件。

## 使用ctags制作地图

在底层，`aider`使用
[universal ctags](https://github.com/universal-ctags/ctags)
来构建地图。Universal ctags可以扫描用多种语言编写的源代码，并提取关于每个文件中定义的所有符号的数据。

历史上，ctags由IDE或代码编辑器生成和索引，使人类更容易搜索和导航代码库、查找函数实现等。相反，我们将使用ctags帮助GPT导航和理解代码库。

以下是在源代码上运行ctags时获得的输出类型。具体来说，这是对上面映射的`main.py`文件运行`ctags --fields=+S --output-format=json`的输出：

```json
{
  "_type": "tag",
  "name": "main",
  "path": "aider/main.py",
  "pattern": "/^def main(args=None, input=None, output=None):$/",
  "kind": "function",
  "signature": "(args=None, input=None, output=None)"
}
{
  "_type": "tag",
  "name": "status",
  "path": "aider/main.py",
  "pattern": "/^    status = main()$/",
  "kind": "variable"
}
```

代码库地图是使用这种类型的`ctags`数据构建的，但格式化为前面展示的节省空间的层次树格式。这是GPT可以轻松理解的格式，并使用最少数量的token传达地图数据。

## 聊天记录示例

这个
[聊天记录](https://aider.chat/examples/add-test.html)
展示了GPT-4创建黑盒测试用例，**而没有给予它
被测试函数的源代码或仓库中任何其他
代码的访问权限。** 相反，GPT仅基于代码库地图进行操作。

仅使用地图中的元数据，GPT能够弄清楚如何调用要测试的方法，以及如何实例化准备测试所需的多个类对象。

GPT在编写测试的第一个版本时犯了一个合理的错误，但在看到`pytest`错误输出后能够快速修复问题。

## 未来工作

正如"每个请求都向GPT发送整个代码库"不是这个问题的有效解决方案，"每个请求都发送整个代码库地图"可能也不是最佳方法。发送适当的代码库地图子集将帮助`aider`更好地处理具有大型地图的更大仓库。

减少地图数据量的一些可能方法是：

  - 提炼全局地图，优先考虑重要符号并丢弃"内部"或其他不太具有全局相关性的标识符。可能利用`gpt-3.5-turbo`以灵活且与语言无关的方式执行此提炼。
  - 提供一种机制，让GPT从全局地图的提炼子集开始，并让它请求查看其认为与当前编码任务相关的子树或关键词的更多详细信息。
  - 尝试分析用户给出的自然语言编码任务并预测代码库地图的哪个子集相关。可能通过分析特定仓库内的先前编码聊天。在某些文件或功能类型上的工作可能需要来自仓库其他部分的某些可预测的上下文。针对聊天历史、代码库地图或代码库的向量和关键词搜索可能有助于此处。

一个关键目标是偏好与语言无关的解决方案，或可轻松部署到大多数流行代码语言的解决方案。`ctags`解决方案具有这一好处，因为它预构建了对大多数流行语言的支持。我怀疑语言服务器协议（Language Server Protocol）可能是比`ctags`更好的工具来解决这个问题。但它部署到广泛语言数组更为繁琐。用户需要为其特定的感兴趣语言建立LSP服务器。

## 试一试

要使用这个实验性的代码库地图功能：

  - 安装[aider](https://aider.chat/docs/install.html)。
  - 安装ctags。
  - 在您的仓库内运行`aider`，它应该显示"Repo-map: universal-ctags using 1024 tokens"。

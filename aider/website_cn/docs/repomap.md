---
parent: 更多信息
highlight_image: /assets/robot-ast.png
nav_order: 300
description: Aider使用git仓库的简明地图来为LLM提供代码上下文。
---

# 代码库地图

![机器人流程图](/assets/robot-ast.png)

Aider会生成**整个git仓库的简明地图**，
其中包含最重要的类和函数及其类型与调用签名。
这有助于aider理解正在编辑的代码
及其与代码库其他部分的关系。
代码库地图还能帮助aider编写新代码时
合理利用代码库中现有的库、模块和抽象。

## 使用代码库地图提供上下文

Aider会在每次用户发起变更请求时，
向LLM发送**代码库地图**。
该地图包含仓库文件列表，
以及每个文件中定义的关键符号。
通过包含每个定义的关键代码行，
展示这些符号的定义方式。

以下是aider代码库地图的示例部分，
对应[base_coder.py](https://github.com/Aider-AI/aider/blob/main/aider/coders/base_coder.py)
和[commands.py](https://github.com/Aider-AI/aider/blob/main/aider/commands.py)
文件：

```
aider/coders/base_coder.py:
⋮...
│class Coder:
│    abs_fnames = None
⋮...
│    @classmethod
│    def create(
│        self,
│        main_model,
│        edit_format,
│        io,
│        skip_model_availabily_check=False,
│        **kwargs,
⋮...
│    def abs_root_path(self, path):
⋮...
│    def run(self, with_message=None):
⋮...

aider/commands.py:
⋮...
│class Commands:
│    voice = None
│
⋮...
│    def get_commands(self):
⋮...
│    def get_command_completions(self, cmd_name, partial):
⋮...
│    def run(self, inp):
⋮...
```

代码库地图带来以下关键优势：

  - LLM可以看到仓库中所有的类、方法和函数签名。仅凭这些信息就足以解决许多任务。例如，LLM通常可以根据地图中的细节推断如何使用模块导出的API
  - 当需要查看更多代码时，LLM可以通过地图确定需要查看哪些文件，并要求aider将这些文件加入聊天上下文

## 地图优化

对于大型仓库，即使只是地图本身也可能超出LLM的上下文窗口限制。
Aider通过发送**最相关**的部分地图来解决这个问题。
具体实现是通过图排序算法分析完整的代码库地图，
将每个源文件视为节点，
并通过文件依赖关系连接边。
Aider会根据活跃的token预算，
选择代码库中最重要的部分进行优化。

token预算由`--map-tokens`参数控制（默认1k token）。
Aider会根据聊天状态动态调整地图大小，通常保持在该设置值内。
但在某些情况下会显著扩展地图，
特别是当没有文件被加入聊天且aider需要尽可能理解整个仓库时。

上文示例地图并未包含文件中所有的类、方法和函数，
只保留了被代码库其他部分最常引用的关键标识符，
这些是LLM理解整体代码库最需要知道的核心上下文。

## 更多信息

请访问[aider博客上的代码库地图专题文章](https://aider.chat/2023/10/22/repomap.html)
了解代码库地图构建的更多细节。

---
parent: 更多信息
nav_order: 490
description: Aider 使用多种"编辑格式"让大语言模型编辑源代码文件。
---

# 编辑格式

Aider 使用多种"编辑格式"让大语言模型编辑源代码文件。
不同模型对不同编辑格式的适配性有所差异。
Aider 默认会为大多数主流模型选择最优格式。
您始终可以使用 `--edit-format` 参数强制指定特定的编辑格式。

## 完整文件格式（whole）

这是最简单的编辑格式。
LLM 被要求返回需要修改的源文件的完整更新副本。
虽然简单，但可能效率较低且成本较高，因为即使只修改几行代码，LLM 也必须返回整个文件内容。

格式要求文件路径直接放在代码块标记之前：

````
show_greeting.py
```
import sys

def greeting(name):
    print("Hey", name)

if __name__ == '__main__':
    greeting(sys.argv[1])
```
````

## 差异格式（diff）

该格式要求 LLM 以搜索/替换块序列的形式指定文件修改。
这是种高效格式，因为模型只需返回文件中有变化的部分。

编辑使用类似 git 合并冲突标记的语法，文件路径直接放在代码块前：

````
mathweb/flask/app.py
```
<<<<<<< SEARCH
from flask import Flask
=======
import math
from flask import Flask
>>>>>>> REPLACE
```
````

## 围栏差异格式（diff-fenced）

该格式基于差异格式，但文件路径放在代码块标记内部。
主要用于 Gemini 系列模型，这些模型常常无法严格遵守标准差异格式的围栏要求。

````
```
mathweb/flask/app.py
<<<<<<< SEARCH
from flask import Flask
=======
import math
from flask import Flask
>>>>>>> REPLACE
```
````

## 统一差异格式（udiff）

该格式基于广泛使用的统一差异格式，但[经过修改和简化](/2023/12/21/unified-diffs.html)。
这是种高效格式，因为模型只需返回文件中发生变化的部分。

该格式主要适用于 GPT-4 Turbo 系列模型，因为它能减少模型的"惰性编码"倾向。
使用其他格式时，GPT-4 Turbo 模型倾向于用"# ...原有代码..." 风格的注释来省略大段代码。

````
```diff
--- mathweb/flask/app.py
+++ mathweb/flask/app.py
@@ ... @@
-class MathWeb:
+import sympy
+
+class MathWeb:
```
````

## 编辑器差异格式（editor-diff）和编辑器完整格式（editor-whole）

这些是差异格式和完整文件格式的简化版本，当使用[架构模式](/docs/usage/modes.html)时，可通过 `--editor-edit-format` 参数启用。
实际编辑格式相同，但 Aider 会使用更简洁的提示词，专注于文件编辑本身而非解决编码任务。
架构模型负责解决编码任务并提供需要修改文件的纯文本说明，编辑器模型则根据这些说明生成语法正确的差异或完整文件修改。
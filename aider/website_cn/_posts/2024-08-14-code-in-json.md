---
title: LLM在JSON中返回代码的表现不佳
excerpt: 如果你要求LLM通过工具函数调用将代码包装在JSON中返回，它们会写出更糟糕的代码。
highlight_image: /assets/code-in-json.jpg
nav_exclude: true
---
{% if page.date %}
<p class="post-date">{{ page.date | date: "%B %d, %Y" }}</p>
{% endif %}

# LLM在JSON中返回代码的表现不佳

如果要求LLM将代码作为结构化JSON响应的一部分返回，它们会产生质量较低的代码。这似乎对许多顶级模型都适用，包括那些专门支持JSON的模型。基准测试表明，模型在编写的代码中存在与引用和转义到JSON相关的语法错误。基准测试结果还暗示，由于JSON格式化的负担，解决编码问题的能力有所下降。

{% include code-in-json-benchmark.js %}

> 图1：模型在使用普通markdown文本或JSON返回代码时的Aider编码基准测试分数。
> 通过率(%)为5次运行的平均值。
> 当模型将代码作为markdown文本返回时，比起将代码作为结构化JSON响应返回，产生的代码质量更好。


## 背景

人们经常问为什么aider使用纯文本格式让LLM指定代码编辑（如下所示），
而不依赖LLM工具和结构化JSON响应。

```python
greeting.py
<<<<<<< SEARCH
def greeting():
    print("Hello")
=======
def greeting():
    print("Goodbye")
>>>>>>> REPLACE
```

人们期望使用工具调用会更容易和更可靠，这将涉及一个更像这样的结构化JSON响应：

```json
{
    "filename": "greeting.py",
    "search": "def greeting():\n    print(\"Hello\")\n"
    "replace": "def greeting():\n    print(\"Goodbye\")\n"
}
```

随着LLM提供商不断改进可靠生成JSON的工具，这个问题变得越来越相关。例如，[OpenAI最近宣布](https://openai.com/index/introducing-structured-outputs-in-the-api/)能够严格确保JSON响应在语法上是正确的，并符合指定的模式。

但仅仅生成有效的JSON对于AI代码生成来说是不够的 —— JSON内部的代码也很重要。它必须是高质量的代码，能够解决指定的编码任务，没有错误或bug。不幸的是，当要求LLM将代码包装在JSON中时，它们写出的代码质量会下降。

从某种意义上说，这并不令人惊讶。只需看看上面的非常简单的JSON示例，其中混入了代码的转义引号`\"`和换行符`\n`。想象一下，如果代码本身包含带有自己转义序列的引号字符串，会增加多少复杂性。

你会选择正常地输入代码，还是将其作为正确转义的JSON字符串输入，哪种方式能写出更好的代码？


## 量化纯文本的好处

之前的[aider基准测试结果](/2023/07/02/benchmarks.html)表明，相比于JSON包装的函数调用，将代码作为纯文本返回的方式更优越。这些结果是在一年多前获得的，当时的模型远不如今天可用的模型强大。OpenAI最近宣布支持"严格"JSON，这表明现代模型可能能够在结构化JSON响应中返回高质量代码。

这里呈现的结果基于[aider"代码编辑"基准测试](/2023/07/02/benchmarks.html#the-benchmark)，该测试包含来自Exercism python存储库的133个练习题。基准测试进行了一些简化，以便专注于比较纯文本和JSON响应之间的差异。特别是，模型仅限于对每个任务进行一次尝试，没有第二次尝试来修复错误。

每个模型在不同的代码返回策略下的性能进行了比较：

- **Markdown** -- 模型在标准markdown三重反引号围栏中返回整个源代码文件。
- **JSON** -- 模型使用工具函数调用在结构化JSON响应中返回整个源代码文件。
- **JSON (strict)** -- 与"JSON"策略相同，但设置`strict=True`。只有gpt-4o-2024-08-06支持此设置。

markdown策略与aider的"whole"编辑格式相同，其中LLM返回源文件的整个更新副本，如下所示：

````
Here is the program you asked for which prints "Hello":

greeting.py
```
def greeting():
    print("Hello")
```
````

两种JSON策略都要求LLM调用`write_file`函数，提供解释/计划和源文件的整个更新副本。LLM不必指定文件名，因为基准测试一次只操作一个源文件。

```json
{
    "explanation": "Here is the program you asked for which prints \"Hello\"",
    "content": "def greeting():\n    print(\"Hello\")\n"
}
```

这个实验设置旨在量化JSON包装对LLM编写代码解决任务能力的影响。

## 结果

对四个最强大的代码编辑模型进行了基准测试，以评估JSON包装代码的影响：

- claude-3-5-sonnet-20240620
- deepseek-coder (V2 0724)
- gpt-4o-2024-05-13
- gpt-4o-2024-08-06

每种模型和代码包装策略的组合在所有133个问题上进行了5次基准测试。

### 整体编码技能

如图1所示，当要求在结构化JSON响应中返回代码时，所有模型在基准测试中的表现都更差。大多数表现明显更差，远低于使用markdown策略的结果。

一些值得注意的观察：

- OpenAI的gpt-4o-2024-05-13是唯一一个markdown和JSON结果接近的模型。使用JSON只使得分数下降了0.4个百分点，这个差异在5次试验的误差范围内。
- 使用OpenAI的新严格模式与非严格JSON相比没有提供改进。两种JSON结果都远低于markdown结果。
- Sonnet和DeepSeek Coder的结果受到JSON包装的损害最严重。

### 语法错误

当要求将代码包装在JSON中时，模型在编写的代码中倾向于出现更多语法错误。模型可以可靠地生成有效的JSON，但内部的代码更容易出现语法错误。

图2显示了每个模型和代码包装策略产生的代码中发现的语法错误数量。它汇总了所有5次运行中的`SyntaxError`和`IndentationError`错误，针对每种模型和策略组合。

以下是由gpt-4o-2024-05-13使用JSON代码包装策略创建的`SyntaxError`示例。看起来模型在尝试格式化JSON响应时对转义和引用产生混淆。

```python
Traceback (most recent call last):
  ...   
  File "bottle-song/bottle_song.py", line 9
    lyrics.append(f'There'll be {i - 1} green bottles hanging on the wall.')
                                                                          ^
SyntaxError: unterminated string literal (detected at line 9)
```

有问题的代码行包含一个单引号字符串，其中也包含一个单引号字符。它应该被输出为以下JSON块，在`There\\'ll`中有一个双斜杠。这是需要对`\`进行JSON转义，以便在JSON解码后生存，并在结果代码中产生`There\'ll`。这将正确地转义单引号字符串内的单引号。

```
...lyrics.append(f'There\\'ll be {i - 1} green bottles hanging on the wall.')\n...
```



{% include code-in-json-syntax.js %}

> 图2：在模型生成的代码中发现的`SyntaxError`和`IndentationError`错误数量，从5次运行中合计。
> 当要求将代码包装在JSON中时，模型倾向于出现更多语法和格式错误。

### 超越语法错误

Sonnet的结果似乎表明，JSON包装的负面影响超出了仅仅语法困难。无论使用什么代码包装策略，Sonnet都避免了语法错误，但在图1中其使用JSON的基准测试分数仍然较低。这意味着JSON包装可能会分散或挑战模型的注意力，降低它们推理解决编码问题的能力。



## 结论

虽然具体结果与类似的[2023年7月实验](/2023/07/02/benchmarks.html)不同，但结论保持不变：LLM在结构化JSON响应中返回代码的表现不佳。

OpenAI似乎在允许LLM返回JSON包装的代码而不损害代码质量方面取得了进展。但此时考虑从纯文本切换到JSON包装的代码似乎为时过早。

---------

#### 关于aider排行榜的注释

*这里呈现的结果与[aider LLM排行榜](https://aider.chat/docs/leaderboards/)中的主要结果不能直接比较。为了专注于比较纯文本和JSON包装的代码，对基准测试进行了一些设置更改。*

---
parent: 屏幕录制
nav_order: 0
layout: minimal
highlight_image: /assets/recordings.jpg
description: 观看aider如何通过集成tree-sitter-language-pack添加对大量新编程语言的支持。演示了如何使用aider编写脚本下载文件集合，以及使用临时bash脚本让aider修改一系列文件。
---

# 通过tree-sitter-language-pack添加语言支持

<script>
const recording_id = "tree-sitter-language-pack";
const recording_url = "https://gist.githubusercontent.com/paul-gauthier/a990333449b09e2793088a45eb1587f4/raw/364124781cca282907ccdc7567cdfc588a9b438b/tmp.redacted.cast";
</script>

{% include recording.md %}


## 解说

- 0:01 我们将通过tree-sitter-language-pack为aider添加大量新语言。
- 0:10 首先，让我们尝试找出它支持哪些语言。
- 1:00 好的，有一个语言定义的json文件。
- 1:10 它是否包含每种语言的github仓库？
- 1:29 好的，这就是我们需要的。
- 1:45 我们需要从每个仓库获取所有的tags文件，用于aider的repo-map。让我们让aider编写一个脚本来获取它们。
- 2:05 我们将向aider展示语言定义json文件。
- 3:37 看起来它找不到大多数tags.scm文件。
- 4:19 也许我们应该让它尝试master分支以外的其他分支？
- 5:02 好的，它现在似乎正在下载它们。
- 5:55 让我们设置成可以重新运行脚本，只下载我们尚未获取的文件。
- 6:12 我看到很多tags文件，所以它正在工作。
- 6:30 好的，重新启动以运行最新代码。这将需要一段时间来获取所有文件。
- 9:02 Grep-AST模块需要了解所有新语言。
- 9:45 让我们让aider添加所有这些语言，并使用它们常用的文件扩展名注册每种语言。
- 10:15 一些语言需要通过它们的基本名称而不是扩展名来识别。
- 11:15 让我们检查一下Grep-AST是否可以处理PowerShell，这是一种新语言。
- 12:00 看起来它解析PowerShell正常。
- 13:00 好的，让我们将所有tags文件下载到aider仓库中的正确位置。
- 14:00 这将需要一分钟...
- 16:07 删除一些无操作或空的tags文件。
- 16:16 让我们提交所有未修改的tags文件。
- 16:33 我们需要更新每个tag文件，这样aider就可以识别所有这些语言中的函数、类等名称。
- 17:01 让我们使用bash循环来编写脚本，让aider修改每个tags文件。
- 17:12 我给aider提供了一个已修改的tags文件的只读示例，作为参考。
- 19:04 看起来它正确更新了前几个tags文件。
- 19:28 让我们使用grep来观察aider处理文件列表的进度。
- 20:20 它现在正在处理Dart语言...
- 20:50 下一个是E-lisp...
- 21:30 这将需要一点时间...
- 24:39 让我们添加一个README文件，标明这些tags文件的归属。
- 26:55 好的，所有文件都已更新，包含了命名代码对象的定义和引用标签。
- 27:10 让我们添加测试覆盖，确保这些语言与repo-map一起工作。
- 27:19 每种语言在测试期间都需要一个"fixture"，其中包含一些要解析的示例代码。让我们向aider展示fixtures目录的布局。
- 27:50 我们可以使用bash循环来请求aider为每个新的tags文件添加测试覆盖。
- 28:12 我们将向aider传递fixtures目录列表。
- 28:52 只需要修复bash以正确迭代tags文件列表。
- 29:27 我忘了请aider为每种语言生成示例代码fixture。
- 30:25 让我们运行repo-map测试，看看第一个新测试是否有效。
- 30:37 Arduino语言的测试失败了，repo-map为空？这不太好。
- 31:52 aider能找出问题所在吗？
- 32:27 好吧，aider通过基本上跳过Arduino让测试通过了。
- 32:36 让我看看是否可以在新的Arduino fixture代码上使用Grep-AST。
- 32:42 哦！我没有使用了解所有新语言的更新版Grep-AST。
- 32:54 好的，现在我们正确解析Arduino代码。撤销aider的错误测试修复。
- 33:05 好的，arduino现在通过了，但似乎tsx存在回归问题？
- 33:20 aider能找出原因吗？
- 34:10 让我们检查解析器映射。
- 35:00 好了，这次录制就到此为止。tsx问题是由于aider早些时候生成的映射中从".tsx"到"typescript"的不良映射造成的。












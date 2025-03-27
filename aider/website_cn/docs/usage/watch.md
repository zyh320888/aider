---
title: 在IDE中使用Aider
#highlight_image: /assets/browser.jpg
parent: 使用指南
nav_order: 750
description: Aider可以监控您的文件并响应您在喜欢的IDE或文本编辑器中添加的AI注释。
---

# 在IDE中使用Aider

<div class="video-container">
  <video controls loop poster="/assets/watch.jpg">
    <source src="/assets/watch.mp4" type="video/mp4">
    <a href="/assets/watch.mp4">Aider浏览器UI演示视频</a>
  </video>
</div>

<style>
.video-container {
  position: relative;
  padding-bottom: 102.7%; /1.027 */
  height: 0;
  overflow: hidden;
}

.video-container video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>

## AI注释

如果您使用`--watch-files`参数运行aider，它将监控您代码库中的所有文件，并查找您通过喜欢的IDE或文本编辑器添加的任何AI编码指令。

具体来说，aider会查找以`AI`、`AI!`或`AI?`开头或结尾的单行注释（# ... 或 // ...），如下所示：

```python
# Make a snake game. AI!
# What is the purpose of this method AI?
```

或者在使用`//`注释的语言中...

```js
// Write a protein folding prediction engine. AI!
```

Aider会记录所有以`AI`开头或结尾的注释。
包含带感叹号的`AI!`或带问号的`AI?`的注释是特殊的。
它们会触发aider采取行动，收集*所有*AI注释并将它们用作您的指令。

- `AI!`触发aider对您的代码进行更改。
- `AI?`触发aider回答您的问题。

观看上方的演示视频，展示了aider在VSCode中处理AI注释的方式。


## 示例

例如，如果您在代码中包含这样的AI注释：

```js
function factorial(n) // Implement this. AI!
```

那么aider会更新文件并实现该函数：

```js
function factorial(n) {
  if (n === 0 || n === 1) {
    return 1;
  } else {
    return n * factorial(n - 1);
  }
}
```

## 注释样式

Aider只监控这些类型的**单行**注释：

```
# Python和bash风格
// Javascript风格
-- SQL风格
```

Aider会在所有文件中查找这些注释类型。
您可以在编辑的任何代码文件中使用它们，即使它们不是该语言正确的注释语法。

## 多种用途

这一功能非常灵活和强大，可以以多种方式使用。

### 上下文指令

您可以在想要更改的函数中添加AI注释，在您希望进行更改的地方直接在上下文中解释更改请求。

```javascript
app.get('/sqrt/:n', (req, res) => {
    const n = parseFloat(req.params.n);

    // Add error handling for NaN and less than zero. AI!

    const result = math.sqrt(n);
    res.json({ result: result });
});
```

### 多条注释

您可以添加多条不带`!`的`AI`注释，最后用一个`AI!`触发aider。
同时请记住，如果您想协调多处的更改，可以在多个文件中分散AI注释。
只需在最后使用`AI!`来触发aider。

```python
@app.route('/factorial/<int:n>')
def factorial(n):
    if n < 0:
        return jsonify(error="Factorial is not defined for negative numbers"), 400

    # AI: Refactor this code...

    result = 1
    for i in range(1, n + 1):
        result *= i

    # ... into to a compute_factorial() function. AI!

    return jsonify(result=result)
```

### 长格式指令

您可以添加一块注释，包含更长的指令。
只需确保其中一行以`AI`或`AI!`开头或结尾，以引起aider的注意。

```python
# Make these changes: AI!
# - Add a proper main() function
# - Use Click to process cmd line args
# - Accept --host and --port args
# - Print a welcome message that includes the listening url

if __name__ == "__main__":
    app.run(debug=True)
```

### 将文件添加到aider聊天

您不必在aider聊天中使用`/add`来添加文件，只需在文件中放置一个`#AI`注释并保存文件即可。
如果您愿意，可以立即撤销/删除该注释，文件仍将添加到aider聊天中。

## 同时使用终端中的aider聊天

使用AI注释开始更改非常有帮助。
但有时您希望在此基础上构建或完善这些更改。
您当然可以继续使用AI注释来完成这些工作，
但有时切换到aider终端聊天可能更有效。
聊天中包含您刚刚做出的AI注释的历史，
所以您可以自然地从那里继续。

您还可以在终端中使用常规的aider聊天来使用
aider的许多高级功能：

- 使用`/undo`撤销您不喜欢的更改。不过您也可能能够使用IDE的撤销功能来回退文件历史。
- 使用[聊天模式](https://aider.chat/docs/usage/modes.html)提问或获取帮助。
- 使用`/tokens`、`/clear`、`/drop`、`/reset`管理聊天上下文。
添加AI注释将把文件添加到聊天中。
定期地，您可能需要移除不再需要的额外上下文。
- [修复代码检查和测试错误](https://aider.chat/docs/usage/lint-test.html)。
- 运行shell命令。
- 等等。


## 可以偷懒

上面的例子都展示了完整句子、适当大写、标点符号等的AI注释。
这样做是为了帮助解释AI注释如何工作，但在实践中并不需要。

大多数LLM完全能够处理模糊性并推断隐含的意图。
这通常允许您在AI注释中相当偷懒。
特别是，您可以使用小写的`ai`和`ai!`开始和结束注释，
而且您也可以使请求本身更加简洁。
以下是上面给出的一些例子的简化版本。

当上下文明确暗示所需操作时，`ai!`可能是您
唯一需要的。例如，要在充满其他数学函数的程序中实现阶乘函数，
以下任一方法可能都有效：

```js
function factorial(n) // ai!
```

或者...

```js
// add factorial() ai!
```

与其使用"Add error handling for NaN and less than zero"这样长而明确的注释，
您可以让aider推断出更多关于请求的信息。
这个简单的注释可能已经足够了：

```javascript
app.get('/sqrt/:n', (req, res) => {
    const n = parseFloat(req.params.n);

    // add error handling ai!

    const result = math.sqrt(n);
    res.json({ result: result });
});
```

类似地，这个重构可能可以用更少的词来请求，比如这样：

```python
@app.route('/factorial/<int:n>')
def factorial(n):
    if n < 0:
        return jsonify(error="Factorial is not defined for negative numbers"), 400

    # ai refactor...

    result = 1
    for i in range(1, n + 1):
        result *= i

    # ... to compute_factorial() ai!

    return jsonify(result=result)
```

随着您使用您选择的LLM与aider合作，您可以发展出一种感觉，了解需要多明确地表达您的AI注释。

## 幕后

Aider将您的AI注释发送给LLM，使用
[repo map](https://aider.chat/docs/repomap.html)
和所有其他代码上下文添加到聊天中。

它还提取并突出显示AI注释，显示LLM
确切如何将它们融入代码库。

```
The "AI" comments below marked with █ can be found in the code files I've shared with you.
They contain your instructions.
Make the requested changes.
Be sure to remove all these "AI" comments from the code!

todo_app.py:
⋮...
│class TodoList:
⋮...
│    def __init__(self):
│        """Initialize an empty todo list"""
⋮...
│
│    def list_tasks(self):
│        """Display all tasks"""
█        # Implement this. AI!
│
│def main():
│    todo = TodoList()
│
⋮...
```

--------

#### 致谢

*这个功能的灵感来源于
[Override](https://github.com/oi-overide)监视文件变化
以查找嵌入在`//> 特定分隔符集 <//`中的提示的方式。*

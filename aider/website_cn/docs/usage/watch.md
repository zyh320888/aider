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

It can be really helpful to get a change started with AI comments.
But sometimes you want to build on or refine those changes.
You can of course continue to do that with AI comments,
but it can sometimes be effective to switch over to the aider terminal chat.
The chat has the history of the AI comments you just made,
so you can continue on naturally from there.

You can also use the normal aider chat in your terminal to work with
many of aider's more advanced features:

- Use `/undo` to revert changes you don't like. Although you may also be able to use your IDE's undo function to step back in the file history.
- Use [chat modes](https://aider.chat/docs/usage/modes.html) to ask questions or get help.
- Manage the chat context with `/tokens`, `/clear`, `/drop`, `/reset`.
Adding an AI comment will add the file to the chat.
Periodically, you may want remove extra context that is no longer needed.
- [Fix lint and test errors](https://aider.chat/docs/usage/lint-test.html).
- Run shell commands.
- Etc.


## You can be lazy

The examples above all show AI
comments with full sentences, proper capitalization, punctuation, etc.
This was done to help explain how AI comments work, but is not needed in practice.

Most LLMs are perfectly capable of dealing with ambiguity and
inferring implied intent.
This often allows you to be quite lazy with your AI comments.
In particular, you can start and end comments with lowercase `ai` and `ai!`,
but you can also be much more terse with the request itself.
Below are simpler versions of some of the examples given above.

When the context clearly implies the needed action, `ai!` might be all you
need. For example, to implement a factorial function
in a program full of other math functions either of these
approaches would probably work:

```js
function factorial(n) // ai!
```

Or...

```js
// add factorial() ai!
```

Rather than a long, explicit comment like "Add error handling for NaN and less than zero,"
you can let aider infer more about the request.
This simpler comment may be sufficient:

```javascript
app.get('/sqrt/:n', (req, res) => {
    const n = parseFloat(req.params.n);

    // add error handling ai!

    const result = math.sqrt(n);
    res.json({ result: result });
});
```

Similarly, this refactor probably could have been requested with fewer words, like this:

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

As you use aider with your chosen LLM, you can develop a sense for how
explicit you need to make your AI comments.

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

#### Credits

*This feature was inspired by
the way [Override](https://github.com/oi-overide) watches for file changes
to find prompts embedded within `//> a specific set of delimiters <//`.*

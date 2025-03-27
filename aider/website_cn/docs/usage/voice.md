---
parent: 使用指南
nav_order: 100
description: 使用语音与aider交流代码！
---

# 用aider进行语音转代码

使用语音与aider交流您的代码！通过语音请求新功能、测试用例或错误修复，让aider完成在本地git仓库中编辑文件的工作。与aider的所有功能一样，您可以在现有仓库中使用语音转代码功能，也可以用它来启动新项目。

语音支持自然地融入了aider的AI结对编程
聊天界面。现在，当您要求aider编辑代码时，
您可以流畅地在语音和文本聊天之间切换。

## 如何使用语音转代码

使用聊天中的`/voice`命令开始录音，
并在说完后按`ENTER`键。
您的语音编码指令将被转录，
就像您在aider聊天会话中
输入它们一样。

查看[安装说明](https://aider.chat/docs/install/optional.html#enable-voice-coding)获取
有关如何启用`/voice`命令的信息。

<br/>
<div class="chat-transcript" markdown="1">

> Aider v0.11.2-dev  
> 已将app.py添加到聊天中。  

#### /voice

<blockquote>
<div class="recording-line">
    <p style="display: inline;">录音中，完成后按ENTER键... <span id="timer">3.5</span>秒</p>
    <div id="progress-bar">
        <div id="progress"></div>
    </div>
</div>
</blockquote>

<style>
    .recording-line > * {
        display: inline-block;
        vertical-align: middle;
    }
    #progress-bar {
        width: 100px;
        height: 20px;
        background-color: #333;
        margin-left: 10px;
    }
    #progress {
        height: 100%;
        background-color: #f0f0f0;
        animation: progress 3s infinite;
    }
    @keyframes progress {
        0% { width: 10%; }
        20% { width: 90%; }
        50% { width: 30%; }
        60% { width: 90%; }
        80% { width: 20%; }
        100% { width: 10%; }

    }
</style>

<script>
window.onload = function() {
    var counter = 0;
    var timer = document.getElementById('timer');
    setInterval(function() {
        counter = (counter + 0.1) % 9;
        timer.textContent = counter.toFixed(1);
    }, 100);
}
</script>

<div style="display: inline-block; position: relative; width: 200px; background-color: #f0f0f0; border-radius: 10px; padding: 10px; color: #333; font-family: 'Comic Sans MS', 'Comic Sans', 'Marker Felt', sans-serif;">
<span style="position: absolute; top: 0; left: 50%; transform: translate(-50%, -100%); width: 0; height: 0; border-left: 10px solid transparent; border-right: 10px solid transparent; border-bottom: 10px solid #f0f0f0;"></span>
"&nbsp;添加一个使用math factorial的阶乘端点&nbsp;"
</div>

#### 添加一个使用math.factorial的阶乘端点。

要向Flask应用程序添加阶乘端点，我们需要修改`app.py`文件。

以下是步骤：

1. 向Flask应用程序添加一个新路由`/fact/<int:x>`。
2. 在此路由的函数中，调用`math.factorial(x)`并将结果作为字符串返回。

以下是这些更改的*编辑块*：

```python
app.py
<<<<<<< HEAD
if __name__ == '__main__':
    print("Starting...")
    app.run()
=======
@app.route('/fact/<int:x>')
def factorial(x):
    result = math.factorial(x)
    return str(result)

if __name__ == '__main__':
    print("Starting...")
    app.run()
>>>>>>> updated
```

> 已应用对app.py的编辑  
> 提交ef9e3e7 aider: 添加一个使用math.factorial的阶乘端点。  

</div>
<br/>
<br/>
<br/>

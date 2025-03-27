---
parent: 安装
nav_order: 20
---

# 可选步骤
{: .no_toc }

以下步骤完全是可选的。

- TOC
{:toc}

## 安装git

如果你安装了git，Aider的效果会更好。
这里有
[在各种环境中安装git的说明](https://github.com/git-guides/install-git)。

## 设置API密钥

你需要从API提供商那里获取密钥才能使用大多数模型：

- [OpenAI](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key) 提供o1、o3-mini、gpt-4o和其他模型。注意，支付API密钥的费用与成为"ChatGPT"订阅用户是不同的。
- [Anthropic](https://docs.anthropic.com/claude/reference/getting-started-with-the-api) 提供Claude 3.7 Sonnet和Haiku。
- [DeepSeek](https://platform.deepseek.com/api_keys) 提供DeepSeek R1和DeepSeek Chat V3。
- [OpenRouter](https://openrouter.ai/keys) 允许你使用单个密钥访问来自多个提供商的模型。

你可以[在配置或环境文件中存储你的API密钥](/docs/config/api-keys.html)，
这样每次运行aider时都会自动加载它们。

## 启用Playwright

Aider支持使用`/web <url>`命令将网页添加到聊天中。
当你添加URL到聊天中时，aider会获取页面并抓取其内容。

默认情况下，aider使用`httpx`库来抓取网页，但这只适用于部分网页。
有些网站明确阻止了来自httpx等工具的请求。
其他网站则严重依赖JavaScript来渲染页面内容，
仅使用httpx是无法实现的。

如果你安装了Playwright的chromium浏览器及其依赖项，
aider可以更好地处理所有网页：

```
playwright install --with-deps chromium
```

有关其他信息，请参阅
[Playwright for Python文档](https://playwright.dev/python/docs/browsers#install-system-dependencies)。


## 启用语音编码

Aider支持
使用聊天内的`/voice`命令
[用语音进行编码](https://aider.chat/docs/usage/voice.html)。
Aider使用[PortAudio](http://www.portaudio.com)库来
捕获音频。
安装PortAudio完全是可选的，但通常可以这样完成：

- 对于Windows，无需安装PortAudio。
- 对于Mac，执行`brew install portaudio`
- 对于Linux，执行`sudo apt-get install libportaudio2`
  - 某些Linux环境可能还需要`sudo apt install libasound2-plugins`

## 将aider添加到你的IDE/编辑器

你可以使用
[aider的`--watch-files`模式](https://aider.chat/docs/usage/watch.html)
与任何IDE或编辑器集成。

有许多第三方aider插件适用于各种IDE/编辑器。
目前不清楚它们与aider最新版本的兼容程度如何，
所以最好的方法可能是在编辑器旁边的终端中运行最新的
aider，并使用`--watch-files`。

### NeoVim

[joshuavial](https://github.com/joshuavial)提供了一个适用于aider的NeoVim插件：

[https://github.com/joshuavial/aider.nvim](https://github.com/joshuavial/aider.nvim)

### VS Code

你可以在VS Code终端窗口内运行aider。
有许多第三方
[VSCode的aider插件](https://marketplace.visualstudio.com/search?term=aider%20-kodu&target=VSCode&category=All%20categories&sortBy=Relevance)。

### 其他编辑器

如果你有兴趣为你喜欢的编辑器创建aider插件，
请通过开启
[GitHub issue](https://github.com/Aider-AI/aider/issues)
告诉我们。



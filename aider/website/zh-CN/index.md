---
title: 首页
nav_order: 1
lang: zh-CN
---

# Aider：在终端中进行 AI 结对编程

Aider 让您可以与 LLM（大语言模型）进行结对编程，
编辑本地 git 仓库中的代码。
您可以开始一个新项目或处理现有的代码库。
Aider 与 Claude 3.5 Sonnet、DeepSeek R1 & Chat V3、OpenAI o1、o3-mini 和 GPT-4o 配合使用效果最佳。Aider 可以[连接几乎所有的 LLM，包括本地模型](https://aider.chat/zh-CN/docs/llms.html)。

<p align="center">
  <video style="max-width: 100%; height: auto;" autoplay loop muted playsinline>
    <source src="/assets/shell-cmds-small.mp4" type="video/mp4">
    您的浏览器不支持视频标签。
  </video>
</p>

<p align="center">
  <a href="https://discord.gg/Tv2uQnR88V">
    <img src="https://img.shields.io/badge/加入-Discord-blue.svg"/>
  </a>
  <a href="https://aider.chat/zh-CN/docs/install.html">
    <img src="https://img.shields.io/badge/阅读-文档-green.svg"/>
  </a>
</p>

## 快速开始

如果您已经安装了 Python 3.8-3.13，可以按照以下步骤快速开始：

```bash
python -m pip install aider-install
aider-install

# 切换到您的代码库目录
cd /to/your/project

# 通过 DeepSeek 的 API 使用 DeepSeek
aider --model deepseek --api-key deepseek=your-key-goes-here

# 通过 Anthropic 的 API 使用 Claude 3.5 Sonnet
aider --model sonnet --api-key anthropic=your-key-goes-here

# 通过 OpenAI 的 API 使用 GPT-4o
aider --model gpt-4o --api-key openai=your-key-goes-here

# 通过 OpenRouter 的 API 使用 Sonnet
aider --model openrouter/anthropic/claude-3.5-sonnet --api-key openrouter=your-key-goes-here

# 通过 OpenRouter 的 API 使用 DeepSeek
aider --model openrouter/deepseek/deepseek-chat --api-key openrouter=your-key-goes-here
```

查看[安装说明](https://aider.chat/zh-CN/docs/install.html)和[使用文档](https://aider.chat/zh-CN/docs/usage.html)了解更多详情。

## 特性

- 运行 aider 时指定要编辑的文件：`aider <file1> <file2> ...`
- 请求更改：
  - 添加新功能或测试用例
  - 描述一个 bug
  - 粘贴错误信息或 GitHub issue URL
  - 重构代码
  - 更新文档
- Aider 将编辑您的文件以完成您的请求
- Aider [自动创建 git 提交](https://aider.chat/zh-CN/docs/git.html)，并生成合理的提交信息
- [在您喜欢的编辑器或 IDE 中使用 aider](https://aider.chat/zh-CN/docs/usage/watch.html)
- Aider 支持[大多数流行的编程语言](https://aider.chat/zh-CN/docs/languages.html)：Python、JavaScript、TypeScript、PHP、HTML、CSS 等
- Aider 可以同时编辑多个文件以处理复杂的请求
- Aider 使用[整个 git 仓库的地图](https://aider.chat/zh-CN/docs/repomap.html)，这有助于它在较大的代码库中更好地工作
- 在与 aider 聊天时可以在编辑器或 IDE 中编辑文件，它总是会使用最新版本。与 AI 结对编程
- [在聊天中添加图片](https://aider.chat/zh-CN/docs/usage/images-urls.html)（支持 GPT-4o、Claude 3.5 Sonnet 等）
- [在聊天中添加 URL](https://aider.chat/zh-CN/docs/usage/images-urls.html)，aider 将读取其内容
- [使用语音编码](https://aider.chat/zh-CN/docs/usage/voice.html)
- Aider 与 Claude 3.5 Sonnet、DeepSeek V3、o1 和 GPT-4o 配合使用效果最佳，并且可以[连接几乎所有的 LLM](https://aider.chat/zh-CN/docs/llms.html)

## 顶级性能

[Aider 在 SWE Bench 上获得了最高分之一](https://aider.chat/2024/06/02/main-swe-bench.html)。
SWE Bench 是一个具有挑战性的软件工程基准测试，aider 在其中解决了来自流行开源项目（如 Django、scikit-learn、matplotlib 等）的*真实* GitHub 问题。

## 更多信息

- [文档](https://aider.chat/zh-CN/)
- [安装](https://aider.chat/zh-CN/docs/install.html)
- [使用说明](https://aider.chat/zh-CN/docs/usage.html)
- [教程视频](https://aider.chat/zh-CN/docs/usage/tutorials.html)
- [连接到 LLM](https://aider.chat/zh-CN/docs/llms.html)
- [配置](https://aider.chat/zh-CN/docs/config.html)
- [故障排除](https://aider.chat/zh-CN/docs/troubleshooting.html)
- [LLM 排行榜](https://aider.chat/zh-CN/docs/leaderboards/)
- [GitHub](https://github.com/Aider-AI/aider)
- [Discord](https://discord.gg/Tv2uQnR88V)
- [博客](https://aider.chat/zh-CN/blog/)

## 用户好评

- *最好的免费开源 AI 编程助手。* -- [IndyDevDan](https://youtu.be/YALpX8oOn78)
- *目前最好的 AI 编程助手。* -- [Matthew Berman](https://www.youtube.com/watch?v=df8afeb1FY8)
- *Aider ... 轻松让我的编码效率提高了四倍。* -- [SOLAR_FIELDS](https://news.ycombinator.com/item?id=36212100)
- *这是一个很酷的工作流程... Aider 的人体工程学对我来说是完美的。* -- [qup](https://news.ycombinator.com/item?id=38185326)
- *就像在你的 Git 仓库中有一个高级开发者 - 真的很神奇！* -- [rappster](https://github.com/Aider-AI/aider/issues/124)
- *多么神奇的工具。简直难以置信。* -- [valyagolev](https://github.com/Aider-AI/aider/issues/6#issue-1722897858)
- *Aider 真是太惊人了！* -- [cgrothaus](https://github.com/Aider-AI/aider/issues/82#issuecomment-1631876700)
- *它在起步和制作前几个工作版本时的速度远超我的预期。* -- [Daniel Feldman](https://twitter.com/d_feldman/status/1662295077387923456)
- *感谢 Aider！它真的让我看到了编码的未来。* -- [derwiki](https://news.ycombinator.com/item?id=38205643)
- *简直太神奇了。它让我能够做以前觉得超出舒适区的事情。* -- [Dougie](https://discord.com/channels/1131200896827654144/1174002618058678323/1174084556257775656)
- *这个项目太棒了。* -- [funkytaco](https://github.com/Aider-AI/aider/issues/112#issuecomment-1637429008)
- *令人惊叹的项目，绝对是我用过的最好的 AI 编程助手。* -- [joshuavial](https://github.com/Aider-AI/aider/issues/84)
- *我非常喜欢使用 Aider ... 它让软件开发的体验变得轻松许多。* -- [principalideal0](https://discord.com/channels/1131200896827654144/1133421607499595858/1229689636012691468)
- *我一直在从多次肩部手术中恢复 ... 并广泛使用 aider。它让我能够继续保持生产力。* -- [codeninja](https://www.reddit.com/r/OpenAI/s/nmNwkHy1zG)
- *我是 aider 的忠实用户。我完成了更多的工作，但用的时间更少。* -- [dandandan](https://discord.com/channels/1131200896827654144/1131200896827654149/1135913253483069470)
- *在花费了 100 美元的代币尝试寻找更好的工具后，我又回到了 Aider。它完全超越了其他所有工具，根本没有竞争。* -- [SystemSculpt](https://discord.com/channels/1131200896827654144/1131200896827654149/1178736602797846548)
- *Aider 太棒了，与 Sonnet 3.5 结合使用简直令人震惊。* -- [Josh Dingus](https://discord.com/channels/1131200896827654144/1133060684540813372/1262374225298198548)
- *毫无疑问，这是迄今为止最好的 AI 编程助手工具。* -- [IndyDevDan](https://www.youtube.com/watch?v=MPYFPvxfGZs)
- *[Aider] 改变了我的日常编码工作流程。令人惊讶的是一个 Python 应用程序如何能改变你的生活。* -- [maledorak](https://discord.com/channels/1131200896827654144/1131200896827654149/1258453375620747264)
- *最适合在现有代码库中进行实际开发工作的代理。* -- [Nick Dobos](https://twitter.com/NickADobos/status/1690408967963652097?s=20)
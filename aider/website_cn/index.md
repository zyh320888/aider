---
title: Home
nav_order: 1
---

<!--[[[cog
# This page is a copy of README.md, adding the front matter above.
# Remove any cog markup before inserting the README text.
text = open("README.md").read()
text = text.replace('['*3 + 'cog', ' NOOP ')
text = text.replace('['*3 + 'end', ' NOOP ')
text = text.replace(']'*3, '')

# embedding these confuses the syntax highlighter while editing index.md
com_open = '<!' + '--'
com_close = '--' + '>'

# comment out the screencast
text = text.replace('SCREENCAST START ' + com_close, '')
text = text.replace(com_open + ' SCREENCAST END', '')

# uncomment the video
text = text.replace('VIDEO START', com_close)
text = text.replace('VIDEO END', com_open)

cog.out(text)
]]]-->

<!-- Edit README.md, not index.md -->

# Aider 是终端里的 AI 结对编程工具

Aider 让你能与大语言模型结对编程，共同编辑本地 git 仓库中的代码。无论是新项目还是已有代码库都能完美兼容。Aider 在 Claude 3.5 Sonnet、DeepSeek R1 & Chat V3、OpenAI o1、o3-mini 和 GPT-4o 上表现最佳，并支持[连接几乎所有大模型（包括本地模型）](https://aider.chat/docs/llms.html)。

<!-- 
<p align="center">
  <img
    src="https://aider.chat/assets/screencast.svg"
    alt="aider screencast"
  >
</p>
 -->

<!-- -->
<p align="center">
  <video style="max-width: 100%; height: auto;" autoplay loop muted playsinline>
    <source src="/assets/shell-cmds-small.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
</p>
<!-- -->

<p align="center">
  <a href="https://discord.gg/Tv2uQnR88V">
    <img src="https://img.shields.io/badge/Join-Discord-blue.svg"/>
  </a>
  <a href="https://aider.chat/docs/install.html">
    <img src="https://img.shields.io/badge/Read-Docs-green.svg"/>
  </a>
</p>

## 快速开始

如果已安装 Python 3.8-3.13，可通过以下命令快速上手：

```bash
python -m pip install aider-install
aider-install

# 进入你的代码目录
cd /to/your/project

# 通过 DeepSeek API 使用
aider --model deepseek --api-key deepseek=你的API密钥

# 通过 Anthropic API 使用 Claude 3.5 Sonnet
aider --model sonnet --api-key anthropic=你的API密钥

# 通过 OpenAI API 使用 GPT-4o 
aider --model gpt-4o --api-key openai=你的API密钥

# 通过 OpenRouter 使用 Sonnet
aider --model openrouter/anthropic/claude-3.5-sonnet --api-key openrouter=你的API密钥

# 通过 OpenRouter 使用 DeepSeek
aider --model openrouter/deepseek/deepseek-chat --api-key openrouter=你的API密钥
```

详细请参考[安装指南](https://aider.chat/docs/install.html)和[使用文档](https://aider.chat/docs/usage.html)。

## 核心功能

- 指定要编辑的文件：`aider <文件1> <文件2> ...`
- 支持多种修改请求：
  - 添加新功能或测试用例
  - 描述程序缺陷
  - 粘贴错误信息或 GitHub issue 链接
  - 代码重构
  - 文档更新
- 自动进行[git commit](https://aider.chat/docs/git.html)并生成清晰的提交信息
- [在常用编辑器/IDE 中使用](https://aider.chat/docs/usage/watch.html)
- 支持[主流编程语言](https://aider.chat/docs/languages.html)：Python、JavaScript、TypeScript、PHP、HTML、CSS 等
- 支持多文件协同修改完成复杂需求
- 通过[全仓库代码地图](https://aider.chat/docs/repomap.html)提升大代码库工作效率
- 支持边编辑边聊天，实时同步最新改动
- [支持图片输入](https://aider.chat/docs/usage/images-urls.html)（GPT-4o、Claude 3.5 Sonnet 等）
- [支持URL内容读取](https://aider.chat/docs/usage/images-urls.html)
- [语音编程支持](https://aider.chat/docs/usage/voice.html)


## 顶尖性能表现

[Aider 在 SWE Bench 基准测试中名列前茅](https://aider.chat/2024/06/02/main-swe-bench.html)。该基准收录了 django、scikitlearn、matplotlib 等知名开源项目的真实 GitHub issue，测试难度极高。

## 更多信息

- [完整文档](https://aider.chat/)
- [安装指南](https://aider.chat/docs/install.html)
- [使用教程](https://aider.chat/docs/usage.html)
- [视频教程](https://aider.chat/docs/usage/tutorials.html)
- [大模型接入指南](https://aider.chat/docs/llms.html)
- [配置说明](https://aider.chat/docs/config.html)
- [问题排查](https://aider.chat/docs/troubleshooting.html)
- [模型性能榜](https://aider.chat/docs/leaderboards/)
- [GitHub 仓库](https://github.com/Aider-AI/aider)
- [Discord 社区](https://discord.gg/Tv2uQnR88V)
- [技术博客](https://aider.chat/blog/)


## 用户评价

- *最佳免费开源AI编程助手* —— [IndyDevDan](https://youtu.be/YALpX8oOn78)
- *迄今最强的AI编程助手* —— [Matthew Berman](https://www.youtube.com/watch?v=df8afeb1FY8)
- *Aider 使我的编码效率至少提升四倍* —— [SOLAR_FIELDS](https://news.ycombinator.com/item?id=36212100)
- *工作流设计精妙... 人机交互体验完美* —— [qup](https://news.ycombinator.com/item?id=38185326)
- *就像资深开发者驻守在你的仓库——不可思议！* —— [rappster](https://github.com/Aider-AI/aider/issues/124)
- *肩膀手术康复期间，Aider 帮助我保持了开发效率* —— [codeninja](https://www.reddit.com/r/OpenAI/s/nmNwkHy1zG)
- *Aider 已成工作必备，效率倍增但耗时更少* —— [dandandan](https://discord.com/channels/1131200896827654144/1131200896827654149/1135913253483069470)
- *最佳实际开发辅助工具，现有代码库工作毫无压力* —— [Nick Dobos](https://twitter.com/NickADobos/status/1690408967963652097?s=20)
<!--[[[end]]]-->

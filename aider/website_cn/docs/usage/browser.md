---
title: 在浏览器中使用Aider
highlight_image: /assets/browser.jpg
parent: 使用指南
nav_order: 800
description: Aider不仅可以在命令行中运行，还可以在浏览器中运行。
---
{% if page.date %}
<p class="post-date">{{ page.date | date: "%B %d, %Y" }}</p>
{% endif %}

# 在浏览器中使用Aider

<div class="video-container">
  <video controls loop poster="/assets/browser.jpg">
    <source src="/assets/aider-browser-social.mp4" type="video/mp4">
    <a href="/assets/aider-browser-social.mp4">Aider浏览器界面演示视频</a>
  </video>
</div>

<style>
.video-container {
  position: relative;
  padding-bottom: 101.89%; /* 1080 / 1060 = 1.0189 */
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

使用aider的新实验性浏览器界面与LLM合作
编辑本地git仓库中的代码。
Aider将直接编辑您本地源文件中的代码，
并以合理的提交消息[git提交更改](https://aider.chat/docs/git.html)。
您可以开始一个新项目或使用现有的git仓库。
Aider与GPT-4o、Sonnet 3.7和DeepSeek Chat V3 & R1等模型
配合良好。
它还支持[连接到几乎任何LLM](https://aider.chat/docs/llms.html)。

使用`--browser`开关启动浏览器版本的aider：

```
python -m pip install -U aider-chat

export OPENAI_API_KEY=<key> # Mac/Linux
setx   OPENAI_API_KEY <key> # Windows, restart shell after setx

aider --browser
```

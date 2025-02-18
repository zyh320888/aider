---
title: 与网页聊天界面进行复制粘贴
#highlight_image: /assets/browser.jpg
parent: 使用指南
nav_order: 850
description: Aider可与LLM网页聊天界面协同工作
---

# 与网页聊天界面进行复制粘贴

<div class="video-container">
  <video controls loop poster="/assets/copypaste.jpg">
    <source src="/assets/copypaste.mp4" type="video/mp4">
    <a href="/assets/copypaste.mp4">Aider浏览器界面演示视频</a>
  </video>
</div>

<style>
.video-container {
  position: relative;
  padding-bottom: 66.34%; /* 2160 / 3256 = 0.6634 */
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

## 与LLM网页聊天界面协同工作

[Aider可以通过API连接大多数LLM](https://aider.chat/docs/llms.html)，这是最佳使用方式。但在某些情况下，您可能需要通过网页聊天界面与LLM协作：

- 公司政策可能限制您只能使用专有的网页聊天系统
- 网页版LLM可能具有独特的上下文访问权限或针对您的任务进行过专门微调
- 某些模型的API使用成本过高
- 可能没有可用的API

Aider提供了与网页版LLM协同工作的功能，使您可以将网页版LLM作为"核心代码架构师"，同时使用更小、更经济的LLM来实际修改本地文件。

在这个"文件编辑器"环节，您可以使用许多开源、免费或成本极低的LLM来运行aider。例如上方的演示视频展示了aider使用DeepSeek来实施o1-preview在网页聊天中建议的修改。

### 复制aider的代码上下文到剪贴板并粘贴至网页界面

使用`/copy-context <instructions>`命令可以将aider的代码上下文复制到剪贴板，内容包括：

- 通过`/add`添加到聊天中的所有文件
- 通过`/read`添加的只读文件
- Aider的[仓库地图](https://aider.chat/docs/repomap.html)，从git仓库其他位置引入相关代码上下文
- 要求LLM简明输出修改指令的提示语
- 如果包含`<instructions>`参数，指令也会被复制

您可以将上下文粘贴到浏览器中，开始与网页版LLM交互并请求代码修改。

### 将LLM的回复粘贴回aider以编辑文件

当LLM生成回复后，您可以使用网页界面中的"复制回复"按钮复制LLM的响应。回到aider中，运行`/paste`命令，aider将根据LLM的建议修改您的文件。

您可以使用经济高效的模型（如GPT-4o Mini、DeepSeek或Qwen）来执行这些编辑。建议使用`--edit-format editor-diff`或`--edit-format editor-whole`参数运行aider以获得最佳效果。

### 复制粘贴模式

Aider提供`--copy-paste`模式来简化整个流程：

- 当使用`/add`或`/read`添加文件时，aider会自动将更新后的完整代码上下文复制到剪贴板
  操作成功后您会看到"已复制代码上下文到剪贴板"的提示
- 当您在aider外部复制LLM的回复到剪贴板时，aider会自动检测并加载到聊天界面
  只需按下ENTER发送消息，aider就会将LLM的修改应用到本地文件
- Aider会自动选择最适合复制粘贴功能的编辑格式
  根据您使用的LLM不同，会自动选择`editor-whole`或`editor-diff`格式

## 服务条款

请务必查阅您使用的任何LLM网络聊天服务的服务条款。这些功能不得用于违反任何服务的条款（TOS）。

Aider的网页聊天功能设计时已考虑符合大多数LLM网页聊天服务的条款要求。

使用LLM网页聊天进行编程时涉及4个复制粘贴步骤：

1. 从aider复制代码和上下文
2. 将代码和上下文粘贴到LLM网页聊天
3. 从LLM网页聊天复制回复
4. 将LLM回复粘贴回aider

大多数LLM网页聊天服务条款禁止自动化步骤(2)和(3)（即代码的复制和粘贴）。Aider的`--copy-paste`模式将这些步骤保留为100%手动操作，仅优化与aider交互的步骤(1)和(4)，这些操作不应属于LLM网页聊天服务条款的管辖范围。

如果您担心步骤(1)和(4)中与aider的自动交互可能违反您LLM服务提供商的条款，可以不使用`--copy-paste`模式，改为手动使用`/copy-context`和`/paste`命令来保持合规。

再次强调，请勿违反任何服务的条款使用这些功能。

---
title: Sonnet绝非懒惰
excerpt: Claude 3.5 Sonnet能轻松编写超出单个4k令牌API响应限制的优质代码。
highlight_image: /assets/sonnet-not-lazy.jpg
nav_exclude: true
---

[![sonnet绝非懒惰](/assets/sonnet-not-lazy.jpg)](https://aider.chat/assets/sonnet-not-lazy.jpg)

{% if page.date %}
<p class="post-date">{{ page.date | date: "%B %d, %Y" }}</p>
{% endif %}

# Sonnet绝非懒惰

Claude 3.5 Sonnet代表了AI编码的一次重大飞跃。
它极其勤奋、认真且努力工作。
出乎意料的是，
这带来了一个挑战：
Sonnet
经常编写如此多的代码，
以至于它会达到4k输出令牌限制，
在中途截断其编码。

Aider现在能够
绕过这个4k限制，允许Sonnet
生成任意数量的代码。
结果令人惊讶地强大。
Sonnet在
[aider的重构基准测试](https://aider.chat/docs/leaderboards/#code-refactoring-leaderboard)
上的得分从55.1%跃升至64.0%。
这使Sonnet跃居第二位，超过了GPT-4o，
仅次于Opus。

使用[aider最新版本](https://aider.chat/HISTORY.html#aider-v0410)
预览版的用户感到非常兴奋：

- *效果非常好。它是个怪物。它可以毫不费力地重构任何大小的文件。Sonnet的继续技巧真是圣杯。Aider完全击败了[其他工具]。我要取消两个订阅。* -- [Emasoft](https://github.com/Aider-AI/aider/issues/705#issuecomment-2200338971)
- *非常感谢这个功能 - 它真的是个改变游戏规则的功能。我可以在要求Claude开发更大的功能时更有野心。* -- [cngarrison](https://github.com/Aider-AI/aider/issues/705#issuecomment-2196026656)
- *太棒了...！不受输出令牌长度问题的限制真是一个巨大的改进。[我将]单个JavaScript文件重构成七个较小的文件，只使用了一个Aider请求。* -- [John Galt](https://discord.com/channels/1131200896827654144/1253492379336441907/1256250487934554143)

## 达到4k令牌输出限制

所有LLM都有各种令牌限制，最为人熟知的是它们的
上下文窗口大小。
但它们也限制了对单个请求的响应中可以输出
多少令牌。
Sonnet和大多数其他
模型都限制返回4k令牌。

Sonnet惊人的工作道德使其
经常达到这个4k输出令牌
限制，原因有几个：

1. Sonnet能够在一个响应中输出非常大量的正确、
完整的新代码。
2. 类似地，Sonnet可以一次性指定长序列的编辑，
比如在重构大型文件时更改大部分行。
3. Sonnet在执行SEARCH & REPLACE编辑时倾向于引用
文件的大块内容。
除了令牌限制外，这也非常浪费。

## 好问题

问题(1)和(2)是"好问题"，
因为Sonnet能够
编写比任何其他模型更多的高质量代码！
我们只是不希望它因为4k输出限制
而过早中断。

Aider现在允许Sonnet以多个4k令牌
响应返回代码。
Aider无缝地将它们组合在一起，使Sonnet可以返回任意
长的响应。
这获得了Sonnet多产编码技能的所有优点，
而不受4k输出令牌限制的约束。

## 浪费令牌

问题(3)更为复杂，因为Sonnet不仅仅是
被提前停止——它实际上浪费了大量
令牌、时间和金钱。

面对源文件中相距较远的几个小变更，
Sonnet常常倾向于对几乎整个文件执行一个巨大的SEARCH/REPLACE
操作。
进行几次精确的编辑会快得多，也便宜得多。

Aider现在会提示Sonnet，劝阻这些冗长的
SEARCH/REPLACE操作，
并促进更简洁的编辑。

## Aider与Sonnet

[aider的最新版本](https://aider.chat/HISTORY.html#aider-v0410)
对Claude 3.5 Sonnet提供了专门支持：

- Aider允许Sonnet生成任意数量的代码，
通过自动无缝地将响应
分散在一系列4k令牌API响应中。
- Aider仔细地提示Sonnet在提出
代码编辑时要简洁。
这减少了Sonnet浪费时间、令牌和金钱返回
大块不变代码的倾向。
- 如果环境中设置了`ANTHROPIC_API_KEY`，Aider现在默认使用Claude 3.5 Sonnet。

查看
[aider的安装说明](https://aider.chat/docs/install.html)
了解更多详情，但
您可以像这样快速开始使用aider和Sonnet：

```
$ python -m pip install -U aider-chat

$ export ANTHROPIC_API_KEY=<key> # Mac/Linux
$ setx   ANTHROPIC_API_KEY <key> # Windows, restart shell after setx

$ aider
```


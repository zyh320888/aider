---
title: 使用Llama 3.1、新版DeepSeek Coder和Mistral Large进行编码
excerpt: 新模型的代码编辑能力总结，以Sonnet和GPT-3.5为参考基准。
highlight_image: /assets/2024-07-new-models.jpg
nav_exclude: true
---
{% if page.date %}
<p class="post-date">{{ page.date | date: "%B %d, %Y" }}</p>
{% endif %}

# 使用Llama 3.1、新版DeepSeek Coder和Mistral Large进行编码

![新模型的代码编辑能力总结，以Sonnet和GPT-3.5为参考基准。](/assets/2024-07-new-models.jpg)

在过去几天中发布了五个值得关注的模型，它们具有各种不同的代码编辑能力。
以下是它们在[aider的代码编辑排行榜](https://aider.chat/docs/leaderboards/)上的结果，
同时包括Claude 3.5 Sonnet和最佳GPT-3.5模型作为参考基准。

- **77% claude-3.5-sonnet**
- 73% DeepSeek Coder V2 0724
- 66% llama-3.1-405b-instruct
- 60% Mistral Large 2 (2407)
- 59% llama-3.1-70b-instruct
- **58% gpt-3.5-turbo-0301**
- 38% llama-3.1-8b-instruct

你可以使用aider与所有这些模型进行编码，如下所示：

```
$ python -m pip install -U aider-chat

# 切换到要处理的git仓库目录
$ cd /to/your/git/repo

$ export DEEPSEEK_API_KEY=your-key-goes-here
$ aider --model deepseek/deepseek-coder

$ export MISTRAL_API_KEY=your-key-goes-here
$ aider --model mistral/mistral-large-2407

$ export OPENROUTER_API_KEY=your-key-goes-here
$ aider --model openrouter/meta-llama/llama-3.1-405b-instruct
$ aider --model openrouter/meta-llama/llama-3.1-70b-instruct
$ aider --model openrouter/meta-llama/llama-3.1-8b-instruct
```

查看[安装说明](https://aider.chat/docs/install.html)和其他[文档](https://aider.chat/docs/usage.html)了解更多详情。

## DeepSeek Coder V2 0724

DeepSeek Coder V2 0724是最大的惊喜，也是最强的代码编辑模型，在排行榜上排名第二。
与之前的DeepSeek Coder版本不同，它可以使用SEARCH/REPLACE高效地编辑代码。
这解锁了编辑大型文件的能力。

这个新的Coder版本在基准测试中获得了73%的分数，
非常接近Sonnet的77%，但成本低20-50倍！

## LLama 3.1

Meta发布了Llama 3.1系列模型，它们在许多评估中表现良好。

旗舰型号Llama 3.1 405B instruct在aider的排行榜上仅位居第7位，
远远落后于Claude 3.5 Sonnet和GPT-4o等前沿模型。

405B模型可以使用SEARCH/REPLACE高效地编辑代码，但基准测试分数有所下降。
使用这种"diff"编辑格式时，其分数从66%下降到64%。

较小的70B模型与GPT-3.5相当，而8B模型则远远落后。
两者似乎都不能可靠地使用SEARCH/REPLACE编辑文件。
这限制了它们只能编辑能够适应其输出令牌限制的较小文件。

## Mistral Large 2 (2407)

Mistral Large 2 (2407)在aider的代码编辑基准测试中仅得到60%的分数。
这使其仅略高于最佳GPT-3.5模型。
它似乎无法可靠地使用SEARCH/REPLACE高效地编辑代码，
这限制了它只能用于小型源文件。





---
title: 开源模型的细节很重要
excerpt: 开源LLM变得越来越强大，但请注意您（或您的提供商）如何提供模型服务。这可能会影响代码编辑技能。
highlight_image: /assets/quantization.jpg
draft: false
nav_exclude: true
---
{% if page.date %}
<p class="post-date">{{ page.date | date: "%B %d, %Y" }}</p>
{% endif %}

# 开源模型的细节很重要
{: .no_toc }

<canvas id="quantChart" width="800" height="600" style="margin: 20px 0"></canvas>

像Qwen 2.5 32B Instruct这样的开源模型在aider的代码编辑基准测试中表现非常好，媲美闭源前沿模型。

但请注意您的模型如何被服务和量化，因为这可能会影响代码编辑技能。
开源模型通常以各种量化版本提供，
并且可以以不同的令牌限制提供服务。
这些细节在处理代码时很重要。

上图和下表比较了Qwen 2.5 Coder 32B Instruct模型的不同版本，
它们既在本地提供服务，也从各种云提供商提供服务。

- 通过[glhf.chat](https://glhf.chat)提供服务的[HuggingFace BF16权重](https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct)。
- [针对mlx的4位和8位量化](https://t.co/cwX3DYX35D)。
- 来自[OpenRouter提供商混合](https://openrouter.ai/qwen/qwen-2.5-coder-32b-instruct/providers)的结果，这些提供商以不同级别的量化提供模型服务。
- 来自OpenRouter提供商的结果，既通过OpenRouter提供，也直接通过它们自己的API提供。
- Ollama从[Ollama模型库](https://ollama.com/library/qwen2.5-coder:32b-instruct-q4_K_M)本地提供不同量化的服务，具有8k+上下文窗口。
- 使用Ollama默认2k上下文窗口提供服务的Ollama fp16量化。

### 陷阱和细节

这项基准测试工作突显了开源模型特有的许多陷阱和细节，
这些因素可能对它们正确编辑代码的能力产生重大影响：

- **量化** -- 开源模型通常以数十种不同的量化版本提供。
大多数似乎只是适度降低代码编辑技能，但更强的量化
确实有实际影响。
- **上下文窗口** -- 云提供商可以决定接受多大的上下文窗口，
而且它们经常做出不同的选择。Ollama的本地API服务器
默认为一个微小的2k上下文窗口，
并且会静默丢弃超出它的数据。这么小的窗口会
对性能造成灾难性影响，而不会抛出明显的硬错误。
- **输出令牌限制** -- 开源模型通常以极其
不同的输出令牌限制提供服务。这直接影响模型可以
在响应中编写或编辑多少代码。
- **有缺陷的云提供商** -- 在对Qwen 2.5 Coder 32B Instruct
和DeepSeek V2.5进行基准测试时，我发现
多个云提供商的API端点存在缺陷或bug。
它们似乎
返回的结果与基于广告的量化和上下文大小预期的不同。
对代码编辑基准测试造成的损害从严重
到灾难性不等。
一个提供商在使用DeepSeek V2.5（一个高度能干的模型）的基准测试中得分为0.5%。

闭源、专有模型通常没有这些问题。
它们由创建它们的组织拥有和运营，
并且通常以特定的、可预测的上下文窗口和输出令牌限制提供服务。
它们的量化级别通常是未知的，但对所有用户是固定和不变的。

### 结论

Qwen模型的最佳版本可与GPT-4o媲美，而性能最差的
量化版本在服务得当时更像是较旧的GPT-4 Turbo。
即使是原本优秀的fp16量化，
如果使用Ollama的默认2k上下文窗口运行，性能也会降至GPT-3.5 Turbo水平。

### 章节
{: .no_toc }

- TOC
{:toc}

## 基准测试结果

{: .note :}
这些是来自单次基准测试运行的结果，所以预期正常变异为+/- 1-2%。

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
{% include quant-chart.js %}
</script>

<input type="text" id="quantSearchInput" placeholder="搜索..." style="width: 100%; max-width: 800px; margin: 10px auto; padding: 8px; display: block; border: 1px solid #ddd; border-radius: 4px;">

<table style="width: 100%; max-width: 800px; margin: auto; border-collapse: collapse; box-shadow: 0 2px 4px rgba(0,0,0,0.1); font-size: 14px;">
  <thead style="background-color: #f2f2f2;">
    <tr>
      <th style="padding: 8px; text-align: left;">模型</th>
      <th style="padding: 8px; text-align: center;">正确完成百分比</th>
      <th style="padding: 8px; text-align: center;">使用正确编辑格式的百分比</th>
      <th style="padding: 8px; text-align: left;">命令</th>
      <th style="padding: 8px; text-align: center;">编辑格式</th>
    </tr>
  </thead>
  <tbody>
    {% assign quant_sorted = site.data.quant | sort: 'pass_rate_2' | reverse %}
    {% for row in quant_sorted %}
      <tr style="border-bottom: 1px solid #ddd;">
        <td style="padding: 8px;">{{ row.model }}</td>
        <td style="padding: 8px; text-align: center;">{{ row.pass_rate_2 }}%</td>
        <td style="padding: 8px; text-align: center;">{{ row.percent_cases_well_formed }}%</td>
        <td style="padding: 8px;"><code>{{ row.command }}</code></td>
        <td style="padding: 8px; text-align: center;">{{ row.edit_format }}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>

<style>
  tr.selected {
    color: #0056b3;
  }
  table {
    table-layout: fixed;
  }
  td, th {
    word-wrap: break-word;
    overflow-wrap: break-word;
  }
  td:nth-child(3), td:nth-child(4) {
    font-size: 12px;
  }
</style>

<script>
document.getElementById('quantSearchInput').addEventListener('keyup', function() {
    var input = this.value.toLowerCase();
    var rows = document.querySelectorAll('tbody tr');
    
    rows.forEach(function(row) {
        var text = row.textContent.toLowerCase();
        if(text.includes(input)) {
            row.style.display = '';
            row.classList.add('selected');
        } else {
            row.style.display = 'none';
            row.classList.remove('selected');
        }
    });
});
</script>

## 设置Ollama的上下文窗口大小

[Ollama默认使用2k上下文窗口](https://github.com/ollama/ollama/blob/main/docs/faq.md#how-can-i-specify-the-context-window-size)，
这对于与aider一起工作来说非常小。
与大多数其他LLM服务器不同，Ollama在您提交
超出上下文窗口的请求时不会抛出错误。
相反，它只是通过丢弃聊天中"最旧"的消息来
静默截断请求，使其适合于上下文窗口内。

除了单个2k上下文结果外，
上面所有的Ollama结果都是使用至少8k上下文窗口收集的。
8k窗口足够大，可以尝试基准测试中的所有编码问题。
从aider v0.65.0开始，Aider默认将Ollama的上下文窗口设置为8k。

您可以使用
[`.aider.model.settings.yml`文件](https://aider.chat/docs/config/adv-model-settings.html#model-settings)
更改Ollama服务器的上下文窗口，如下所示：

```
- name: ollama/qwen2.5-coder:32b-instruct-fp16
  extra_params:
    num_ctx: 8192
```

## 使用OpenRouter选择提供商

OpenRouter允许您在您的
[首选项](https://openrouter.ai/settings/preferences)中忽略特定提供商。
这可以用来限制您的OpenRouter请求
仅由您首选的提供商提供服务。

## 注意事项

这篇文章经过多次修订，因为我收到了
社区众多成员的反馈。
以下是一些值得注意的经验和变化：

- 本文的第一个版本包含了不正确的Ollama模型。
- 早期的Ollama结果使用了太小的默认2k上下文窗口，
人为地损害了基准测试结果。
- 基准测试结果似乎发现了OpenRouter
与Hyperbolic通信方式中的一个问题。
他们在11/24/24修复了这个问题，就在它被指出后不久。

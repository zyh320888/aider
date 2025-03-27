---
title: DeepSeek V3 替代提供商
excerpt: DeepSeek的API一直存在可靠性问题。这里有一些您可以使用的替代提供商。
#highlight_image: /assets/deepseek-down.jpg
draft: false
nav_exclude: true
---
{% if page.date %}
<p class="post-date">{{ page.date | date: "%B %d, %Y" }}</p>
{% endif %}

# DeepSeek V3 替代提供商
{: .no_toc }

<canvas id="editChart" width="800" height="450" style="margin-top: 20px"></canvas>

在过去的24-48+小时内，DeepSeek的API一直存在重大可靠性问题，许多用户报告了停机和过载问题。
他们的[状态页面](https://status.deepseek.com)显示存在正在进行的事件。

如果您受到这些问题的影响，有几个替代提供商提供对DeepSeek V3的访问。本文比较了它们在aider的多语言基准测试上的表现，以帮助您选择可靠的替代方案。

## 提供商
{: .no_toc }

* TOC
{:toc}

## OpenRouter

[OpenRouter提供多种DeepSeek提供商](https://openrouter.ai/deepseek/deepseek-chat/providers)
通过他们的统一API。
您可以这样使用OpenRouter和aider：

```bash
# 使用环境变量设置API密钥
export OPENROUTER_API_KEY=<your-key>
aider --model openrouter/deepseek/deepseek-chat

# 或使用--api-key命令行选项
aider --model openrouter/deepseek/deepseek-chat --api-key openrouter=<your-key>

# 或将其添加到您的主目录或项目根目录的.aider.conf.yml中：
api-key:
  - openrouter=<your-key>
```

OpenRouter自动监控其提供商，并将请求路由到稳定的API，远离那些性能不可靠的API。

但并非所有提供商都提供相同版本的开源模型，也并非所有提供商都有相同的隐私保证。
您可以通过[aider的模型设置](https://aider.chat/docs/config/adv-model-settings.html#model-settings)控制用于提供模型的OpenRouter提供商。
在您的主目录或git项目根目录中创建一个`.aider.model.settings.yml`文件，其设置如下：

```yaml
- name: openrouter/deepseek/deepseek-chat
  extra_params:
    extra_body:
      provider:
        # 仅使用这些提供商，按此顺序
        order: ["Novita"]
        # 不要回退到其他提供商
        allow_fallbacks: false
```

更多详情请参阅[OpenRouter的提供商路由文档](https://openrouter.ai/docs/provider-routing)。


## Fireworks

```bash
# 使用环境变量设置API密钥
export FIREWORKS_API_KEY=<your-key>
aider --model fireworks_ai/accounts/fireworks/models/deepseek-chat

# 或使用--api-key命令行选项
aider --model fireworks_ai/accounts/fireworks/models/deepseek-chat --api-key fireworks=<your-key>

# 或将其添加到您的主目录或项目根目录的.aider.conf.yml中：
api-key:
  - fireworks=<your-key>
```

在您的主目录或git项目根目录中创建一个`.aider.model.settings.yml`文件，其设置如下：

```yaml
- name: fireworks_ai/accounts/fireworks/models/deepseek-chat
  edit_format: diff
  weak_model_name: null
  use_repo_map: true
  send_undo_reply: false
  lazy: false
  reminder: sys
  examples_as_sys_msg: true
  extra_params:
    max_tokens: 8192
  cache_control: false
  caches_by_default: true
  use_system_prompt: true
  use_temperature: true
  streaming: true
```


## Hyperbolic

您可以使用[Hyperbolic的API](https://hyperbolic.xyz)作为OpenAI兼容的提供商：

```bash
# 使用环境变量设置API密钥
export OPENAI_API_BASE=https://api.hyperbolic.xyz/v1/
export OPENAI_API_KEY=<your-key>
aider --model openai/deepseek-ai/DeepSeek-V3

# 或使用--api-key命令行选项
aider --model openai/deepseek-ai/DeepSeek-V3 --api-key openai=<your-key>

# 或将其添加到您的主目录或项目根目录的.aider.conf.yml中：
api-key:
  - openai=<your-key>
```

在您的主目录或git项目根目录中创建一个`.aider.model.settings.yml`文件，其设置如下：

```yaml
- name: openai/deepseek-ai/DeepSeek-V3
  edit_format: diff
  weak_model_name: null
  use_repo_map: true
  send_undo_reply: false
  lazy: false
  reminder: sys
  examples_as_sys_msg: true
  cache_control: false
  caches_by_default: true
  use_system_prompt: true
  use_temperature: true
  streaming: true
  editor_model_name: null
  editor_edit_format: null
  extra_params:
    max_tokens: 65536
```

## Ollama

您可以通过[Ollama运行DeepSeek V3](https://ollama.com/library/deepseek-v3)。

```bash
# 拉取模型
ollama pull deepseek-v3

# 启动ollama服务器
ollama serve

# 在另一个终端窗口...
export OLLAMA_API_BASE=http://127.0.0.1:11434 # Mac/Linux
setx   OLLAMA_API_BASE http://127.0.0.1:11434 # Windows，setx后重启shell

aider --model ollama/deepseek-v3
```

提供模型设置很重要，特别是`num_ctx`参数来设置上下文窗口。
Ollama默认使用2k上下文窗口，这对于与aider一起工作来说非常小。
更大的上下文窗口将允许您处理更多的代码，
但会使用更多内存并增加延迟。

与大多数其他LLM服务器不同，如果您提交的请求超过上下文窗口，Ollama不会抛出错误。相反，它只是通过丢弃聊天中"最旧"的消息来静默截断请求，使其适合上下文窗口内。

所以如果您的上下文窗口太小，您不会收到明确的错误。最大的症状将是aider表示它看不到您添加到聊天中的（部分）文件。这是因为ollama正在静默丢弃它们，因为它们超出了上下文窗口。

在您的主目录或git项目根目录中创建一个`.aider.model.settings.yml`文件，其设置如下：

```yaml
- name: ollama/deepseek-v3
  edit_format: diff
  weak_model_name: null
  use_repo_map: true
  send_undo_reply: false
  lazy: false
  reminder: sys
  examples_as_sys_msg: true
  cache_control: false
  caches_by_default: true
  use_system_prompt: true
  use_temperature: true
  streaming: true
  extra_params:
    num_ctx: 8192 # 上下文窗口有多大？
```

## 其他提供商

当通过其他提供商提供DeepSeek V3时，您需要正确配置aider：

- 确定要使用的`--model`名称。
- 向aider提供您的API密钥。
- 将模型设置添加到`.aider.model.settings.yml`。


调整上面显示的Fireworks的`.aider.model.settings.yml`。您需要将`name`字段更改为匹配您选择的提供商的模型命名方案。

有关所有aider模型设置的详细信息，请参阅[高级模型设置](https://aider.chat/docs/config/adv-model-settings.html#model-settings)

## 结果


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
    {% assign edit_sorted = site.data.deepseek-down | sort: 'pass_rate_2' | reverse %}
    {% for row in edit_sorted %}
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

<script src="https://unpkg.com/patternomaly/dist/patternomaly.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
{% assign data_source = edit_sorted %}
{% assign pass_rate_field = "pass_rate_2" %}
{% assign highlight_model = "DeepSeek" %}
{% include leaderboard.js %}
</script>
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

---
parent: 配置
nav_order: 5
description: 为API提供商设置API密钥。
---

# API密钥

Aider允许您通过几种方式指定API密钥：

- 在命令行中
- 作为环境变量
- 在`.env`文件中
- 在您的`.aider.conf.yml`配置文件中

---

## OpenAI和Anthropic

Aider对通过专用开关和配置选项提供
OpenAI和Anthropic API密钥有特殊支持。
其他提供商的设置密钥工作方式略有不同，请参见下文。

#### 命令行

您可以通过[命令行开关](/docs/config/options.html#api-keys-and-settings)
`--openai-api-key`和`--anthropic-api-key`设置OpenAI和Anthropic API密钥。


#### 环境变量或.env文件

您也可以将它们存储在环境变量或[.env文件](/docs/config/dotenv.html)中，
这对每个API提供商都有效：

```
OPENAI_API_KEY=<密钥>
ANTHROPIC_API_KEY=<密钥>
```

#### Yaml配置文件
您还可以通过[yaml配置文件](/docs/config/aider_conf.html)中的特殊条目设置这些API密钥，如下所示：

```yaml
openai-api-key: <密钥>
anthropic-api-key: <密钥>
```


---

## 其他API提供商

所有其他LLM提供商可以使用以下方法之一设置他们的API密钥。

#### 命令行
{: .no_toc }

使用`--api-key provider=<密钥>`，这将设置环境变量`PROVIDER_API_KEY=<密钥>`。因此，`--api-key gemini=xxx`将设置`GEMINI_API_KEY=xxx`。

#### 环境变量或.env文件
{: .no_toc }

您可以在环境变量中设置API密钥。
[.env文件](/docs/config/dotenv.html)
是存储API密钥和其他提供商API环境变量的好地方：

```bash
GEMINI_API_KEY=foo
OPENROUTER_API_KEY=bar
DEEPSEEK_API_KEY=baz
```

#### Yaml配置文件


您还可以通过[`.aider.conf.yml`文件](/docs/config/aider_conf.html)
中的`api-key`条目设置API密钥：

```
api-key:
- gemini=foo      # 设置环境变量 GEMINI_API_KEY=foo
- openrouter=bar  # 设置环境变量 OPENROUTER_API_KEY=bar
- deepseek=baz    # 设置环境变量 DEEPSEEK_API_KEY=baz
```


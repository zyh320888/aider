---
parent: 连接到LLMs
nav_order: 500
---

# Ollama

Aider可以连接到本地Ollama模型。

```
# 拉取模型
ollama pull <model>

# 启动您的ollama服务器，将上下文窗口增加到8k tokens
OLLAMA_CONTEXT_LENGTH=8192 ollama serve

# 在另一个终端窗口...
python -m pip install -U aider-chat

export OLLAMA_API_BASE=http://127.0.0.1:11434 # Mac/Linux
setx   OLLAMA_API_BASE http://127.0.0.1:11434 # Windows, 使用setx后需重启shell

aider --model ollama_chat/<model>
```

{: .note }
推荐使用`ollama_chat/`而不是`ollama/`。


有关使用aider不熟悉的模型时出现警告的信息，
请参阅[模型警告](warnings.html)部分。

## API密钥

如果您使用的ollama需要API密钥，可以设置`OLLAMA_API_KEY`：

```
export OLLAMA_API_KEY=<api-key> # Mac/Linux
setx   OLLAMA_API_KEY <api-key> # Windows, 使用setx后需重启shell
```

## 设置上下文窗口大小

[Ollama默认使用2k上下文窗口](https://github.com/ollama/ollama/blob/main/docs/faq.md#how-can-i-specify-the-context-window-size)，
这对于与aider一起工作来说非常小。
它还会**静默地**丢弃超出窗口的上下文。
这特别危险，因为许多用户甚至没有意识到他们的大部分数据
正被Ollama丢弃。
 
默认情况下，aider将Ollama的上下文窗口
设置为足够大，以容纳您发送的每个请求加上8k tokens用于回复。
这确保数据不会被Ollama静默丢弃。

如果您想要配置固定大小的上下文窗口，
可以使用
[`.aider.model.settings.yml`文件](https://aider.chat/docs/config/adv-model-settings.html#model-settings)
像这样：

```
- name: ollama/qwen2.5-coder:32b-instruct-fp16
  extra_params:
    num_ctx: 65536
```


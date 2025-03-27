---
parent: 连接到LLMs
nav_order: 300
---

# Gemini

您需要一个 [Gemini API密钥](https://aistudio.google.com/app/u/2/apikey)。

```
python -m pip install -U aider-chat

# 您可能需要安装google-generativeai
pip install -U google-generativeai

# 或使用pipx...
pipx inject aider-chat google-generativeai

export GEMINI_API_KEY=<key> # Mac/Linux
setx   GEMINI_API_KEY <key> # Windows, 使用setx后需重启shell

# 您可以使用Gemini 2.5 Pro模型：
aider --model gemini-2.5-pro

# 列出Gemini可用的模型
aider --list-models gemini/
```


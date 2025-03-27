
如果您已经安装了 Python 3.8-3.13，可以按照以下方式快速开始：

```bash
python -m pip install aider-install
aider-install

# 切换到您的代码库目录
cd /to/your/project

# 通过 DeepSeek API 使用 DeepSeek
aider --model deepseek --api-key deepseek=your-key-goes-here

# 通过 Anthropic API 使用 Claude 3.5 Sonnet
aider --model sonnet --api-key anthropic=your-key-goes-here

# 通过 OpenAI API 使用 GPT-4o
aider --model gpt-4o --api-key openai=your-key-goes-here

# 通过 OpenRouter API 使用 Sonnet
aider --model openrouter/anthropic/claude-3.5-sonnet --api-key openrouter=your-key-goes-here

# 通过 OpenRouter API 使用 DeepSeek
aider --model openrouter/deepseek/deepseek-chat --api-key openrouter=your-key-goes-here
```

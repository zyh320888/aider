---
title: 提示缓存
highlight_image: /assets/prompt-caching.jpg
parent: 使用指南
nav_order: 750
description: Aider 支持提示缓存功能，可节省成本并加速编程流程。
---

# 提示缓存

Aider 支持提示缓存功能，可节省成本并加速编程流程。
目前 Anthropic 为 Sonnet 和 Haiku 模型提供缓存支持，
DeepSeek 则为 Chat 模型提供缓存功能。

Aider 通过组织聊天历史记录来实现缓存，包括：

- 系统提示词
- 通过 `--read` 或 `/read-only` 添加的只读文件
- 仓库地图（代码仓库结构）
- 已加入聊天会话的可编辑文件

![提示缓存](/assets/prompt-caching.jpg)

## 使用方法

运行 aider 时添加 `--cache-prompts` 参数，或将该设置加入您的
[配置文件](/docs/config.html)。

由于供应商 API 的限制，当启用流式响应时无法获取缓存统计信息和成本数据。
如需关闭流式传输，请使用 `--no-stream` 参数。

启用缓存功能后，主模型启动时会显示缓存状态提示：

```
Main model: claude-3-5-sonnet-20240620 with diff edit format, prompt cache, infinite output
```

## 防止缓存过期

Aider 可以通过定期 ping 供应商来保持提示缓存活跃，防止其过期。
默认情况下，Anthropic 的缓存保留时间为 5 分钟。
使用 `--cache-keepalive-pings N` 参数可让 aider 每 5 分钟发送一次 ping 
以维持缓存活跃状态。在您发送每条消息后，aider 将在接下来的 `N*5` 分钟内
最多发送 `N` 次 ping。


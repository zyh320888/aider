---
parent: 更多信息
nav_order: 500
description: 可选的匿名数据收集，不包含个人信息
---

# 分析数据

Aider 可以收集匿名分析数据以帮助改进其使用大语言模型、编辑代码和完成用户请求的能力。

## 可选的匿名数据，不包含个人信息

只有在您同意并选择加入时才会收集分析数据。
Aider 尊重您的隐私，从不收集您的代码、聊天信息、密钥或个人信息。

Aider 收集的信息包括：

- 使用的大语言模型及其token消耗量
- 使用的代码编辑格式
- 功能和使用命令的频率
- 异常和错误信息
- 其他相关信息

这些分析数据会关联一个匿名随机生成的UUID4用户标识符。

这些信息通过识别最常用的模型、编辑格式、功能和命令来帮助改进aider。同时也有助于发现用户遇到的错误，以便在未来的版本中修复。

## 禁用分析数据

您可以通过运行以下命令永久禁用分析数据收集：

```
aider --analytics-disable
```

## 启用分析数据

`--[no-]analytics` 开关控制当前会话是否启用分析数据：

- `--analytics` 会在当前会话启用分析数据。
如果您已使用`--analytics-disable`永久禁用，该开关将失效。
如果是首次启用，aider会确认您是否同意加入分析数据收集。
- `--no-analytics` 会在当前会话禁用分析数据。
- 默认情况下，如果您不提供`--analytics`或`--no-analytics`参数，
aider会为随机选择的用户启用分析数据。如果您已使用`--analytics-disable`永久禁用，则不会启用。
被随机选中的用户会被询问是否同意加入分析数据收集。


## 选择加入

首次启用分析数据时，需要确认同意加入：

```
aider --analytics

Aider尊重您的隐私，从不收集您的代码、提示词、聊天记录、密钥或任何个人信息。
更多信息请访问：https://aider.chat/docs/more/analytics.html
是否允许收集匿名分析数据以帮助改进aider？(Y)是/(N)否 [Yes]：
```

如果选择"否"，分析数据收集将被永久禁用。


## 数据收集详情

### 分析数据示例

要了解收集的数据类型，您可以查看
[示例分析日志](https://github.com/aider-ai/aider/blob/main/aider/website/assets/sample-analytics.jsonl)。
这些是作者个人使用aider的最后1000条分析事件，会定期更新。


### 分析代码

由于aider是开源项目，所有收集分析数据的代码都可以在源码中查看。
可以通过
[GitHub搜索](https://github.com/search?q=repo%3Aaider-ai%2Faider+%22.event%28%22&type=code)
查看相关代码。


### 记录和查看分析数据

您可以获取aider收集的所有分析数据的完整日志，以便审核或检查：

```
aider --analytics-log filename.jsonl
```

如果只想记录分析数据但不发送，可以：

```
aider --analytics-log filename.jsonl --no-analytics
```


## 问题反馈

如果您对aider收集的分析数据或我们的数据实践有任何疑问，
请通过提交
[GitHub Issue](https://github.com/aider-ai/aider/issues)
联系我们。

## 隐私政策

更多详细信息请参阅aider的
[隐私政策](/docs/legal/privacy.html)。


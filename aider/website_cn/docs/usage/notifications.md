---
title: 通知
highlight_image: /assets/notifications.jpg
parent: 使用指南
nav_order: 760
description: Aider可以在等待您输入时通知您。
---

# 通知

Aider可以在完成工作并等待您输入时通知您。
这对于长时间运行的操作或当您在多任务处理时特别有用。

## 用法

使用`--notifications`标志启用通知：

```bash
aider --notifications
```

启用后，当LLM完成响应生成并等待您的输入时，aider将通知您。

## 特定操作系统的通知

Aider会自动检测您的操作系统并使用适当的通知方法：

- **macOS**：如果可用，使用`terminal-notifier`，否则回退到AppleScript通知
- **Linux**：如果可用，使用`notify-send`或`zenity`
- **Windows**：使用PowerShell显示消息框

## 自定义通知命令

您可以使用`--notifications-command`指定自定义通知命令：

```bash
aider --notifications-command "your-custom-command"
```

例如，在macOS上您可以使用：

```bash
aider --notifications-command "say 'Aider已准备就绪'"
```

### 远程通知

对于远程通知，您可以使用[Apprise](https://github.com/caronc/apprise)，
这是一个跨平台的Python库，用于向各种服务发送通知。

我们可以使用Apprise向Slack发送通知：

```bash
aider --notifications-command "apprise -b 'Aider已准备就绪' 'slack://your-slack-webhook-token'"
```

或Discord：
```bash
aider --notifications-command "apprise -b 'Aider已准备就绪' 'discord://your-discord-webhook-token'"
```

甚至通过Pushbullet发送到您的手机：
```bash
aider --notifications-command "apprise -b 'Aider已准备就绪' 'pbul://your-pushbullet-access-token'"
```

查看Apprise的GitHub页面了解更多使用和配置方法。

## 配置

您可以将这些设置添加到配置文件中：

```yaml
# 启用通知
notifications: true

# 可选的自定义通知命令
notifications_command: "your-custom-command"
```

或在您的`.env`文件中：

```
AIDER_NOTIFICATIONS=true
AIDER_NOTIFICATIONS_COMMAND=your-custom-command
``` 
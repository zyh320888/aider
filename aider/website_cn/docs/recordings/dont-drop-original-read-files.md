---
parent: 屏幕录制
nav_order: 1
layout: minimal
highlight_image: /assets/recordings.jpg
description: 跟随演示如何修改aider以在使用/drop命令时保留启动时指定的只读文件。Aider完成了此实现并添加了测试覆盖。
---

# 启动时添加的只读文件不被/drop命令删除

<script>
const recording_id = "dont-drop-original-read-files";
const recording_url = "https://gist.githubusercontent.com/paul-gauthier/c2e7b2751925fb7bb47036cdd37ec40d/raw/08e62ab539e2b5d4b52c15c31d9a0d241377c17c/707583.cast";
</script>

{% include recording.md %}

## 解说

- 0:01 我们将更新/drop命令，以保留最初在启动时指定的任何只读文件。
- 0:10 我们添加了处理主CLI和聊天内斜杠命令（如/drop）的文件。
- 0:20 让我们向aider解释所需的更改。
- 1:20 好的，让我们查看代码。
- 1:30 我不太喜欢使用"hasattr()"，让我们寻求改进方案。
- 1:45 让我们进行一些手动测试。
- 2:10 看起来不错。让我们检查现有的测试套件，确保我们没有破坏任何功能。
- 2:19 让我们请aider为此添加测试。
- 2:50 测试看起来合理，我们完成了！








---
parent: 配置
nav_order: 100
description: 如何为aider的/editor命令配置自定义编辑器
---

# 编辑器配置

Aider允许您配置首选文本编辑器以与`/editor`命令一起使用。编辑器必须能够在"阻塞模式"下运行，这意味着命令行将等待直到您关闭编辑器后才继续。

## 使用`--editor`

您可以使用`--editor`开关或在aider的[yaml配置文件](https://aider.chat/docs/config/aider_conf.html)中使用`editor:`来指定文本编辑器。

## 环境变量

Aider按以下顺序检查环境变量以确定使用哪个编辑器：

1. `AIDER_EDITOR`
2. `VISUAL`
3. `EDITOR`

## 默认行为

如果未配置编辑器，aider将使用这些特定平台的默认值：

- Windows: `notepad`
- macOS: `vim`
- Linux/Unix: `vi`

## 使用自定义编辑器

您可以在shell的配置文件中设置您首选的编辑器（例如，`.bashrc`，`.zshrc`）：

```bash
export AIDER_EDITOR=vim
```

## 按平台划分的流行编辑器

### macOS

1. **vim**
   ```bash
   export AIDER_EDITOR=vim
   ```

2. **Emacs**
   ```bash
   export AIDER_EDITOR=emacs
   ```

3. **VSCode**
   ```bash
   export AIDER_EDITOR="code --wait"
   ```

4. **Sublime Text**
   ```bash
   export AIDER_EDITOR="subl --wait"
   ```

5. **BBEdit**
   ```bash
   export AIDER_EDITOR="bbedit --wait"
   ```

### Linux

1. **vim**
   ```bash
   export AIDER_EDITOR=vim
   ```

2. **Emacs**
   ```bash
   export AIDER_EDITOR=emacs
   ```

3. **nano**
   ```bash
   export AIDER_EDITOR=nano
   ```

4. **VSCode**
   ```bash
   export AIDER_EDITOR="code --wait"
   ```

5. **Sublime Text**
   ```bash
   export AIDER_EDITOR="subl --wait"
   ```

### Windows

1. **Notepad**
   ```bat
   set AIDER_EDITOR=notepad
   ```

2. **VSCode**
   ```bat
   set AIDER_EDITOR="code --wait"
   ```

3. **Notepad++**
   ```bat
   set AIDER_EDITOR="notepad++ -multiInst -notabbar -nosession -noPlugin -waitForClose"
   ```

## 编辑器命令参数

某些编辑器需要特定的命令行参数才能在阻塞模式下运行。`--wait`标志（或等效标志）通常用于使编辑器阻塞直到文件关闭。

## 故障排除

如果您遇到编辑器不阻塞（立即返回提示符）的问题，请验证：

1. 您的编辑器支持阻塞模式
2. 您已包含阻塞模式所需的命令行参数
3. 如果编辑器命令包含空格或特殊字符，则编辑器命令已正确引用，例如：
   ```bash
   export AIDER_EDITOR="code --wait"
   ```

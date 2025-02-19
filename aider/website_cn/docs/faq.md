---
nav_order: 90
description: 关于aider的常见问题解答。
---

# FAQ
{: .no_toc }

- 目录
{:toc}

{% include help-tip.md %}

## 如何将所有文件添加到聊天？

用户经常询问如何将代码库中的**大量或全部文件**添加到聊天中。这通常不是一个好主意，可能会带来更多问题而非帮助。

最佳做法是考虑完成当前任务需要修改哪些文件，只添加这些文件到聊天中。

当人们想要添加"所有文件"时，通常认为这能为大语言模型提供代码库的整体上下文。Aider会自动通过分析整个代码库来构建紧凑的[仓库地图](https://aider.chat/2023/10/22/repomap.html)。

添加大量与当前任务无关的文件会分散大语言模型的注意力，导致代码生成质量下降甚至文件编辑错误。同时也会增加token消耗成本。

如果仍希望添加多个文件，可以：
- 启动时使用通配符：`aider src/*.py`
- 在聊天中使用带通配符的`/add`命令：`/add src/*.py`
- 为`/add`命令指定目录名递归添加：`/add src`

## 能否在大型（单体）代码库中使用aider？

Aider可在任何规模的代码库中使用，但对超大型代码库的响应速度未做专门优化。以下建议可改善性能：

请先查看[通用使用技巧](/docs/usage/tips.html)，再考虑以下大型代码库专用建议：

- 使用`--subtree-only`参数，限制aider只处理当前子目录
- 创建`.aiderignore`文件（遵循`.gitignore`语法）忽略无关部分。例如：

```
# 忽略所有
/*

# 允许特定目录
!foo/
!bar/
!baz/

# 允许这些目录下的嵌套文件
!foo/**
!bar/**
!baz/**
```

- 使用`--aiderignore <filename>`指定不同的忽略规则文件

## 能否同时使用多个git代码库？

当前aider只能处理单个代码库。如需跨代码库协作，可以尝试：

1. 在代码库A中使用`/read`命令添加代码库B的关键文件（只读）
2. 在各代码库中运行`aider --show-repo-map > map.md`生成代码库地图
3. 在代码库A中`/read`代码库B的地图文件
4. 使用aider编写跨代码库文档，在需要时`/read`相关文档

## 如何启用代码库地图？

根据使用的LLM，aider可能默认禁用代码库地图：
```
Repo-map: disabled
```
这是因为较弱模型容易被代码库地图内容干扰。如需强制启用，可运行`aider --map-tokens 1024`。

## 如何在上下文中包含git历史？

在新会话中包含近期git历史：
1. 使用`/run git diff`命令查看差异：
   ``` 
   /run git diff HEAD~1
   ```
2. 查看多个提交：
   ``` 
   /run git diff HEAD~3
   ```

查看PR分支差异：
``` 
/run git diff one-branch..another-branch

...
添加6.9k tokens的命令输出到聊天？(Y)es/(N)o [Yes]: Yes

/ask 这个修改与FooBar类的协作是否存在问题？
```

{: .tip }
`/git`命令的输出不会包含在聊天上下文中

## 如何从源码本地运行aider？

本地运行步骤：
```
# 克隆代码库
git clone git@github.com:Aider-AI/aider.git

# 进入项目目录
cd aider

# 建议创建虚拟环境

# 以可编辑模式安装
python -m pip install -e .

# 运行本地版本
python -m aider
```


## 能否修改aider使用的系统提示？

最便捷的方式是使用[约定文件](https://aider.chat/docs/usage/conventions.html)添加自定义指令。

aider采用模块化设计支持不同的系统提示和编辑格式。查看`aider/coders`子目录可以看到基础提示和多种具体实现。如果想实验系统提示，可以参考[代码编辑基准测试文档](https://aider.chat/docs/benchmarks.html)。

当前支持的编辑器格式：
- wholefile格式（GPT-3.5默认）：`--edit-format whole`
- editblock格式（GPT-4o默认）：`--edit-format diff` 
- universal diff格式（GPT-4 Turbo默认）：`--edit-format udiff`

实验时可使用`--verbose --no-pretty`参数查看原始通信数据。

## 开发aider时使用哪些LLM？

aider自身约70%的新代码由LLM编写。以下是从[公开日志](https://github.com/aider-ai/aider/blob/main/aider/website/assets/sample-analytics.jsonl)提取的近期使用模型统计：

<!--[[[cog
import sys
sys.path.append(".")
import scripts.my_models as my_models
stats = my_models.collect_model_stats()
html = my_models.format_html_table(stats)
cog.out(html)
]]]-->
<style>
table { border-collapse: collapse; width: 100%; }
th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
th { background-color: #f2f2f2; }
tr:hover { background-color: #f5f5f5; }
.right { text-align: right; }
</style>
<table>
<tr><th>Model Name</th><th class='right'>Total Tokens</th><th class='right'>Percent</th></tr>
<tr><td>claude-3-5-sonnet-20241022</td><td class='right'>905,105</td><td class='right'>63.8%</td></tr>
<tr><td>fireworks_ai/accounts/fireworks/models/deepseek-v3</td><td class='right'>277,726</td><td class='right'>19.6%</td></tr>
<tr><td>deepseek/deepseek-chat</td><td class='right'>97,745</td><td class='right'>6.9%</td></tr>
<tr><td>claude-3-5-haiku-20241022</td><td class='right'>69,203</td><td class='right'>4.9%</td></tr>
<tr><td>o3-mini</td><td class='right'>46,467</td><td class='right'>3.3%</td></tr>
<tr><td>fireworks_ai/accounts/fireworks/models/deepseek-r1</td><td class='right'>21,182</td><td class='right'>1.5%</td></tr>
<tr><td>ollama_chat/REDACTED</td><td class='right'>309</td><td class='right'>0.0%</td></tr>
</table>

{: .note :}
部分模型显示为REDACTED，因它们是新模型或非主流模型。
Aider的统计仅记录"知名"LLM的名称。
<!--[[[end]]]-->

## 如何统计"aider编写xx%代码"？

通过[git blame统计脚本](https://github.com/Aider-AI/aider/blob/main/scripts/blame.py)分析仓库历史，计算每个版本中新增的源代码行数（仅统计源代码文件，不含文档和提示文件）。

## 为什么有时代码高亮失效？

当添加的文件包含三重反引号时，aider会改用`<source>`标签包裹代码块以保证安全，此时可能失去语法高亮。

## 为什么LLM使用意外语言回复？

可尝试用`--chat-language <语言>`明确设置，但LLM可能不遵守。

## 能否分享聊天记录？

{: .tip }
`/git`命令的输出不会包含在聊天上下文中

1. 将`.aider.chat.history.md`内容发布为gist
2. 拼接URL：`https://aider.chat/share/?mdurl=你的gist地址`

## 运行aider时能否手动编辑文件？

可以，但建议不要在等待回复时编辑已加入聊天的文件，可能产生冲突。

## 什么是Aider AI LLC？

aider的开发者公司，项目在[GitHub开源](https://github.com/Aider-AI/aider)并采用[Apache 2.0协议](https://github.com/Aider-AI/aider/blob/main/LICENSE.txt)。


<div style="height:80vh"></div>


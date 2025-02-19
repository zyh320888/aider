---
parent: 更多信息
nav_order: 200
description: Aider 支持几乎所有流行的编程语言。
---
# 支持的语言

Aider 能够很好地与大多数主流编程语言配合使用。这是因为顶尖的大语言模型（LLM）精通多数主流语言，并熟悉流行的库、包和框架。

Aider 对许多语言提供了专门的语法检查支持。默认情况下，Aider 在每次文件编辑后都会运行内置的语法检查器。如果发现语法错误，Aider 会主动提供修复建议。这有助于捕获代码中的小问题并快速修复。

Aider 还通过代码分析帮助 LLM 导航大型代码库，生成[仓库地图](https://aider.chat/docs/repomap.html)。目前 Aider 可以为以下列出的多种主流语言生成仓库地图。


## 如何添加对新语言的支持

即使没有仓库地图或语法检查支持，Aider 对其他语言仍然有很好的兼容性。在假设 Aider 需要增强对您所用语言的支持之前，建议先尝试使用 Aider 进行编码。

也就是说，如果 Aider 已经支持对您所用语言的语法检查，那么添加仓库地图支持是可行的。要构建仓库地图，Aider 需要来自该语言的 tree-sitter 语法的 `tags.scm` 文件。如果您能在 [GitHub issue](https://github.com/Aider-AI/aider/issues) 中找到并分享该文件，我们就有可能添加仓库地图支持。

如果 Aider 尚未支持语法检查，添加语法检查和仓库地图支持会相对复杂。这是因为 Aider 依赖于 [py-tree-sitter-languages](https://github.com/grantjenks/py-tree-sitter-languages) 来提供多种语言的预打包 tree-sitter 解析器。

Aider 需要保持在不同环境中的易安装性，因此为额外的 tree-sitter 解析器添加依赖可能会过于复杂。


<!--[[[cog
from aider.repomap import get_supported_languages_md
cog.out(get_supported_languages_md())
]]]-->

| Language | File extension | Repo map | Linter |
|:--------:|:--------------:|:--------:|:------:|
| bash                 | .bash                |          |   ✓    |
| c                    | .c                   |    ✓     |   ✓    |
| c_sharp              | .cs                  |    ✓     |   ✓    |
| commonlisp           | .cl                  |          |   ✓    |
| cpp                  | .cc                  |    ✓     |   ✓    |
| cpp                  | .cpp                 |    ✓     |   ✓    |
| css                  | .css                 |          |   ✓    |
| dockerfile           | .dockerfile          |          |   ✓    |
| dot                  | .dot                 |          |   ✓    |
| elisp                | .el                  |    ✓     |   ✓    |
| elixir               | .ex                  |    ✓     |   ✓    |
| elm                  | .elm                 |    ✓     |   ✓    |
| embedded_template    | .et                  |          |   ✓    |
| erlang               | .erl                 |          |   ✓    |
| go                   | .go                  |    ✓     |   ✓    |
| gomod                | .gomod               |          |   ✓    |
| hack                 | .hack                |          |   ✓    |
| haskell              | .hs                  |          |   ✓    |
| hcl                  | .hcl                 |    ✓     |   ✓    |
| hcl                  | .tf                  |    ✓     |   ✓    |
| html                 | .html                |          |   ✓    |
| java                 | .java                |    ✓     |   ✓    |
| javascript           | .js                  |    ✓     |   ✓    |
| javascript           | .mjs                 |    ✓     |   ✓    |
| jsdoc                | .jsdoc               |          |   ✓    |
| json                 | .json                |          |   ✓    |
| julia                | .jl                  |          |   ✓    |
| kotlin               | .kt                  |    ✓     |   ✓    |
| lua                  | .lua                 |          |   ✓    |
| make                 | .mk                  |          |   ✓    |
| objc                 | .m                   |          |   ✓    |
| ocaml                | .ml                  |    ✓     |   ✓    |
| perl                 | .pl                  |          |   ✓    |
| php                  | .php                 |    ✓     |   ✓    |
| python               | .py                  |    ✓     |   ✓    |
| ql                   | .ql                  |    ✓     |   ✓    |
| r                    | .R                   |          |   ✓    |
| r                    | .r                   |          |   ✓    |
| regex                | .regex               |          |   ✓    |
| rst                  | .rst                 |          |   ✓    |
| ruby                 | .rb                  |    ✓     |   ✓    |
| rust                 | .rs                  |    ✓     |   ✓    |
| scala                | .scala               |          |   ✓    |
| sql                  | .sql                 |          |   ✓    |
| sqlite               | .sqlite              |          |   ✓    |
| toml                 | .toml                |          |   ✓    |
| tsq                  | .tsq                 |          |   ✓    |
| typescript           | .ts                  |    ✓     |   ✓    |
| typescript           | .tsx                 |    ✓     |   ✓    |
| yaml                 | .yaml                |          |   ✓    |

<!--[[[end]]]-->



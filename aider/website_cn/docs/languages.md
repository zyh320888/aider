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
| actionscript         | .as                  |          |   ✓    |
| ada                  | .adb                 |          |   ✓    |
| ada                  | .ads                 |          |   ✓    |
| agda                 | .agda                |          |   ✓    |
| arduino              | .ino                 |    ✓     |   ✓    |
| asm                  | .asm                 |          |   ✓    |
| asm                  | .s                   |          |   ✓    |
| astro                | .astro               |          |   ✓    |
| bash                 | .bash                |          |   ✓    |
| bash                 | .sh                  |          |   ✓    |
| bash                 | .zsh                 |          |   ✓    |
| beancount            | .bean                |          |   ✓    |
| bibtex               | .bib                 |          |   ✓    |
| bicep                | .bicep               |          |   ✓    |
| bitbake              | .bb                  |          |   ✓    |
| bitbake              | .bbappend            |          |   ✓    |
| bitbake              | .bbclass             |          |   ✓    |
| c                    | .c                   |    ✓     |   ✓    |
| c                    | .h                   |    ✓     |   ✓    |
| cairo                | .cairo               |          |   ✓    |
| capnp                | .capnp               |          |   ✓    |
| chatito              | .chatito             |    ✓     |   ✓    |
| clarity              | .clar                |          |   ✓    |
| clojure              | .clj                 |          |   ✓    |
| clojure              | .cljc                |          |   ✓    |
| clojure              | .cljs                |          |   ✓    |
| clojure              | .edn                 |          |   ✓    |
| cmake                | .cmake               |          |   ✓    |
| cmake                | CMakeLists.txt       |          |   ✓    |
| commonlisp           | .cl                  |    ✓     |   ✓    |
| commonlisp           | .lisp                |    ✓     |   ✓    |
| cpon                 | .cpon                |          |   ✓    |
| cpp                  | .cc                  |    ✓     |   ✓    |
| cpp                  | .cpp                 |    ✓     |   ✓    |
| cpp                  | .cxx                 |    ✓     |   ✓    |
| cpp                  | .h++                 |    ✓     |   ✓    |
| cpp                  | .hpp                 |    ✓     |   ✓    |
| cpp                  | .hxx                 |    ✓     |   ✓    |
| csharp               | .cs                  |    ✓     |   ✓    |
| css                  | .css                 |          |   ✓    |
| csv                  | .csv                 |          |   ✓    |
| cuda                 | .cu                  |          |   ✓    |
| cuda                 | .cuh                 |          |   ✓    |
| d                    | .d                   |    ✓     |   ✓    |
| dart                 | .dart                |    ✓     |   ✓    |
| dockerfile           | Dockerfile           |          |   ✓    |
| dtd                  | .dtd                 |          |   ✓    |
| elisp                | .el                  |    ✓     |   ✓    |
| elixir               | .ex                  |    ✓     |   ✓    |
| elixir               | .exs                 |    ✓     |   ✓    |
| elm                  | .elm                 |    ✓     |   ✓    |
| erlang               | .erl                 |          |   ✓    |
| erlang               | .hrl                 |          |   ✓    |
| fennel               | .fnl                 |          |   ✓    |
| firrtl               | .fir                 |          |   ✓    |
| fish                 | .fish                |          |   ✓    |
| fortran              | .f                   |          |   ✓    |
| fortran              | .f03                 |          |   ✓    |
| fortran              | .f08                 |          |   ✓    |
| fortran              | .f90                 |          |   ✓    |
| fortran              | .f95                 |          |   ✓    |
| func                 | .fc                  |          |   ✓    |
| gdscript             | .gd                  |          |   ✓    |
| gitattributes        | .gitattributes       |          |   ✓    |
| gitcommit            | .gitcommit           |          |   ✓    |
| gitignore            | .gitignore           |          |   ✓    |
| gleam                | .gleam               |    ✓     |   ✓    |
| glsl                 | .frag                |          |   ✓    |
| glsl                 | .glsl                |          |   ✓    |
| glsl                 | .vert                |          |   ✓    |
| gn                   | .gn                  |          |   ✓    |
| gn                   | .gni                 |          |   ✓    |
| go                   | .go                  |    ✓     |   ✓    |
| gomod                | go.mod               |          |   ✓    |
| gosum                | go.sum               |          |   ✓    |
| groovy               | .groovy              |          |   ✓    |
| gstlaunch            | .launch              |          |   ✓    |
| hack                 | .hack                |          |   ✓    |
| hare                 | .ha                  |          |   ✓    |
| haskell              | .hs                  |          |   ✓    |
| haxe                 | .hx                  |          |   ✓    |
| hcl                  | .hcl                 |    ✓     |   ✓    |
| hcl                  | .tf                  |    ✓     |   ✓    |
| hcl                  | .tfvars              |    ✓     |   ✓    |
| heex                 | .heex                |          |   ✓    |
| hlsl                 | .hlsl                |          |   ✓    |
| html                 | .htm                 |          |   ✓    |
| html                 | .html                |          |   ✓    |
| hyprlang             | .hypr                |          |   ✓    |
| ispc                 | .ispc                |          |   ✓    |
| janet                | .janet               |          |   ✓    |
| java                 | .java                |    ✓     |   ✓    |
| javascript           | .js                  |    ✓     |   ✓    |
| javascript           | .jsx                 |    ✓     |   ✓    |
| javascript           | .mjs                 |    ✓     |   ✓    |
| jsdoc                | .jsdoc               |          |   ✓    |
| json                 | .json                |          |   ✓    |
| jsonnet              | .jsonnet             |          |   ✓    |
| jsonnet              | .libsonnet           |          |   ✓    |
| julia                | .jl                  |          |   ✓    |
| kconfig              | Kconfig              |          |   ✓    |
| kdl                  | .kdl                 |          |   ✓    |
| kotlin               | .kt                  |    ✓     |   ✓    |
| kotlin               | .kts                 |    ✓     |   ✓    |
| latex                | .cls                 |          |   ✓    |
| latex                | .sty                 |          |   ✓    |
| latex                | .tex                 |          |   ✓    |
| linkerscript         | .ld                  |          |   ✓    |
| llvm                 | .ll                  |          |   ✓    |
| lua                  | .lua                 |    ✓     |   ✓    |
| luadoc               | .luadoc              |          |   ✓    |
| luap                 | .luap                |          |   ✓    |
| luau                 | .luau                |          |   ✓    |
| magik                | .magik               |          |   ✓    |
| make                 | .mk                  |          |   ✓    |
| make                 | Makefile             |          |   ✓    |
| markdown             | .markdown            |          |   ✓    |
| markdown             | .md                  |          |   ✓    |
| matlab               | .m                   |          |   ✓    |
| matlab               | .mat                 |          |   ✓    |
| mermaid              | .mermaid             |          |   ✓    |
| meson                | meson.build          |          |   ✓    |
| ninja                | .ninja               |          |   ✓    |
| nix                  | .nix                 |          |   ✓    |
| nqc                  | .nqc                 |          |   ✓    |
| objc                 | .mm                  |          |   ✓    |
| odin                 | .odin                |          |   ✓    |
| org                  | .org                 |          |   ✓    |
| pascal               | .pas                 |          |   ✓    |
| pascal               | .pp                  |          |   ✓    |
| pem                  | .pem                 |          |   ✓    |
| perl                 | .pl                  |          |   ✓    |
| perl                 | .pm                  |          |   ✓    |
| pgn                  | .pgn                 |          |   ✓    |
| php                  | .php                 |    ✓     |   ✓    |
| po                   | .po                  |          |   ✓    |
| po                   | .pot                 |          |   ✓    |
| pony                 | .pony                |    ✓     |   ✓    |
| powershell           | .ps1                 |          |   ✓    |
| powershell           | .psm1                |          |   ✓    |
| printf               | .printf              |          |   ✓    |
| prisma               | .prisma              |          |   ✓    |
| properties           | .properties          |    ✓     |   ✓    |
| prql                 | .prql                |          |   ✓    |
| proto                | .proto               |          |   ✓    |
| python               | .py                  |    ✓     |   ✓    |
| python               | .pyi                 |    ✓     |   ✓    |
| python               | .pyx                 |    ✓     |   ✓    |
| qmldir               | qmldir               |          |   ✓    |
| qmljs                | .qml                 |          |   ✓    |
| r                    | .r                   |          |   ✓    |
| racket               | .rkt                 |          |   ✓    |
| regex                | .regex               |          |   ✓    |
| rego                 | .rego                |          |   ✓    |
| requirements         | requirements.txt     |          |   ✓    |
| rst                  | .rst                 |          |   ✓    |
| ruby                 | .rb                  |    ✓     |   ✓    |
| rust                 | .rs                  |    ✓     |   ✓    |
| scala                | .scala               |    ✓     |   ✓    |
| scheme               | .scm                 |          |   ✓    |
| scss                 | .scss                |          |   ✓    |
| sexp                 | .sexp                |          |   ✓    |
| sml                  | .sml                 |          |   ✓    |
| solidity             | .sol                 |          |   ✓    |
| sparql               | .rq                  |          |   ✓    |
| sql                  | .sql                 |          |   ✓    |
| squirrel             | .nut                 |          |   ✓    |
| starlark             | .bzl                 |          |   ✓    |
| strace               | .strace              |          |   ✓    |
| supercollider        | .sc                  |          |   ✓    |
| svelte               | .svelte              |          |   ✓    |
| swift                | .swift               |    ✓     |   ✓    |
| systemrdl            | .rdl                 |          |   ✓    |
| tablegen             | .td                  |          |   ✓    |
| templ                | .templ               |          |   ✓    |
| thrift               | .thrift              |          |   ✓    |
| tiger                | .tig                 |          |   ✓    |
| todotxt              | .txt                 |          |   ✓    |
| toml                 | .toml                |          |   ✓    |
| tsx                  | .tsx                 |    ✓     |   ✓    |
| turtle               | .ttl                 |          |   ✓    |
| twig                 | .twig                |          |   ✓    |
| typescript           | .ts                  |    ✓     |   ✓    |
| typst                | .typ                 |          |   ✓    |
| usd                  | .usda                |          |   ✓    |
| vala                 | .vala                |          |   ✓    |
| verilog              | .v                   |          |   ✓    |
| vhdl                 | .vhd                 |          |   ✓    |
| vhdl                 | .vhdl                |          |   ✓    |
| wat                  | .wat                 |          |   ✓    |
| webgpu               | .wgsl                |          |   ✓    |
| xml                  | .svg                 |          |   ✓    |
| xml                  | .xml                 |          |   ✓    |
| xml                  | .xml.erb             |          |   ✓    |
| yaml                 | .yaml                |          |   ✓    |
| yaml                 | .yml                 |          |   ✓    |
| yang                 | .yang                |          |   ✓    |
| yuck                 | .yuck                |          |   ✓    |
| zig                  | .zig                 |          |   ✓    |

<!--[[[end]]]-->



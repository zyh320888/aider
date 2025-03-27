---
title: 屏幕录制
has_children: true
nav_order: 75
has_toc: false
description: 使用aider开发aider的屏幕录制。
highlight_image: /assets/recordings.jpg
---

# 屏幕录制

以下是开发者使用aider来增强aider的一系列屏幕录制。
这些视频包含了对aider使用方式的解说，
可能会为您使用aider提供一些灵感。

{% assign sorted_pages = site.pages | where: "parent", "屏幕录制" | sort: "nav_order" %}
{% for page in sorted_pages %}
- [{{ page.title }}]({{ page.url | relative_url }}) - {{ page.description }}
{% endfor %}


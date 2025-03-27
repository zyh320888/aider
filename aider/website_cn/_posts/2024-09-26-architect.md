---
title: 分离代码推理和编辑
excerpt: Architect模型描述如何解决编码问题，而Editor模型将其转换为文件编辑。这种Architect/Editor方法产生了最先进的基准测试结果。
highlight_image: /assets/architect.jpg
draft: false
nav_exclude: true
---
{% if page.date %}
<p class="post-date">{{ page.date | date: "%B %d, %Y" }}</p>
{% endif %}

# 分离代码推理和编辑

Aider现在实验性地支持使用两个模型来完成每项编码任务：

- Architect模型负责描述如何解决编码问题。
- Editor模型接收Architect的解决方案，并生成特定的代码编辑指令，将这些更改应用到现有源文件中。

这种将"代码推理"和"代码编辑"分离的方法
在[aider的代码编辑基准测试](/docs/benchmarks.html#the-benchmark)中产生了最先进的结果。
使用o1-preview作为Architect，配合DeepSeek或o1-mini作为
Editor产生了85%的最高分。
使用Architect/Editor方法
还显著提高了许多模型的基准测试分数，
相比它们之前的"单独"基线分数（条纹柱）。

<style>
  .shaded td {
    background-color: #f2f2f2;
    border-top: 1px solid #ccc;
  }
  .table-container {
    max-width: 100%;
    overflow-x: auto;
  }
  .responsive-table {
    border-collapse: separate;
    border-spacing: 0;
    width: 100%;
    font-size: 16px;
    border: 1px solid #ddd;
  }
  .responsive-table th, .responsive-table td {
    padding: 8px;
    text-align: left;
    border-bottom: 1px solid #ddd;
    word-break: break-word;
  }
  .responsive-table th {
    background-color: #e2e2e2;
  }
  .responsive-table th:first-child,
  .responsive-table td:first-child {
    border-left: 1px solid #ddd;
  }
  .responsive-table th:last-child,
  .responsive-table td:last-child {
    border-right: 1px solid #ddd;
  }
  
  @media screen and (max-width: 600px) {
    .responsive-table {
      font-size: 12px;
    }
    .responsive-table th, .responsive-table td {
      padding: 4px;
    }
  }
</style>

<style>
  #passRateChart {
    max-width: 100%;
    height: auto !important;
  }
</style>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@1.0.2"></script>
{% assign sorted_data = site.data.architect | sort: "pass_rate_2" | reverse %}
<canvas id="passRateChart" width="400" height="250"></canvas>
<script>
  document.addEventListener("DOMContentLoaded", function() {
    var ctx = document.getElementById('passRateChart').getContext('2d');
    
    // Function to determine aspect ratio and base font size based on screen width
    function getChartSettings() {
      if (window.innerWidth < 600) {
        return { aspectRatio: 1, baseFontSize: 8 }; // Slightly taller for small screens
      } else if (window.innerWidth < 800) {
        return { aspectRatio: 1.2, baseFontSize: 10 }; // Slightly taller for small screens
      } else {
        return { aspectRatio: 1.4, baseFontSize: 12 }; // Slightly taller for larger screens
      }
    }

    var chartSettings = getChartSettings();
    var baseFontSize = chartSettings.baseFontSize;

    var labels = [];
    var data = [];
    var colorMapping = {
      "claude-3.5-sonnet": "rgba(75, 192, 192, 0.2)",
      "gpt-4o": "rgba(255, 99, 132, 0.2)",
      "o1-preview": "rgba(54, 162, 235, 0.2)",
      "o1-mini": "rgba(255, 206, 86, 0.2)",
      "gpt-4o-mini": "rgba(153, 102, 255, 0.2)"
    };
    var borderColorMapping = {
      "claude-3.5-sonnet": "rgba(75, 192, 192, 1)",
      "gpt-4o": "rgba(255, 99, 132, 1)",
      "o1-preview": "rgba(54, 162, 235, 1)",
      "o1-mini": "rgba(255, 206, 86, 1)",
      "gpt-4o-mini": "rgba(153, 102, 255, 1)"
    };
    var backgroundColors = [];
    var borderColors = [];
    var patterns = {};
    for (var key in colorMapping) {
      patterns[key] = ctx.createPattern(createStripePattern(colorMapping[key]), 'repeat');
    }
    {% assign grouped_data = sorted_data | group_by: "model" %}
    {% for group in grouped_data %}
      {% for item in group.items %}
        if ("{{ item.editor_model }}" == "") {
          labels.push("Baseline");
        } else {       
          labels.push("{{ item.editor_model }}/{{ item.editor_edit_format | default: item.edit_format }}");
        }
        data.push({{ item.pass_rate_2 }});
        if ("{{ item.editor_model }}" == "") {
          backgroundColors.push(patterns["{{ item.model }}"]);
        } else {
          backgroundColors.push(colorMapping["{{ item.model }}"]);
        }
        borderColors.push(borderColorMapping["{{ item.model }}"]);
      {% endfor %}
    {% endfor %}
    labels.reverse();
    data.reverse();
    backgroundColors.reverse();
    borderColors.reverse();
    var chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: '通过率',
          data: data,
          backgroundColor: backgroundColors,
          borderColor: borderColors,
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio: chartSettings.aspectRatio,
        scales: {
          y: { 
            beginAtZero: true,
            title: {
              display: true,
              text: '通过率 (%)',
              font: {
                size: baseFontSize + 6
              }
            },
            ticks: {
              font: {
                size: baseFontSize
              }
            }
          },
          x: {
            title: {
              display: true,
              text: 'Editor模型和编辑格式',
              font: {
                size: baseFontSize + 6
              }
            },
            ticks: {
              font: {
                size: baseFontSize + 4
              },
              maxRotation: 90, // Allow full rotation if needed
              minRotation: 45  // Start rotating at 45 degrees to fit more labels
            }
          }
        },
        plugins: {
          annotation: {
            annotations: {
              line1: {
                type: 'line',
                yMin: 79.7,
                yMax: 79.7,
                borderColor: 'rgba(255, 99, 132, 0.8)',
                borderWidth: 2,
                borderDash: [6, 6],
                label: {
                  content: '先前最高水平',
                  enabled: true,
                  position: 'start',
                  xAdjust: 10,
                  font: {
                    size: baseFontSize
                  }
                }
              }
            }
          },
          legend: {
            display: true,
            title: {
              display: true,
              text: 'Architect模型',
              font: {
                size: baseFontSize + 2,
                weight: 'bold'
              }
            },
            labels: {
              font: {
                size: baseFontSize + 4
              },
              generateLabels: function(chart) {
                var colorMapping = {
                  "o1-preview": "rgba(54, 162, 235, 0.2)",
                  "claude-3.5-sonnet": "rgba(75, 192, 192, 0.2)",
                  "gpt-4o": "rgba(255, 99, 132, 0.2)",
                  "o1-mini": "rgba(255, 206, 86, 0.2)",
                  "gpt-4o-mini": "rgba(153, 102, 255, 0.2)"
                };
                return Object.keys(colorMapping).reverse().map(function(key) {
                  return {
                    text: key,
                    fillStyle: colorMapping[key],
                    strokeStyle: colorMapping[key].replace('0.2', '1'),
                    lineWidth: 1
                  };
                });
              }
            }
          }
        }
      }
    });

    // Update aspect ratio and font sizes on window resize
    window.addEventListener('resize', function() {
      var newSettings = getChartSettings();
      chart.options.aspectRatio = newSettings.aspectRatio;
      baseFontSize = newSettings.baseFontSize;
      
      // Update font sizes
      chart.options.scales.y.title.font.size = baseFontSize + 6;
      chart.options.scales.y.ticks.font.size = baseFontSize;
      chart.options.scales.x.title.font.size = baseFontSize + 6;
      chart.options.scales.x.ticks.font.size = baseFontSize + 4;
      chart.options.plugins.annotation.annotations.line1.label.font.size = baseFontSize;
      chart.options.plugins.legend.title.font.size = baseFontSize + 4;
      chart.options.plugins.legend.labels.font.size = baseFontSize + 4;
      
      chart.update();
    });
  });

  function createStripePattern(baseColor) {
    var canvas = document.createElement('canvas');
    canvas.width = 10;
    canvas.height = 10;
    var ctx = canvas.getContext('2d');

    ctx.fillStyle = baseColor;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = 'rgba(0, 0, 0, 0.1)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(10, 10);
    ctx.stroke();

    return canvas;
  }
</script>

## 动机

这种方法的动机源于OpenAI的o1模型的发布。
这些模型在推理方面表现强大，但常常无法输出格式正确的
代码编辑指令。
让它们按照自己喜欢的方式描述解决方案，然后将输出传递给更传统的LLM会更有帮助。
这第二个Editor LLM可以解释解决方案描述并
生成代码编辑指令，用于更新
现有源代码。

由于前沿模型在速度和成本方面的快速改进，
这种方法最近对aider变得具有吸引力。
特别是，链接旧的LLM会非常缓慢，
与aider提供交互式AI辅助编程体验的目标不符。

## 代码推理和代码编辑

通常情况下，aider要求模型在一个提示中解决编码问题，
要求LLM解释解决方案并返回
格式良好的文件编辑系列。
所有[aider的编辑格式](/docs/more/edit-formats.html)
都要求LLM以特定的文本格式返回源代码编辑，
以便aider可以处理这些编辑并将其应用到本地源文件中。

由于这一切都发生在单个提示/响应与LLM的往返中，
模型必须在解决编码问题和遵循编辑格式之间分配注意力。

Architect/Editor方法将此分为两个推理步骤，可能
使用两个不同的LLM：

1. 解决编码问题（Architect）。
2. 将提议的解决方案转换为一系列格式良好的代码编辑（Editor）。

Architect/Editor方法允许Architect专注于解决编码问题，
并*以最自然的方式描述解决方案*。
同样，Editor可以将所有注意力集中在正确格式化编辑上，
而不需要太多考虑如何解决编码问题。

我们可以根据需求为LLM分配Architect和Editor角色。
像o1-preview这样的强大推理模型是优秀的Architect，而
Editor角色可以根据成本、速度和代码编辑技能
分配给适当的模型。

## 结果

上图和下表显示了各种Architect和Editor模型组合的
[aider代码编辑基准测试](/docs/benchmarks.html#the-benchmark)
分数。

一些值得注意的观察结果：

- 将o1-preview作为Architect与DeepSeek或o1-mini作为Editor配对，创造了远高于之前最佳分数的最高水平。这一结果使用"whole"编辑格式获得，要求Editor输出每个编辑源文件的完整更新副本。这两个步骤都相当缓慢，因此可能不适合与aider进行交互式使用。
- 将OpenAI的o1-preview与Anthropic的Sonnet作为Editor配对产生了第二好的结果。这对于能够使用两家提供商的用户来说是一个完全可行的配置。
- 在Architect/Editor配置中将许多模型与自身配对可以提供显著好处。当用作Architect/Editor对时，Sonnet、GPT-4o和GPT-4o-mini的得分都更高。
- Deepseek作为Editor模型出奇地有效。它似乎非常擅长将提议的编码解决方案转换为源文件的新版本。使用高效的"diff"编辑格式，Deepseek帮助了所有Architect模型，除了Sonnet。

## 试一试！

aider的开发版本
内置默认支持使用o1-preview、o1-mini、GPT-4o和Claude 3.5 Sonnet进行Architect/Editor编码。
使用`--architect`运行aider，或者像这样快速开始：

```
pip install -U aider-chat

# 切换到git仓库目录
cd /to/your/git/repo

# 使用Claude 3.5 Sonnet作为Architect和Editor
export ANTHROPIC_API_KEY=your-key-goes-here
aider --sonnet --architect

# 使用OpenAI模型，使用gpt-4o作为Editor
export OPENAI_API_KEY=your-key-goes-here
aider --4o --architect
aider --o1-mini --architect
aider --o1-preview --architect
```

## 更多信息

Aider有多种"聊天模式"，"architect"作为新的聊天模式可用。
`--architect`开关是`--chat-mode architect`的快捷方式。
更多详细信息，请参阅
[aider的聊天模式](/docs/usage/modes.html)文档。


## 完整结果

以下是使用各种模型作为Architect，与
各种模型作为Editor配对的基准测试结果。
每个部分都包括一个"基线"结果，
即模型在aider的正常"code"编辑模式下单独工作
（不作为Architect/Editor配置的一部分）。
这个"单独"基线代表了使用该模型与aider时
之前可用的性能。

<div class="table-container">
  <table class="responsive-table">
    <thead>
      <tr>
        <th>Architect</th>
        <th>Editor</th>
        <th>编辑格式</th>
        <th>通过率</th>
      </tr>
    </thead>
    <tbody>
      {% for group in grouped_data %}
        {% assign group_class = forloop.index | modulo: 2 | plus: 1 %}
        {% for item in group.items %}
          <tr class="{% if group_class == 1 %}shaded{% endif %}">
            <td>{{ item.model }}</td>
            <td>{% if item.editor_model %}{{ item.editor_model }}{% else %}<b>基线</b>{% endif %}</td>
            <td style="text-align: center;">{{ item.editor_edit_format | default: item.edit_format }}</td>
            <td style="text-align: right;">{{ item.pass_rate_2 }}%</td>
          </tr>
        {% endfor %}
      {% endfor %}
    </tbody>
  </table>
</div>

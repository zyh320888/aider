---
title: Sonnet表现一如既往地优秀
excerpt: Sonnet在aider代码编辑基准测试中的得分自发布以来一直保持稳定。
highlight_image: /assets/sonnet-seems-fine.jpg
---
{% if page.date %}
<p class="post-date">{{ page.date | date: "%B %d, %Y" }}</p>
{% endif %}

# Sonnet表现一如既往地优秀

最近有很多猜测认为Sonnet被降级、削弱或性能变差。
通过API执行[aider代码编辑基准测试](/docs/benchmarks.html#the-benchmark)时，
Sonnet表现一如既往地优秀。

下图显示了Claude 3.5 Sonnet随时间的性能变化。
它展示了Sonnet发布以来执行的每次干净、可比较的基准测试运行。
进行基准测试的原因各不相同，通常是
为了评估对aider系统提示的小改动的影响。

图表显示了一些变异，但没有表明存在明显的
性能下降。
基准测试结果总是有一些变异，通常在使用相同提示的运行之间有+/- 2%
的差异。

值得注意的是，这些结果不会捕捉到Anthropic网络聊天对Sonnet使用的任何变化。

<div class="chart-container" style="position: relative; height:400px; width:100%">
    <canvas id="sonnetPerformanceChart"></canvas>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdn.jsdelivr.net/npm/moment@2.29.4/moment.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-moment@1.0.1/dist/chartjs-adapter-moment.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('sonnetPerformanceChart').getContext('2d');
    var sonnetData = {{ site.data.sonnet-fine | jsonify }};

    var chartData = sonnetData.map(item => ({
        x: moment(item.date).toDate(),
        y1: item.pass_rate_1,
        y2: item.pass_rate_2
    })).sort((a, b) => a.x - b.x);

    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: '通过率 1',
                data: chartData.map(item => ({ x: item.x, y: item.y1 })),
                backgroundColor: 'rgb(75, 192, 192)',
                pointRadius: 5,
                pointHoverRadius: 7
            }, {
                label: '通过率 2',
                data: chartData.map(item => ({ x: item.x, y: item.y2 })),
                backgroundColor: 'rgb(255, 99, 132)',
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: '通过率 (%)',
                        font: {
                            size: 14
                        }
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                },
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    },
                    title: {
                        display: true,
                        text: '日期',
                        font: {
                            size: 14
                        }
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Claude 3.5 Sonnet随时间的性能表现',
                    font: {
                        size: 18
                    }
                },
                legend: {
                    labels: {
                        font: {
                            size: 14
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += context.parsed.y.toFixed(1) + '%';
                            }
                            return label;
                        }
                    }
                }
            }
        }
    });
});
</script>

> 此图显示了Claude 3.5 Sonnet在[aider的代码编辑基准测试](/docs/benchmarks.html#the-benchmark)中
> 随时间的性能表现。"通过率1"代表初始成功率，而"通过率2"显示第二次尝试修复测试错误后的成功率。
> [aider LLM代码编辑排行榜](https://aider.chat/docs/leaderboards/)
> 根据通过率2对模型进行排名。


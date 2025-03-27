<style>
    .chart-container {
        position: relative;
        width: 100%;
        max-width: 800px;
        margin: 0 auto;
    }
</style>

<div class="chart-container">
    <canvas id="syntaxErrorsChart"></canvas>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function () {
    var ctx = document.getElementById('syntaxErrorsChart').getContext('2d');
    var chartContainer = document.querySelector('.chart-container');
    
    var yamlData = {{ site.data.code-in-json | jsonify }};
    
    var models = [...new Set(yamlData.map(item => item.model))].sort();
    var editFormats = [...new Set(yamlData.map(item => item.edit_format))];
    
    var datasets = editFormats.map(format => ({
        label: format,
        data: models.map(model => {
            var items = yamlData.filter(d => d.model === model && d.edit_format === format);
            if (items.length === 0) return null;
            var totalErrors = items.reduce((sum, item) => sum + item.syntax_errors + item.indentation_errors, 0);
            return totalErrors;
        }),
        backgroundColor: function(context) {
            const format = context.dataset.label;
            if (format === 'Markdown') {
                return 'rgba(54, 162, 235, 0.8)';
            } else if (format.startsWith('JSON')) {
                const ctx = context.chart.ctx;
                const gradient = ctx.createPattern(createStripedCanvas(format === 'JSON (strict)'), 'repeat');
                return gradient;
            } else {
                return 'rgba(75, 192, 192, 0.8)';
            }
        },
    }));

    var data = {
        labels: models,
        datasets: datasets
    };

    function getAspectRatio() {
        var width = chartContainer.offsetWidth;
        // 逐渐将宽高比从2（横向）变为1（方形）
        return Math.max(1, Math.min(2, width / 300));
    }

    var config = {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            aspectRatio: getAspectRatio(),
            scales: {
                x: {
                    title: {
                        display: true,
                        text: '模型'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: '5次运行的语法错误总数'
                    },
                    max: 35
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: '按模型和代码包装策略的语法错误',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += context.parsed.y;
                            }
                            return label;
                        }
                    }
                }
            }
        },
        plugins: [{
            afterDraw: function(chart) {
                var ctx = chart.ctx;
                chart.data.datasets.forEach(function(dataset, i) {
                    var meta = chart.getDatasetMeta(i);
                    meta.data.forEach(function(bar, index) {
                        var data = dataset.data[index];
                        if (data !== null) {
                            ctx.fillStyle = '#000000';
                            ctx.textAlign = 'center';
                            ctx.textBaseline = 'bottom';
                            ctx.fillText(data, bar.x, bar.y - 5);
                        }
                    });
                });
            }
        }]
    };

    var chart = new Chart(ctx, config);

    function resizeChart() {
        chart.options.aspectRatio = getAspectRatio();
        chart.resize();
    }

    window.addEventListener('resize', resizeChart);

    // 初始调整以设置正确的大小
    resizeChart();
});

function createStripedCanvas(isStrict) {
    const patternCanvas = document.createElement('canvas');
    const patternContext = patternCanvas.getContext('2d');
    const size = 10;
    patternCanvas.width = size;
    patternCanvas.height = size;

    patternContext.fillStyle = 'rgba(255, 99, 132, 0.8)';
    patternContext.fillRect(0, 0, size, size);

    if (isStrict) {
        patternContext.strokeStyle = 'rgba(255, 255, 255, 0.8)';
        patternContext.lineWidth = 0.75;
        patternContext.beginPath();
        patternContext.moveTo(0, 0);
        patternContext.lineTo(size, size);
        patternContext.stroke();
    }

    return patternCanvas;
}
</script>

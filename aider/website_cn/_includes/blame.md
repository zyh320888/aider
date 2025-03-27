<div class="chart-container">
    <canvas id="blameChart" style="margin-top: 20px"></canvas>
</div>
<div class="chart-container">
    <canvas id="linesChart" style="margin-top: 20px"></canvas>
</div>

<style>
.chart-container {
    position: relative;
    width: 100%;
    height: 300px;
}
</style>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdn.jsdelivr.net/npm/moment"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-moment"></script>
<script>
document.addEventListener('DOMContentLoaded', function () {
    var blameCtx = document.getElementById('blameChart').getContext('2d');
    var linesCtx = document.getElementById('linesChart').getContext('2d');
    
    var labels = [{% for row in site.data.blame %}'{{ row.end_tag }}',{% endfor %}];
    
    var blameData = {
        labels: labels,
        datasets: [{
            label: '每个版本中Aider编写的新代码百分比',
            data: [{% for row in site.data.blame %}{ x: '{{ row.end_tag }}', y: {{ row.aider_percentage }}, lines: {{ row.aider_total }} },{% endfor %}],
            backgroundColor: 'rgba(54, 162, 235, 0.8)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    };

    var linesData = {
        labels: labels,
        datasets: [{
            label: 'Aider',
            data: [{% for row in site.data.blame %}{ x: '{{ row.end_tag }}', y: {{ row.aider_total }} },{% endfor %}],
            backgroundColor: 'rgba(54, 162, 235, 0.8)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        },
        {
            label: '人类',
            data: [{% for row in site.data.blame %}{ x: '{{ row.end_tag }}', y: {{ row.total_lines | minus: row.aider_total }} },{% endfor %}],
            backgroundColor: 'rgba(200, 200, 200, 0.8)',
            borderColor: 'rgba(200, 200, 200, 1)',
            borderWidth: 1
        }]
    };

    var blameChart = new Chart(blameCtx, {
        type: 'bar',
        data: blameData,
        options: {
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'category',
                    title: {
                        display: true,
                        text: '版本'
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: '新代码百分比'
                    },
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            var label = 'Aider的贡献';
                            var value = context.parsed.y || 0;
                            var lines = context.raw.lines || 0;
                            return `${label}: ${Math.round(value)}% (${lines} 行)`;
                        }
                    }
                },
                title: {
                    display: true,
                    text: '按版本划分的Aider编写的新代码百分比',
                    font: {
                        size: 16
                    }
                }
            }
        }
    });

    var linesChart = new Chart(linesCtx, {
        type: 'bar',
        data: linesData,
        options: {
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'category',
                    stacked: true,
                    title: {
                        display: true,
                        text: '版本'
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                },
                y: {
                    stacked: true,
                    title: {
                        display: true,
                        text: '新代码行数'
                    },
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'chartArea',
                    reverse: true
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            var label = context.dataset.label;
                            var value = context.parsed.y || 0;
                            return `${label}: ${value}`;
                        }
                    }
                },
                title: {
                    display: true,
                    text: '按版本划分的新代码行数',
                    font: {
                        size: 16
                    }
                }
            }
        }
    });
});
</script>

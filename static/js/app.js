// Main JavaScript for Music Data Visualization

// Initialize all charts when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

async function initializeDashboard() {
    try {
        // Load data overview
        await loadOverview();
        
        // Load all visualizations
        await Promise.all([
            loadReleaseTrend(),
            loadAlbumTypes(),
            loadMusicGenres(),
            loadTopAlbumTypes(),
            loadTopArtists(),
            loadWordCloud(),
            loadSentiment()
        ]);
    } catch (error) {
        console.error('Error initializing dashboard:', error);
    }
}

// Load overview statistics
async function loadOverview() {
    try {
        const response = await fetch('/api/overview');
        const data = await response.json();
        
        document.getElementById('total-songs').textContent = data.total_songs || 0;
        document.getElementById('total-artists').textContent = data.total_artists || 0;
        document.getElementById('total-albums').textContent = data.total_albums || 0;
        document.getElementById('total-comments').textContent = data.total_comments || 0;
    } catch (error) {
        console.error('Error loading overview:', error);
    }
}

// Load release trend chart
async function loadReleaseTrend() {
    try {
        const response = await fetch('/api/release-trend');
        const data = await response.json();
        
        const option = {
            title: {
                text: '音乐发布趋势分析',
                left: 'center',
                textStyle: {
                    color: '#667eea',
                    fontSize: 20
                }
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross'
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: data.years,
                name: '年份',
                nameTextStyle: {
                    fontSize: 14
                }
            },
            yAxis: {
                type: 'value',
                name: '发布数量',
                nameTextStyle: {
                    fontSize: 14
                }
            },
            series: [{
                name: '音乐发布数量',
                type: 'line',
                smooth: true,
                data: data.counts,
                itemStyle: {
                    color: '#667eea'
                },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: 'rgba(102, 126, 234, 0.5)' },
                        { offset: 1, color: 'rgba(102, 126, 234, 0.1)' }
                    ])
                },
                emphasis: {
                    focus: 'series'
                }
            }]
        };
        
        const chart = echarts.init(document.getElementById('trend-chart'));
        chart.setOption(option);
        
        // Make chart responsive
        window.addEventListener('resize', () => chart.resize());
    } catch (error) {
        console.error('Error loading release trend:', error);
        document.getElementById('trend-chart').innerHTML = '<div class="error">加载趋势数据失败</div>';
    }
}

// Load album types chart
async function loadAlbumTypes() {
    try {
        const response = await fetch('/api/album-types');
        const data = await response.json();
        
        const option = {
            title: {
                text: '专辑类型分布',
                left: 'center',
                textStyle: {
                    color: '#667eea'
                }
            },
            tooltip: {
                trigger: 'item',
                formatter: '{b}: {c} ({d}%)'
            },
            legend: {
                orient: 'vertical',
                left: 'left'
            },
            series: [{
                name: '专辑类型',
                type: 'pie',
                radius: '55%',
                data: data.labels.map((label, index) => ({
                    name: label,
                    value: data.data[index]
                })),
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }]
        };
        
        const chart = echarts.init(document.getElementById('album-types-chart'));
        chart.setOption(option);
        
        window.addEventListener('resize', () => chart.resize());
    } catch (error) {
        console.error('Error loading album types:', error);
    }
}

// Load music genres chart
async function loadMusicGenres() {
    try {
        const response = await fetch('/api/music-genres');
        const data = await response.json();
        
        const option = {
            title: {
                text: '音乐类型占比',
                left: 'center',
                textStyle: {
                    color: '#667eea'
                }
            },
            tooltip: {
                trigger: 'item',
                formatter: '{b}: {c} ({d}%)'
            },
            legend: {
                orient: 'vertical',
                left: 'left'
            },
            series: [{
                name: '音乐类型',
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                },
                label: {
                    show: true,
                    formatter: '{b}: {d}%'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: 16,
                        fontWeight: 'bold'
                    }
                },
                data: data.labels.map((label, index) => ({
                    name: label,
                    value: data.data[index]
                }))
            }]
        };
        
        const chart = echarts.init(document.getElementById('genres-chart'));
        chart.setOption(option);
        
        window.addEventListener('resize', () => chart.resize());
    } catch (error) {
        console.error('Error loading music genres:', error);
    }
}

// Load top album types chart
async function loadTopAlbumTypes() {
    try {
        const response = await fetch('/api/top-album-types');
        const data = await response.json();
        
        const option = {
            title: {
                text: '专辑类型TOP10',
                left: 'center',
                textStyle: {
                    color: '#667eea'
                }
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'value'
            },
            yAxis: {
                type: 'category',
                data: data.labels,
                axisLabel: {
                    interval: 0
                }
            },
            series: [{
                name: '数量',
                type: 'bar',
                data: data.data,
                itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                        { offset: 0, color: '#667eea' },
                        { offset: 1, color: '#764ba2' }
                    ])
                },
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowColor: 'rgba(0,0,0,0.3)'
                    }
                }
            }]
        };
        
        const chart = echarts.init(document.getElementById('top-albums-chart'));
        chart.setOption(option);
        
        window.addEventListener('resize', () => chart.resize());
    } catch (error) {
        console.error('Error loading top album types:', error);
    }
}

// Load top artists chart
async function loadTopArtists() {
    try {
        const response = await fetch('/api/top-artists');
        const data = await response.json();
        
        const option = {
            title: {
                text: '艺术家作品数量TOP5',
                left: 'center',
                textStyle: {
                    color: '#667eea'
                }
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: data.labels,
                axisLabel: {
                    interval: 0,
                    rotate: 30
                }
            },
            yAxis: {
                type: 'value',
                name: '作品数量'
            },
            series: [{
                name: '作品数量',
                type: 'bar',
                data: data.data,
                itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: '#667eea' },
                        { offset: 1, color: '#764ba2' }
                    ]),
                    borderRadius: [5, 5, 0, 0]
                },
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowColor: 'rgba(0,0,0,0.3)'
                    }
                }
            }]
        };
        
        const chart = echarts.init(document.getElementById('top-artists-chart'));
        chart.setOption(option);
        
        window.addEventListener('resize', () => chart.resize());
    } catch (error) {
        console.error('Error loading top artists:', error);
    }
}

// Load word cloud
async function loadWordCloud() {
    try {
        const response = await fetch('/api/wordcloud');
        const data = await response.json();
        
        const option = {
            title: {
                text: '音乐名称词云',
                left: 'center',
                textStyle: {
                    color: '#667eea',
                    fontSize: 20
                }
            },
            tooltip: {
                show: true
            },
            series: [{
                type: 'wordCloud',
                gridSize: 8,
                sizeRange: [12, 60],
                rotationRange: [-45, 45],
                shape: 'circle',
                width: '100%',
                height: '100%',
                drawOutOfBound: false,
                textStyle: {
                    fontFamily: 'sans-serif',
                    fontWeight: 'bold',
                    color: function () {
                        const colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe'];
                        return colors[Math.floor(Math.random() * colors.length)];
                    }
                },
                emphasis: {
                    textStyle: {
                        shadowBlur: 10,
                        shadowColor: '#333'
                    }
                },
                data: data.words
            }]
        };
        
        const chart = echarts.init(document.getElementById('wordcloud'));
        chart.setOption(option);
        
        window.addEventListener('resize', () => chart.resize());
    } catch (error) {
        console.error('Error loading word cloud:', error);
        document.getElementById('wordcloud').innerHTML = '<div class="error">加载词云失败</div>';
    }
}

// Load sentiment analysis
async function loadSentiment() {
    try {
        const response = await fetch('/api/sentiment');
        const data = await response.json();
        
        // Update sentiment statistics
        document.getElementById('positive-count').textContent = data.positive || 0;
        document.getElementById('neutral-count').textContent = data.neutral || 0;
        document.getElementById('negative-count').textContent = data.negative || 0;
        
        document.getElementById('positive-pct').textContent = (data.positive_pct || 0) + '%';
        document.getElementById('neutral-pct').textContent = (data.neutral_pct || 0) + '%';
        document.getElementById('negative-pct').textContent = (data.negative_pct || 0) + '%';
        
        // Create sentiment chart
        const option = {
            title: {
                text: '评论情感分布',
                left: 'center',
                textStyle: {
                    color: '#667eea'
                }
            },
            tooltip: {
                trigger: 'item',
                formatter: '{b}: {c} ({d}%)'
            },
            legend: {
                orient: 'vertical',
                left: 'left'
            },
            series: [{
                name: '情感',
                type: 'pie',
                radius: '55%',
                data: [
                    { name: '正面', value: data.positive || 0, itemStyle: { color: '#28a745' } },
                    { name: '中性', value: data.neutral || 0, itemStyle: { color: '#ffc107' } },
                    { name: '负面', value: data.negative || 0, itemStyle: { color: '#dc3545' } }
                ],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }]
        };
        
        const chart = echarts.init(document.getElementById('sentiment-chart'));
        chart.setOption(option);
        
        window.addEventListener('resize', () => chart.resize());
    } catch (error) {
        console.error('Error loading sentiment:', error);
    }
}

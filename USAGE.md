# 使用指南

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python app.py
```

应用将在 http://localhost:5000 启动

### 3. 访问仪表板

打开浏览器访问 http://localhost:5000 即可查看音乐数据分析可视化仪表板。

## 功能说明

### 数据概览
页面顶部显示4个关键指标卡片：
- 歌曲总数
- 艺术家数量
- 专辑数量
- 评论总数

### 音乐发布趋势分析
使用折线图展示音乐作品随年份的发布趋势，可以：
- 查看不同年份的音乐发布数量
- 分析市场活跃期和低迷期
- 识别音乐市场的发展趋势

### 音乐结构分析
包含两个并列的图表：
1. **专辑类型分布** - 饼图展示不同专辑类型的占比
2. **音乐类型占比** - 环形图展示不同音乐类型的分布

### 排行洞察
1. **专辑类型TOP10** - 横向柱状图展示最受欢迎的专辑类型
2. **艺术家作品数量TOP5** - 柱状图展示最高产的艺术家

### 音乐名称词云
使用词云可视化展示高频出现的音乐名称和关键词，字体大小表示热度。

### 用户评论情感分析
分析评论区的用户情感倾向：
- 情感分布饼图（正面/中性/负面）
- 详细的情感统计数据
- AI驱动的情感分析总结

## 数据采集

### 使用内置示例数据
项目已包含示例数据（data/music_data.json），可直接运行查看效果。

### 采集新数据
运行爬虫脚本采集网易云音乐数据：

```bash
python crawler/netease_crawler.py
```

注意事项：
- 网易云音乐可能有反爬虫机制
- 请合理设置爬取间隔
- 遵守网站的使用条款

### 自定义数据
您也可以准备自己的数据，格式参考 data/music_data.json：

```json
{
  "songs": [
    {
      "id": 1,
      "name": "歌曲名",
      "artists": ["艺术家1", "艺术家2"],
      "album": "专辑名",
      "album_type": "录音室专辑",
      "publish_time": 1234567890000,
      "duration": 240000,
      "popularity": 95
    }
  ],
  "comments": [
    {
      "song_id": 1,
      "song_name": "歌曲名",
      "content": "评论内容",
      "time": 1234567890000,
      "liked_count": 100
    }
  ]
}
```

## 配置说明

### 情感分析API
如果您有Qwen3-30B-A3B API密钥，可以在 `analysis/sentiment_analyzer.py` 中配置：

```python
class SentimentAnalyzer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or "YOUR_API_KEY_HERE"
```

默认使用简单的规则基础情感分析，适用于中文评论。

### 爬虫配置
在 `crawler/netease_crawler.py` 中可以调整爬取参数：

```python
# 爬取10个歌单，每个歌单20首歌
data = crawler.crawl_music_data(num_playlists=10, songs_per_playlist=20)
```

## API接口

应用提供以下RESTful API接口：

| 接口 | 说明 |
|------|------|
| GET / | 主页面 |
| GET /api/overview | 数据概览统计 |
| GET /api/release-trend | 音乐发布趋势数据 |
| GET /api/album-types | 专辑类型分布数据 |
| GET /api/music-genres | 音乐类型占比数据 |
| GET /api/top-album-types | TOP10专辑类型 |
| GET /api/top-artists | TOP5艺术家 |
| GET /api/wordcloud | 词云数据 |
| GET /api/sentiment | 情感分析结果 |

## 故障排除

### 问题：图表不显示
- 检查浏览器控制台是否有JavaScript错误
- 确认ECharts库加载成功
- 检查网络连接是否正常

### 问题：数据为空
- 确认 data/music_data.json 文件存在
- 检查JSON格式是否正确
- 查看Flask日志输出

### 问题：爬虫无法获取数据
- 网易云音乐可能更新了反爬虫策略
- 尝试调整请求间隔
- 检查网络连接

### 问题：中文显示乱码
- 确保所有文件使用UTF-8编码
- 检查浏览器字符编码设置

## 性能优化建议

1. **数据缓存** - 对于大数据集，考虑使用Redis缓存分析结果
2. **异步加载** - 图表可以使用懒加载提升页面加载速度
3. **数据分页** - 大量数据时实现分页加载
4. **CDN加速** - 静态资源使用CDN加速

## 扩展开发

### 添加新的分析维度
1. 在 `analysis/data_analyzer.py` 中添加分析方法
2. 在 `app.py` 中添加对应的API路由
3. 在前端添加图表展示

### 自定义主题
修改 `static/css/style.css` 中的颜色变量：

```css
/* 主色调 */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### 集成其他数据源
在 `crawler` 目录下添加新的爬虫模块，参考 `netease_crawler.py` 的实现。

## 部署建议

### 开发环境
使用Flask内置服务器：
```bash
python app.py
```

### 生产环境
使用Gunicorn + Nginx：
```bash
# 安装Gunicorn
pip install gunicorn

# 启动应用
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

配置Nginx反向代理以提供更好的性能和安全性。

## 许可与贡献

本项目采用MIT许可证，欢迎贡献代码和提出建议！

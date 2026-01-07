# 🎵 音乐大数据分析可视化系统

一个基于Flask的音乐大数据分析可视化项目，爬取网易云音乐数据并提供多维度的数据分析和可视化展示。

## 项目特性

### 数据采集
- 🎼 爬取网易云音乐热门歌单数据
- 💬 采集歌曲评论用于情感分析
- 🔄 支持反爬虫机制处理

### 数据分析与可视化

1. **数据概览** - 展示歌曲、艺术家、专辑、评论总数
2. **音乐发布趋势分析** - 折线图展示音乐作品发布时间趋势
3. **专辑类型分析** - 分析不同专辑类型（录音室专辑、现场专辑等）的分布
4. **音乐类型占比分析** - 展示不同音乐类型（流行、摇滚、古典等）的占比
5. **专辑类型TOP10** - 列出最受欢迎的专辑类型
6. **艺术家作品数量TOP5** - 展示发布作品最多的艺术家
7. **音乐名称词云** - 使用词云展示热门音乐关键词
8. **用户评论情感分析** - 基于AI分析评论区用户情感趋势

### 技术架构

- **后端**: Flask 3.0
- **前端**: HTML5 + CSS3 + JavaScript
- **数据可视化**: ECharts 5.4
- **数据处理**: Pandas, NumPy
- **中文分词**: jieba
- **词云生成**: wordcloud
- **情感分析**: Qwen3-30B-A3B API（可选）

## 安装部署

### 1. 克隆项目

```bash
git clone https://github.com/among-the-mountain/musicdata.git
cd musicdata
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行应用

```bash
python app.py
```

应用将在 http://localhost:5000 启动

## 使用说明

### 数据采集（可选）

项目已包含示例数据。如需采集新数据：

```bash
python crawler/netease_crawler.py
```

注意：网易云音乐可能有反爬虫机制，请合理使用。

### 自定义配置

- 修改 `crawler/netease_crawler.py` 调整爬取参数
- 修改 `analysis/sentiment_analyzer.py` 配置情感分析API密钥

## 页面布局

### 整体结构（从上到下）

1. **页面顶部** - 项目概览与数据统计
2. **核心趋势区** - 音乐发布趋势折线图
3. **结构分析区** - 专辑类型和音乐类型分析
4. **排行洞察区** - TOP榜单分析
5. **内容热点区** - 音乐名称词云
6. **用户反馈区** - 评论情感趋势分析

### 设计特点

- ✅ 响应式设计，所有容器自适应高度和宽度
- ✅ 渐变色彩方案，视觉效果优雅
- ✅ 卡片式布局，信息层次清晰
- ✅ 交互式图表，支持数据探索

## 项目结构

```
musicdata/
├── app.py                      # Flask主应用
├── requirements.txt            # 项目依赖
├── README.md                   # 项目文档
├── crawler/                    # 爬虫模块
│   ├── __init__.py
│   └── netease_crawler.py     # 网易云音乐爬虫
├── analysis/                   # 数据分析模块
│   ├── __init__.py
│   ├── data_analyzer.py       # 数据分析器
│   └── sentiment_analyzer.py  # 情感分析器
├── data/                       # 数据存储
│   └── music_data.json        # 音乐数据
├── static/                     # 静态文件
│   ├── css/
│   │   └── style.css          # 样式文件
│   └── js/
│       └── app.js             # 前端脚本
└── templates/                  # HTML模板
    └── index.html             # 主页面
```

## API接口

- `GET /` - 主页面
- `GET /api/overview` - 数据概览
- `GET /api/release-trend` - 发布趋势数据
- `GET /api/album-types` - 专辑类型数据
- `GET /api/music-genres` - 音乐类型数据
- `GET /api/top-album-types` - TOP10专辑类型
- `GET /api/top-artists` - TOP5艺术家
- `GET /api/wordcloud` - 词云数据
- `GET /api/sentiment` - 情感分析数据

## 技术亮点

1. **模块化设计** - 爬虫、分析、可视化模块分离
2. **数据处理** - 使用Pandas进行高效数据处理
3. **智能分析** - 支持AI驱动的情感分析
4. **交互式可视化** - ECharts提供丰富的图表交互
5. **响应式布局** - 适配各种屏幕尺寸

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 致谢

- 网易云音乐提供数据来源
- 参考项目：[music163-miningr](https://github.com/LindiaC/music163-miningr)
- ECharts可视化库
- Flask Web框架
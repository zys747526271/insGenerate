# Instagram 视频批量下载与合并工具

这是一个用于批量下载Instagram视频并将其合并的工具套件，包含两个主要组件：视频下载器和视频合并器。

## 功能特点

- 批量下载Instagram视频
- 自动生成过渡画面
- 视频合并与转场效果
- 支持自定义标题和作者
- 美观的进度显示

## 快速开始

### 安装

1. 克隆项目：
```bash
git clone https://github.com/kakaoxy/insGenerate.git
cd insGenerate
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

### 基本使用

1. 准备视频链接文件（links.txt）：
```
https://www.instagram.com/reel/xxx
https://www.instagram.com/reel/yyy
https://www.instagram.com/reel/zzz
```

2. 下载视频：
```bash
python video_downloader.py -i links.txt -o ./11-23
```

3. 合并视频：
```bash
python video_merger.py -i "11-23" -o "11-23-final.mp4"
```

## 详细使用说明

### 1. 视频下载器 (video_downloader.py)

用于从文本文件中批量下载Instagram视频。

#### 命令行参数：
```bash
python video_downloader.py [选项]

选项：
  -i, --input     输入文件路径，包含Instagram视频链接
  -o, --output    输出目录路径
  -c, --cookie    Cookie文件路径（可选）
```

#### 使用示例：
```bash
# 基本使用
python video_downloader.py -i links.txt -o ./downloads

# 使用Cookie文件（推荐，避免访问限制）
python video_downloader.py -i links.txt -o ./downloads -c cookies.txt
```

### 2. 视频合并器 (video_merger.py)

将下载的视频合并为一个文件，并添加过渡画面。

#### 命令行参数：
```bash
python video_merger.py [选项]

选项：
  -i, --input     输入视频目录路径
  -o, --output    输出视频文件路径
  -t, --title     标题文本（默认：今日份快乐）
  -a, --author    作者名称（默认：Cynvann）
  --test          运行测试模式
```

#### 使用示例：
```bash
# 基本使用
python video_merger.py -i "11-23" -o "11-23-final.mp4"

# 自定义标题和作者
python video_merger.py -i "11-23" -o "11-23-final.mp4" -t "今日份萌宠" -a "Cynvann"

# 测试过渡画面
python video_merger.py --test
```

## 过渡画面说明

1. 第一个过渡画面：
   - 显示日期
   - 显示标题
   - 显示作者名称
   - 显示视频序号

2. 中间过渡画面：
   - 显示视频序号
   - 显示进度（如：2/5）

3. 最终过渡画面：
   - 显示互动提示
   - 包含点赞、关注、转发呼吁

## 系统要求

- Python 3.x
- Windows操作系统
- 必要的Python包（见 requirements.txt）

## 开发相关

### 目录结构
```
insGenerate/
├── video_downloader.py  # 视频下载器
├── video_merger.py      # 视频合并器
├── requirements.txt     # 项目依赖
├── .gitignore          # Git忽略配置
└── README.md           # 说明文档
```

### Git提交规范

提交信息格式：
- 功能更新：`feat: add video merger transition screens`
- 修复问题：`fix: resolve video download timeout issue`
- 文档更新：`docs: update README with usage examples`

## 注意事项

1. 视频下载：
   - 确保提供的Instagram链接有效
   - 建议使用Cookie以避免访问限制
   - 下载失败会自动重试

2. 视频合并：
   - 支持的视频格式：MP4
   - 确保输入目录中只包含要合并的视频
   - 视频会按文件名顺序合并

## 常见问题

1. 下载失败：
   - 检查网络连接
   - 验证Cookie是否有效
   - 确认链接是否可访问

2. 合并失败：
   - 检查视频格式是否支持
   - 确保有足够的磁盘空间
   - 验证输入路径是否正确

## 更新日志

### v1.1 (2023-11-23)
- 引入Gradio Web界面，提供更友好的用户交互
- 新增三个功能标签页：
  1. 📥 下载视频：仅下载视频
  2. 🔄 合并视频：仅合并已下载的视频
  3. 🚀 一键下载合并：自动完成下载和合并
- 支持拖拽或粘贴Instagram链接，自动提取有效链接
- 优化文件路径选择和配置
- 改进错误处理和用户反馈

### v1.0.0
- 实现基础下载功能
- 添加视频合并功能
- 支持自定义过渡画面
- 添加命令行参数支持

## 贡献指南

1. 感谢yt-dlp ：`https://github.com/yt-dlp/yt-dlp.git`
2. 感谢moviepy：`https://github.com/Zulko/moviepy.git`
3. 感谢ffmpeg-python：`https://github.com/kkroening/ffmpeg-python.git`

感谢windsurf：项目全程使用windsurf搭建，没有任何手写代码





## 许可证

MIT License

# Instagram 视频批量下载与合并工具

这是一个用于批量下载Instagram视频并将其合并的工具套件，包含三个主要组件：视频下载器、视频合并器和Web界面。

## 功能特点

- 批量下载Instagram视频
- 自动生成过渡画面
- 视频合并与转场效果
- 支持自定义标题和作者
- 美观的进度显示
- 直观的Web操作界面
- 支持视频预览和手动排序

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

#### 方式一：Web界面（推荐）

1. 启动Web界面：
```bash
python web_ui.py
```

2. 在浏览器中访问显示的地址（通常是 http://127.0.0.1:7860）

3. 使用Web界面：
   - 在"下载视频"标签页：
     * 粘贴Instagram视频链接
     * 选择输出目录
     * 点击"开始下载"
   - 在"合并视频"标签页：
     * 选择要合并的视频
     * 预览视频内容
     * 设置第一个视频（其他视频将按文件名排序）
     * 设置输出文件名
     * 添加标题和作者信息
     * 点击"开始合并"

#### 方式二：命令行

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

### 1. Web界面 (web_ui.py)

提供图形化界面，方便直观地操作下载和合并功能。

#### 主要功能：
- 视频下载：
  * 支持单个或批量链接输入
  * 实时显示下载进度
  * 自动创建输出目录

- 视频合并：
  * 视频预览功能
  * 支持手动设置第一个视频
  * 其他视频自动按文件名排序
  * 自定义标题和作者信息
  * 实时显示合并进度

#### 使用说明：
1. 启动服务：
```bash
python web_ui.py
```

2. 在浏览器中访问显示的地址

3. 根据界面提示操作：
   - 下载视频时确保提供有效的Instagram链接
   - 合并视频时可以预览视频内容
   - 支持设置第一个视频，其他视频将按文件名排序
   - 合并完成后可以在指定目录找到输出文件

### 2. 视频下载器 (video_downloader.py)

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

### 3. 视频合并器 (video_merger.py)

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

过渡画面是在视频之间添加的转场效果，包含以下元素：
- 视频序号（1/5、2/5 等）
- 标题文本（可自定义）
- 作者名称（可自定义）
- 优雅的淡入淡出效果
- 可选的音效

## 注意事项

1. 视频下载：
   - 确保提供有效的Instagram视频链接
   - 推荐使用Cookie文件以避免访问限制
   - 下载失败时会自动重试

2. 视频合并：
   - 支持mp4和mov格式的视频
   - 所有视频将被统一调整为720x1280分辨率
   - 建议使用Web界面预览和排序视频
   - 确保有足够的磁盘空间

3. Web界面：
   - 支持实时预览视频
   - 可以手动设置第一个视频
   - 其他视频将按文件名自动排序
   - 合并完成后会显示输出文件路径

## 常见问题

1. 下载失败：
   - 检查网络连接
   - 确认链接有效性
   - 尝试使用Cookie文件
   - 等待一段时间后重试

2. 合并失败：
   - 确认视频文件完整性
   - 检查磁盘空间
   - 确保输出路径有写入权限
   - 查看日志获取详细错误信息

## 更新日志

### v1.1.0
- 添加Web界面支持
- 新增视频预览功能
- 支持手动设置第一个视频
- 优化视频合并流程
- 改进错误处理和提示

### v1.0.0
- 初始版本发布
- 支持批量下载Instagram视频
- 实现视频合并功能
- 添加过渡画面效果

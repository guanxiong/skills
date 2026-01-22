# yt-dlp-downloader Skill

一个使用 yt-dlp 下载视频的 Skill，支持从 YouTube 和 1000+ 其他网站下载视频。

## 功能特性

- 从 YouTube、Vimeo、Bilibili 等 1000+ 网站下载视频
- 支持视频质量选择（自动选择最佳质量）
- 下载字幕（包括自动生成字幕）
- 下载播放列表
- 获取视频信息（标题、时长、描述等）
- 支持批量下载
- **智能代理检测**（Chrome + Clash，新增）
- **YouTube 连接性测试**（非大陆地区服务，新增）
- **自动查找并测试代理**（新增）
- **代理信息输出**（新增）
- **文件存在性检查**（新增）
- **智能重复下载避免**（新增）
- **自动使用 Chrome Cookies**（年龄限制、地区限制视频）

## 安装

### 1. 安装 yt-dlp

在使用这个 Skill 之前，需要先安装 yt-dlp：

```bash
pip install yt-dlp
```

或者下载独立可执行文件：

```bash
# Windows
winget install yt-dlp

# macOS
brew install yt-dlp

# Linux
sudo apt install yt-dlp
```

### 2. 安装 Skill

将 `yt-dlp-downloader.skill` 文件安装到 Claude 的 skills 目录中。

## 使用方法

### 基本用法

只需提供视频链接即可：

```
帮我下载这个视频：https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### 下载到指定目录

```
把 https://youtube.com/watch?v=xxx 这个视频下载到 D:/Downloads 目录
```

### 下载带字幕

```
下载这个视频 https://youtube.com/watch?v=xxx 并下载字幕
```

### 下载播放列表

```
帮我下载这个播放列表的前5个视频 https://youtube.com/playlist?list=xxx
```

### 只下载音频

```
下载这个视频的音频 https://youtube.com/watch?v=xxx
```

### 获取视频信息

```
看看这个视频的信息 https://youtube.com/watch?v=xxx
```

### 文件已存在处理

**重要**: 下载前 Skill 会检查输出目录中是否已存在同名文件。如果找到：

- **显示信息** - 列出现有文件及其大小
- **自动跳过** - yt-dlp 自动跳过重复下载，避免覆盖
- **正常行为** - 这是为了防止文件覆盖的机制

**如果需要重新下载**：

1. 删除现有文件，然后重试
2. 下载到其他目录
3. 手动指定不同的文件名（暂不支持）

**示例输出**：
```
[Checking for existing files...]
[INFO] Found 1 existing file(s) for this video:
  - 我的视频.f401.mp4 (100.50 MB)
[INFO] yt-dlp will skip re-download if file already exists.
[INFO] This is normal behavior to avoid duplicates.

[INFO] To re-download:
  1. Delete existing file, then try again
  2. Download to a different directory
  3. Specify a different output filename
```

## 高级选项

### 使用代理

**自动代理（推荐）**：
Skill 会自动读取 Chrome 的代理设置。如果你在 Chrome 中配置了代理，Skill 会自动使用。

```bash
# 在 Chrome 中设置代理后，直接使用即可
下载这个视频：https://www.youtube.com/watch?v=xxx
```

**手动指定代理**：
如果不想使用 Chrome 的代理，可以手动指定：

```
使用代理 http://127.0.0.1:7890 下载视频：https://www.youtube.com/watch?v=xxx
```

### 选择视频质量

```
下载 720p 质量的视频 https://youtube.com/watch?v=xxx
```

### 下载多语言字幕

```
下载视频 https://youtube.com/watch?v=xxx 并下载中英文字幕
```

### 下载元数据

```
下载视频 https://youtube.com/watch?v=xxx 并保存元数据和缩略图
```

## 支持的网站

- YouTube（视频、播放列表、频道）
- Bilibili
- Vimeo
- Twitter/X
- Facebook
- Instagram
- TikTok
- Reddit
- Twitch
- 以及 1000+ 其他网站...

## 常见问题

### Q: yt-dlp 未安装怎么办？
A: 运行 `pip install yt-dlp` 安装 yt-dlp

### Q: 下载失败怎么办？
A: 可能原因：
1. 视频已删除或不可用
2. 视频有地区限制
3. 视频需要登录
4. 网络连接问题

### Q: 如何下载年龄限制视频？
A: 需要使用浏览器 cookies。参考 yt-dlp 文档。

### Q: 下载速度慢怎么办？
A: 尝试下载较低质量的视频，或检查网络连接。

## 技术细节

Skill 包含以下文件：

- `SKILL.md` - 主要说明文档
- `scripts/download_video.py` - 下载脚本
- `references/commands.md` - 命令参考手册

## 示例对话

**用户：** 下载这个视频 https://www.youtube.com/watch?v=dQw4w9WgXcQ

**Claude：** 开始下载视频...
下载完成！视频已保存为：Rick Astley - Never Gonna Give You Up.webm

**用户：** 看看这个视频有多长 https://www.youtube.com/watch?v=xxx

**Claude：** 视频信息：
- 标题：示例视频
- 时长：10分30秒
- 上传时间：2024-01-01
- 描述：这是视频描述...

## 更多信息

- yt-dlp GitHub: https://github.com/yt-dlp/yt-dlp
- 支持的网站列表: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

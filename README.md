# Claude Skills

自定义 Claude Code 技能集合，扩展 AI 助手的能力。

## 技能列表

### 1. skills-publish
**管理 skills 项目的发布流程，包括：检查技能变化、更新 README.md、git 提交并推送到 GitHub。当用户说：提交技能、发布更新、push skills、更新技能仓库时使用此技能。**

**使用示例**：
```
- - 核心功能亮点
```

### 2. word-to-h5-agreement
**将Word格式的法律协议文档（用户协议、隐私协议、法律条款）转换为美观的响应式H5页面。仅处理用户指定的单个文件，不联想生成其他文件。当用户请求：转换指定Word文件为HTML、查看Word文档的H5效果、在浏览器中预览Word协议时使用此技能。**

**使用示例**：
```

```

### 3. yt-dlp-downloader
**Download videos from YouTube and 1000+ other websites using yt-dlp. Use when you need to: (1) Download videos from YouTube, Bilibili, Vimeo, or any supported site, (2) Extract audio from videos, (3) Download subtitles, (4) Download entire playlists, (5) Get video information (title, duration, description), (6) Select video quality or format, (7) Download video metadata or thumbnails**

**使用示例**：
```

```

---

## 目录结构

```
.claude/skills/
├── skills/                     # 各技能目录
└── README.md                   # 本文件
```

---

## 贡献

欢迎提交新的技能或改进现有技能！

---

## 许可

本项目采用开源许可证，详见 [LICENSE](LICENSE)

---

*最后更新：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*

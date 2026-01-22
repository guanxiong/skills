# Claude Skills

自定义 Claude Code 技能集合，扩展 AI 助手的能力。

## 技能列表

### skills-publish
**管理 skills 项目的发布流程，包括：检查技能变化、更新 README.md、git 提交并推送到 GitHub**

**使用示例**：
```
- 提交技能更新
- 发布 skills 到 GitHub
- 检查并提交技能变化
```

### word-to-h5-agreement
**将 Word 格式的法律协议文档（用户协议、隐私协议、法律条款）转换为美观的响应式 H5 页面**

**使用示例**：
```
- 帮我把这个用户协议文档转换成 H5 页面：C:\Documents\用户协议.docx
- 转换这个隐私协议：D:\Contracts\隐私政策2024版.docx
- 法务 doc 转成 html：C:\Agreements\服务条款.docx
```

### yt-dlp-downloader
**使用 yt-dlp 从 YouTube、Bilibili、Vimeo 等 1000+ 网站下载视频**

**使用示例**：
```
- 下载这个视频：https://www.youtube.com/watch?v=a2sfkJeXmE0
- 帮我把这个 Bilibili 视频下载到 D:\Videos 目录：https://www.bilibili.com/video/BV1xx411c7mD
- 只下载音频：https://www.youtube.com/watch?v=VIDEO_ID
```

---

## 目录结构

```
.claude/skills/
├── skills-publish/        # 技能发布工具
├── word-to-h5-agreement/  # Word 转 H5 协议
├── yt-dlp-downloader/     # 视频下载器
└── README.md              # 本文件
```

---

## 贡献

欢迎提交新的技能或改进现有技能！

---

## 许可

本项目采用开源许可证，详见 [LICENSE](LICENSE)

---

*最后更新：2026-01-22 11:26:54

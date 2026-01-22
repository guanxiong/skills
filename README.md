# Claude Skills

自定义 Claude Code 技能集合，扩展 AI 助手的能力。

## 技能列表

### 1. word-to-h5-agreement
**Word 协议文档转 H5 页面**

将 Word 格式的法律协议文档（用户协议、隐私协议、法律条款）转换为美观的响应式 H5 页面。

**核心亮点**：
- 智能识别文档标题和生效日期
- 完整保留 Word 文档格式（加粗、斜体、下划线、超链接）
- 智能序号修复（自动修复缺失/不连续的标题序号）
- 响应式设计（适配 PC/移动端/小程序）
- 严格对照原文，不修改任何内容

**使用示例**：
```
帮我把这个用户协议文档转换成 H5 页面：C:\Documents\用户协议.docx

转换这个隐私协议：D:\Contracts\隐私政策2024版.docx

把 Word 文档生成网页：C:\Agreements\服务条款.docx
```

**生成文件命名**：
- 隐私协议 → `privacy-policy-YYYYMMDD.html`
- 用户协议 → `user-agreement-YYYYMMDD.html`
- 儿童隐私保护 → `children-privacy-YYYYMMDD.html`

---

### 2. yt-dlp-downloader
**视频下载工具**

使用 yt-dlp 从 YouTube、Bilibili、Vimeo 等 1000+ 网站下载视频。

**核心亮点**：
- 自动检测并使用代理（Chrome 代理 / Clash）
- 默认使用浏览器 Cookie（支持年龄限制/私密视频）
- 智能文件存在检测（避免重复下载）
- 支持字幕、元数据、缩略图下载
- 支持播放列表下载
- 支持 1000+ 视频网站

**使用示例**：
```
下载这个视频：https://www.youtube.com/watch?v=a2sfkJeXmE0

帮我把这个 Bilibili 视频下载到 D:\Videos 目录：https://www.bilibili.com/video/BV1xx411c7mD

下载 YouTube 播放列表的前 5 个视频：https://www.youtube.com/playlist?list=PLxxxxxx

获取这个视频的信息：https://www.youtube.com/watch?v=dQw4w9WgXcQ

只下载音频：https://www.youtube.com/watch?v=VIDEO_ID

下载视频并下载中英文字幕：https://www.youtube.com/watch?v=VIDEO_ID
```

**自动代理优先级**：
1. Chrome 浏览器代理（系统设置）
2. Clash 代理（端口 7890-7899）
3. 手动指定代理

---

## 安装

每个技能都有独立的依赖，请参考各个技能的 `SKILL.md` 文件安装所需依赖。

### 通用安装
```bash
# 进入技能目录
cd C:\Users\BRN\.claude\skills\<skill-name>

# 安装依赖（如果有 requirements.txt）
pip install -r requirements.txt
```

---

## 目录结构

```
.claude/skills/
├── word-to-h5-agreement/          # Word 转 H5 协议
│   ├── SKILL.md                   # 技能说明
│   ├── scripts/                   # 脚本文件
│   ├── references/                # 参考文档
│   └── requirements.txt           # Python 依赖
│
├── yt-dlp-downloader/             # 视频下载器
│   ├── SKILL.md                   # 技能说明
│   ├── scripts/                   # 脚本文件
│   └── references/                # 参考文档
│
└── README.md                      # 本文件
```

---

## 贡献

欢迎提交新的技能或改进现有技能！

1. Fork 本仓库
2. 创建技能分支
3. 提交更改
4. 发起 Pull Request

---

## 许可

本项目采用开源许可证，详见 [LICENSE](LICENSE)

---

## 相关链接

- [Claude Code](https://claude.ai/code)
- [Claude 技能文档](https://docs.claude.com/skills)

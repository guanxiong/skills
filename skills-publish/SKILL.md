---
name: skills-publish
description: 管理 skills 项目的发布流程，包括：检查技能变化、更新 README.md、git 提交并推送到 GitHub。当用户说：提交技能、发布更新、push skills、更新技能仓库时使用此技能。
---

# Skills Publish 技能发布工具

管理 Claude Skills 项目的发布流程，自动检查技能变化、更新 README、提交并推送到 GitHub。

## 工作流程

### 1. 检查技能变化

扫描 skills 目录下所有技能，检测：
- 新增的技能目录
- 修改的文件（通过 git status）
- 需要更新 README 的内容

### 2. 更新 README

自动更新项目根目录的 README.md，包括：
- 所有技能的名称和描述
- 每个技能的使用示例（自然语言提示词）
- 核心功能亮点

### 3. Git 提交和推送

自动执行：
```bash
git add .
git commit -m "描述性提交信息"
git push
```

## 使用示例

```
提交技能更新

发布 skills 到 GitHub

检查并提交技能变化

更新技能仓库并推送

帮我发布这次技能更新
```

## 技能目录结构

```
skills-publish/
├── SKILL.md              # 技能说明（本文件）
└── scripts/              # 脚本目录
    └── publish.py        # 发布脚本
```

## 注意事项

- 自动提交前会显示所有变更
- 支持自定义提交信息
- 备份 .backup 目录会被忽略

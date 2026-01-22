"""
Skills Publish - 自动检查技能变化、更新 README、提交并推送到 GitHub
"""

import os
import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime

# 修复 Windows 控制台中文编码问题
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


class SkillsPublisher:
    def __init__(self, skills_dir=None):
        self.skills_dir = Path(skills_dir) if skills_dir else Path(__file__).parent.parent.parent
        self.readme_path = self.skills_dir / "README.md"

    def get_skill_dirs(self):
        """获取所有技能目录（排除 .git、.backup 等）"""
        skills = []
        for item in self.skills_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                if not item.name.endswith('.backup'):
                    skill_file = item / "SKILL.md"
                    if skill_file.exists():
                        skills.append(item)
        return sorted(skills, key=lambda x: x.name)

    def parse_skill_info(self, skill_dir):
        """解析 SKILL.md 获取技能信息"""
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            return None

        content = skill_file.read_text(encoding='utf-8')

        # 解析 frontmatter
        name = ""
        description = ""
        if content.startswith('---'):
            frontmatter = content.split('---')[1]
            name_match = re.search(r'name:\s*(.+)', frontmatter)
            desc_match = re.search(r'description:\s*(.+)', frontmatter)
            if name_match:
                name = name_match.group(1).strip()
            if desc_match:
                description = desc_match.group(1).strip()

        return {
            "name": name or skill_dir.name,
            "description": description or "",
            "dir_name": skill_dir.name
        }

    def get_examples_from_skill(self, skill_dir):
        """从 SKILL.md 中提取使用示例"""
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            return []

        content = skill_file.read_text(encoding='utf-8')
        examples = []

        # 查找使用示例部分
        lines = content.split('\n')
        in_code_block = False
        in_example_section = False

        for i, line in enumerate(lines):
            # 检测代码块
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                if not in_code_block and examples:
                    break  # 代码块结束
                continue

            # 检测示例部分开始
            if '使用示例' in line or 'Usage Examples' in line or 'Examples' in line:
                in_example_section = True
                continue

            # 提取示例内容
            if in_example_section and in_code_block:
                if line.strip() and not line.strip().startswith('#'):
                    examples.append(line.strip())

        return examples[:5]  # 最多返回 5 个示例

    def check_git_changes(self):
        """检查 git 状态"""
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=self.skills_dir,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()

    def generate_readme(self):
        """生成 README.md 内容"""
        skills = self.get_skill_dirs()
        skill_infos = [self.parse_skill_info(s) for s in skills]
        skill_infos = [s for s in skill_infos if s]

        # 手动定义每个技能的信息和示例
        skill_data = {
            "skills-publish": {
                "name": "skills-publish",
                "description": "管理 skills 项目的发布流程，包括：检查技能变化、更新 README.md、git 提交并推送到 GitHub",
                "examples": [
                    "提交技能更新",
                    "发布 skills 到 GitHub",
                    "检查并提交技能变化"
                ]
            },
            "word-to-h5-agreement": {
                "name": "word-to-h5-agreement",
                "description": "将 Word 格式的法律协议文档（用户协议、隐私协议、法律条款）转换为美观的响应式 H5 页面",
                "examples": [
                    "帮我把这个用户协议文档转换成 H5 页面：C:\\Documents\\用户协议.docx",
                    "转换这个隐私协议：D:\\Contracts\\隐私政策2024版.docx",
                    "法务 doc 转成 html：C:\\Agreements\\服务条款.docx"
                ]
            },
            "yt-dlp-downloader": {
                "name": "yt-dlp-downloader",
                "description": "使用 yt-dlp 从 YouTube、Bilibili、Vimeo 等 1000+ 网站下载视频",
                "examples": [
                    "下载这个视频：https://www.youtube.com/watch?v=a2sfkJeXmE0",
                    "帮我把这个 Bilibili 视频下载到 D:\\Videos 目录：https://www.bilibili.com/video/BV1xx411c7mD",
                    "只下载音频：https://www.youtube.com/watch?v=VIDEO_ID"
                ]
            }
        }

        readme = """# Claude Skills

自定义 Claude Code 技能集合，扩展 AI 助手的能力。

## 技能列表

"""
        for skill_dir in skills:
            skill_name = skill_dir.name
            if skill_name in skill_data:
                data = skill_data[skill_name]
                example_lines = "\n".join([f"- {e}" for e in data["examples"]])
                readme += f"""### {data['name']}
**{data['description']}**

**使用示例**：
```
{example_lines}
```

"""

        readme += """---

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

*最后更新："""
        readme += datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        readme += "\n"
        return readme

    def update_readme(self):
        """更新 README.md"""
        new_readme = self.generate_readme()
        self.readme_path.write_text(new_readme, encoding='utf-8')
        print("✓ README.md updated")

    def commit_and_push(self, message="Update skills"):
        """提交并推送到 GitHub"""
        os.chdir(self.skills_dir)

        # 添加所有更改
        subprocess.run(["git", "add", "."], capture_output=True)
        print("✓ git add .")

        # 提交
        commit_msg = message or f"Update skills - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True)
        print(f"✓ git commit -m \"{commit_msg}\"")

        # 推送
        result = subprocess.run(["git", "push"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ git push")
        else:
            print(f"✗ git push failed: {result.stderr}")

    def publish(self, commit_message=None):
        """执行完整的发布流程"""
        print("=" * 50)
        print(" Skills Publish - Release Tool")
        print("=" * 50)
        print()

        # 1. 检查变化
        changes = self.check_git_changes()
        if changes:
            print("Changes detected:")
            print(changes)
            print()
        else:
            print("No changes detected")
            return

        # 2. 更新 README
        print("Updating README.md...")
        self.update_readme()
        print()

        # 3. 提交并推送
        print("Committing and pushing to GitHub...")
        self.commit_and_push(commit_message)
        print()

        print("=" * 50)
        print(" Release completed!")
        print("=" * 50)


if __name__ == "__main__":
    import sys

    message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    publisher = SkillsPublisher()
    publisher.publish(message)

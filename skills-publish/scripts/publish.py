"""
Skills Publish - 自动检查技能变化、更新 README、提交并推送到 GitHub
"""

import os
import subprocess
import re
from pathlib import Path
from datetime import datetime


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
        in_example_section = False
        for line in content.split('\n'):
            if '使用示例' in line or 'Usage Examples' in line or 'Examples' in line:
                in_example_section = True
                continue
            if in_example_section:
                if line.strip().startswith('##') or line.strip().startswith('---'):
                    break
                if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('```'):
                    examples.append(line.strip())

        return examples[:3]  # 最多返回 3 个示例

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

        readme = f"""# Claude Skills

自定义 Claude Code 技能集合，扩展 AI 助手的能力。

## 技能列表

"""
        for i, skill in enumerate(skill_infos, 1):
            examples = self.get_examples_from_skill(self.skills_dir / skill["dir_name"])
            example_text = "\n".join([f"- {e}" for e in examples]) if examples else ""

            readme += f"""### {i}. {skill["name"]}
**{skill["description"]}**

**使用示例**：
```
{example_text}
```

"""

        readme += """---

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
"""
        return readme

    def update_readme(self):
        """更新 README.md"""
        new_readme = self.generate_readme()
        self.readme_path.write_text(new_readme, encoding='utf-8')
        print(f"[OK] README.md updated")

    def commit_and_push(self, message="Update skills"):
        """提交并推送到 GitHub"""
        os.chdir(self.skills_dir)

        # 添加所有更改
        subprocess.run(["git", "add", "."], capture_output=True)
        print(f"[OK] git add .")

        # 提交
        commit_msg = message or f"Update skills - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True)
        print(f"[OK] git commit -m \"{commit_msg}\"")

        # 推送
        result = subprocess.run(["git", "push"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[OK] git push")
        else:
            print(f"[FAIL] git push 失败: {result.stderr}")

    def publish(self, commit_message=None):
        """执行完整的发布流程"""
        print("=" * 50)
        print(" Skills Publish - 技能发布工具")
        print("=" * 50)
        print()

        # 1. 检查变化
        changes = self.check_git_changes()
        if changes:
            print("检测到变化：")
            print(changes)
            print()
        else:
            print("没有检测到变化")
            return

        # 2. 更新 README
        print("更新 README.md...")
        self.update_readme()
        print()

        # 3. 提交并推送
        print("提交并推送到 GitHub...")
        self.commit_and_push(commit_message)
        print()

        print("=" * 50)
        print(" 发布完成！")
        print("=" * 50)


if __name__ == "__main__":
    import sys

    message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    publisher = SkillsPublisher()
    publisher.publish(message)

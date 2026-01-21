import os
from pathlib import Path

dir_path = Path(r"D:\Seafile\国宝奇妙游小游戏小程序\08 小红书+微信小程序方案\09 条款文件\唐小妹协议条款 final")
html_files = list(dir_path.glob("*.html"))

for html_file in sorted(html_files):
    print(f"\n=== {html_file.name} ===")
    content = html_file.read_text(encoding='utf-8')
    start = content.find('<nav class="footer-links">')
    if start != -1:
        end = content.find('</nav>', start)
        nav_section = content[start:end+len('</nav>')]
        print(nav_section)

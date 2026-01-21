@echo off
cd /d "D:\Seafile\国宝奇妙游小游戏小程序\08 小红书+微信小程序方案\09 条款文件\唐小妹协议条款 final"
for %%f in (*.html) do (
    echo === %%f ===
    findstr /C:"footer-links" /A:4 "%%f"
    echo.
)

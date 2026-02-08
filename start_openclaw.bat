@echo off
chcp 65001 > nul
echo 正在启动 OpenClaw 对话工具...
echo ================================
pause
echo 启动中...
python openclaw_chat.py
echo ================================
echo 按任意键退出...
pause > nul

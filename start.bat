@echo off
chcp 65001 >nul
echo ==================================================
echo 飞书股票智能机器人 - 启动脚本
echo ==================================================
echo.

echo [1/3] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH
    pause
    exit /b 1
)
echo ✅ Python环境正常
echo.

echo [2/3] 检查依赖包...
python -c "import requests, websocket, schedule" >nul 2>&1
if errorlevel 1 (
    echo 📦 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
)
echo ✅ 依赖包正常
echo.

echo [3/3] 启动机器人...
echo ==================================================
echo 🚀 机器人启动中...
echo ==================================================
echo.
echo 💡 提示:
echo   - 按 Ctrl+C 停止机器人
echo   - 日志文件: feishu_bot.log
echo   - 在飞书中发送 '帮助' 查看可用命令
echo.
echo ==================================================

python main.py

if errorlevel 1 (
    echo.
    echo ❌ 机器人异常退出
    pause
)

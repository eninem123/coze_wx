@echo off
cls
echo ==================================================
echo Feishu Stock Bot - Startup Script
echo ==================================================
echo.

echo [1/3] Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)
echo OK: Python environment is ready
echo.

echo [2/3] Checking dependencies...
python -c "import requests, websocket, schedule, base64, json" >nul 2>&1
if errorlevel 1 (
    echo INSTALLING: Dependencies not found, installing...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)
echo OK: Dependencies are ready
echo.

echo [3/3] Starting bot...
echo ==================================================
echo STARTING: Bot is starting...
echo ==================================================
echo.
echo TIPS:
echo   - Press Ctrl+C to stop the bot
echo   - Log file: feishu_bot.log
echo   - Send 'help' in Feishu to see available commands
echo   - Send images for automatic analysis

echo.
echo FEATURES:
echo   ✅ Two-way Q&A with context
echo   ✅ Automatic stock analysis push
echo   ✅ Image analysis with Doubao
echo   ✅ Local WebSocket connection
echo.
echo ==================================================

python main.py

if errorlevel 1 (
    echo.
    echo ERROR: Bot exited with error
    pause
)

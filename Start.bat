@echo off
cd /d "%~dp0"
if not exist .venv-jarvis\.jarvis-vision-ready (
    py -3.11 scripts\setup.py --vision-only
    if errorlevel 1 (
        pause
        exit /b 1
    )
    type nul > .venv-jarvis\.jarvis-vision-ready
)
.venv-jarvis\Scripts\python.exe scripts\start.py --vision-only
pause

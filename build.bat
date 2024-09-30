@echo off

where pyinstaller >nul 2>nul
if %errorlevel% neq 0 (
    echo PyInstaller not installed. Please install it before running this script.
    exit /b 1
)
pyinstaller --add-data "assets;assets" main.py
pyinstaller --onefile update.py


pause

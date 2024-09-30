@echo off

where pyinstaller >nul 2>nul
if %errorlevel% neq 0 (
    echo PyInstaller not installed. Please install it before running this script.
    exit /b 1
)
if %1%==main (
    pyinstaller --noconsole --onefile --add-data "assets;assets" %1%.py
)
if %1%==updater (
    pyinstaller --noconsole --onefile  %1%.py
)
pause

@echo off
color 0A
echo ================================================================
echo           PAPER AI - QUICK START INSTALLER
echo ================================================================
echo.
echo This script will set up everything automatically!
echo.
pause

echo.
echo [Step 1/4] Installing Poppler...
echo ================================================================
call fix_poppler.bat
if %errorlevel% neq 0 (
    echo [ERROR] Poppler installation failed
    echo Please install manually and try again
    pause
    exit /b 1
)

echo.
echo [INFO] Poppler installed. Please CLOSE this window and open a NEW terminal.
echo.
echo After opening a new terminal, run: quickstart_step2.bat
echo.
pause

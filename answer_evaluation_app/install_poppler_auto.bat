@echo off
echo ====================================
echo Poppler Auto-Installer
echo ====================================
echo.
echo This will automatically download and install Poppler
echo.
pause

PowerShell -ExecutionPolicy Bypass -File "%~dp0install_poppler_auto.ps1"

echo.
echo ====================================
echo Next Steps:
echo ====================================
echo 1. CLOSE this command prompt window
echo 2. Open a NEW command prompt
echo 3. Navigate back to: cd C:\Users\nk\paperai\answer_evaluation_app
echo 4. Run: python app.py
echo.
pause

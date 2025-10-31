@echo off
echo ====================================
echo Installing Poppler for PDF Processing
echo ====================================
echo.

echo This will download and set up Poppler (needed for PDF to image conversion)
echo.

REM Create tools directory
if not exist "C:\poppler" mkdir "C:\poppler"

echo.
echo Please follow these steps:
echo.
echo 1. Download Poppler from: https://github.com/oschwartz10612/poppler-windows/releases/
echo 2. Download the latest "Release-XX.XX.X-X.zip" file
echo 3. Extract it to C:\poppler
echo 4. Add C:\poppler\Library\bin to your PATH
echo.
echo Alternatively, run this PowerShell command as Administrator:
echo.
echo winget install sharkdp.poppler
echo.
echo OR use Chocolatey:
echo.
echo choco install poppler
echo.
echo After installation, restart your command prompt and run the app again.
echo.

pause

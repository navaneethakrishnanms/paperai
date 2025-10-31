@echo off
color 0A
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                   POPPLER INSTALLATION WIZARD                  ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Your app needs Poppler to process PDF files.
echo.
echo Choose installation method:
echo.
echo [1] Automatic Installation (Recommended)
echo     - Downloads and installs Poppler automatically
echo     - No manual steps required
echo.
echo [2] Winget Installation
echo     - Uses Windows Package Manager
echo     - Requires Windows 11 or updated Windows 10
echo.
echo [3] Chocolatey Installation
echo     - Uses Chocolatey package manager
echo     - Requires Chocolatey to be installed
echo.
echo [4] View Manual Installation Instructions
echo.
echo [5] Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto auto
if "%choice%"=="2" goto winget
if "%choice%"=="3" goto choco
if "%choice%"=="4" goto manual
if "%choice%"=="5" goto end

echo Invalid choice! Please run again.
pause
goto end

:auto
echo.
echo Starting automatic installation...
call install_poppler_auto.bat
goto end

:winget
echo.
echo Starting Winget installation...
call install_poppler_winget.bat
goto end

:choco
echo.
echo Starting Chocolatey installation...
call install_poppler_choco.bat
goto end

:manual
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                 MANUAL INSTALLATION STEPS                      ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 1. Visit: https://github.com/oschwartz10612/poppler-windows/releases/
echo 2. Download the latest Release-XX.XX.X-X.zip file
echo 3. Extract to C:\poppler
echo 4. Add to PATH:
echo    - Right-click 'This PC' → Properties
echo    - Advanced system settings → Environment Variables
echo    - Under 'User variables', edit 'Path'
echo    - Click 'New' and add: C:\poppler\Library\bin
echo 5. Click OK on all windows
echo 6. RESTART your terminal
echo.
echo For detailed guide, see POPPLER_FIX.md
echo.
pause
goto end

:end
echo.
echo Thank you!

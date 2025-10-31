@echo off
color 0B
cls
echo.
echo ===============================================================================
echo                    ✅ YOUR SYSTEM HAS BEEN FIXED!
echo ===============================================================================
echo.
echo 🔧 WHAT WAS FIXED:
echo    - PowerShell encoding error in install_poppler_auto.ps1
echo    - All Python files verified and error-free
echo    - Created easy installation scripts
echo.
echo ===============================================================================
echo                    📋 NEXT STEPS - CHOOSE YOUR PATH
echo ===============================================================================
echo.
echo [1] QUICK START (Recommended - Automated Setup)
echo     - Installs everything automatically
echo     - Just follow the prompts
echo.
echo [2] MANUAL SETUP (Advanced Users)
echo     - More control over installation
echo     - Step-by-step process
echo.
echo [3] VERIFY EXISTING INSTALLATION
echo     - Check if everything is already installed
echo     - Useful if you ran setup before
echo.
echo [4] VIEW DOCUMENTATION
echo     - Complete guide
echo     - Troubleshooting tips
echo.
echo [5] EXIT
echo.
echo ===============================================================================
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto quickstart
if "%choice%"=="2" goto manual
if "%choice%"=="3" goto verify
if "%choice%"=="4" goto docs
if "%choice%"=="5" goto end

:quickstart
cls
echo.
echo ===============================================================================
echo                    🚀 QUICK START MODE
echo ===============================================================================
echo.
echo This will automatically:
echo   1. Install Poppler (PDF processing tool)
echo   2. Install all Python dependencies
echo   3. Verify everything is working
echo.
echo ⚠️ IMPORTANT: After step 1, you MUST:
echo    - CLOSE this terminal
echo    - OPEN A NEW terminal
echo    - Run: quickstart_step2.bat
echo.
pause
call quickstart_step1.bat
goto end

:manual
cls
echo.
echo ===============================================================================
echo                    🔧 MANUAL SETUP MODE
echo ===============================================================================
echo.
echo Step 1: Install Poppler
echo ------------------------
echo Run: fix_poppler.bat
echo Choose option 1 (Automatic Installation)
echo.
echo Step 2: Restart Terminal
echo ------------------------
echo Close this window and open a NEW terminal
echo.
echo Step 3: Install Dependencies
echo ----------------------------
echo Run: pip install -r requirements.txt
echo.
echo Step 4: Verify Installation
echo ---------------------------
echo Run: verify_system.bat
echo.
echo Step 5: Start Application
echo -------------------------
echo Run: python app.py
echo.
echo Press any key to open fix_poppler.bat...
pause
call fix_poppler.bat
goto end

:verify
cls
echo.
echo ===============================================================================
echo                    ✅ SYSTEM VERIFICATION
echo ===============================================================================
echo.
call verify_system.bat
echo.
echo If everything passed, you can start the app with: python app.py
echo.
pause
goto end

:docs
cls
echo.
echo ===============================================================================
echo                    📚 DOCUMENTATION
echo ===============================================================================
echo.
echo Opening documentation files...
echo.
if exist "ALL_FIXED.txt" (
    notepad ALL_FIXED.txt
) else (
    echo Documentation file not found!
)
echo.
pause
goto end

:end
echo.
echo ===============================================================================
echo Thank you for using Paper AI Answer Evaluation System!
echo ===============================================================================
echo.
pause

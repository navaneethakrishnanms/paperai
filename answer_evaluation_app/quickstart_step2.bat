@echo off
color 0A
echo ================================================================
echo           PAPER AI - INSTALLATION STEP 2
echo ================================================================
echo.

echo [Step 2/4] Verifying Poppler Installation...
echo ================================================================
pdfinfo -v
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Poppler is not in PATH yet!
    echo Please make sure you:
    echo 1. Closed the previous terminal
    echo 2. Opened a NEW terminal
    echo 3. Navigated back to this directory
    echo.
    pause
    exit /b 1
)
echo [SUCCESS] Poppler is working!
echo.

echo [Step 3/4] Installing Python Dependencies...
echo ================================================================
echo This may take 10-15 minutes depending on your internet speed...
echo.
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Dependency installation failed
    echo Try running: python -m pip install --upgrade pip
    echo Then run this script again
    pause
    exit /b 1
)
echo [SUCCESS] All dependencies installed!
echo.

echo [Step 4/4] Verifying Installation...
echo ================================================================
call verify_system.bat

echo.
echo ================================================================
echo              INSTALLATION COMPLETE!
echo ================================================================
echo.
echo To start the application, run:
echo     python app.py
echo.
echo Then open your browser to: http://localhost:5000
echo.
pause

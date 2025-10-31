@echo off
echo ============================================
echo Testing DeepSeek-OCR Fix
echo ============================================
echo.

REM Activate conda environment
call conda activate torch_gpu
if errorlevel 1 (
    echo Error: Could not activate torch_gpu environment
    echo Please make sure conda is installed and torch_gpu environment exists
    pause
    exit /b 1
)

echo Environment activated: torch_gpu
echo.

REM Run the test script
echo Running test script...
echo.
python test_deepseek_fix.py

echo.
echo ============================================
echo Test Complete!
echo ============================================
echo.
echo To start the main application, run: start.bat
echo.
pause

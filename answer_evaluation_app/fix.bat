@echo off
echo.
echo ====================================================
echo    AUTO-DIAGNOSTIC TOOL
echo ====================================================
echo.
echo This will check:
echo   1. PDF content (text vs scanned)
echo   2. Database status  
echo   3. Extraction patterns
echo.
echo Starting diagnosis...
echo.

cd /d %~dp0
python auto_diagnose.py

echo.
echo ====================================================
echo Press any key to exit...
pause >nul

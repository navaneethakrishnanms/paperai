@echo off
echo ====================================
echo Checking Poppler Installation
echo ====================================
echo.

echo Checking if pdfinfo is available...
where pdfinfo >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✓ pdfinfo found!
    echo.
    echo Version information:
    pdfinfo -v
    echo.
    echo ✓ Poppler is installed and working!
    echo.
    echo You can now run your app: python app.py
) else (
    echo ✗ pdfinfo not found in PATH
    echo.
    echo Poppler is NOT installed or not in PATH.
    echo.
    echo Please run: fix_poppler.bat
    echo.
    echo Or manually check:
    echo 1. Is Poppler installed at C:\poppler?
    echo 2. Is the bin folder added to your PATH?
    echo 3. Did you restart your terminal after installation?
)

echo.
pause

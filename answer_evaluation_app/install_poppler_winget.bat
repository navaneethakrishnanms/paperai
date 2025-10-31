@echo off
echo ====================================
echo Installing Poppler via Winget
echo ====================================
echo.

winget install --id=sharkdp.poppler -e

echo.
echo ====================================
echo Installation Complete!
echo ====================================
echo.
echo IMPORTANT: Restart your terminal and verify with: pdfinfo -v
echo.
pause

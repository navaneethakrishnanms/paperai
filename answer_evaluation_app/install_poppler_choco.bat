@echo off
echo ====================================
echo Installing Poppler via Chocolatey
echo ====================================
echo.
echo NOTE: This requires Chocolatey to be installed
echo If you don't have it, use install_poppler_auto.bat instead
echo.
pause

choco install poppler -y

echo.
echo ====================================
echo Installation Complete!
echo ====================================
echo.
echo IMPORTANT: Restart your terminal and verify with: pdfinfo -v
echo.
pause

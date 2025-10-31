@echo off
echo ===================================
echo Installing Missing Dependencies
echo ===================================
echo.

echo Installing addict...
pip install addict==2.4.0

echo.
echo Installing timm...
pip install timm==0.9.12

echo.
echo Installing einops...
pip install einops==0.7.0

echo.
echo ===================================
echo Installation Complete!
echo ===================================
echo.
echo Press any key to close...
pause > nul

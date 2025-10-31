@echo off
echo ===================================
echo UNINSTALLING SPECIFIC PACKAGES
echo ===================================
echo.

echo Uninstalling addict...
pip uninstall -y addict

echo.
echo Uninstalling timm...
pip uninstall -y timm

echo.
echo Uninstalling einops...
pip uninstall -y einops

echo.
echo ===================================
echo UNINSTALLATION COMPLETE!
echo ===================================
echo.
echo Press any key to close...
pause > nul

@echo off
echo ========================================
echo Fixing huggingface_hub Version Issue
echo ========================================
echo.

echo This will fix the ImportError for cached_download
echo.

echo Step 1: Uninstalling incompatible huggingface-hub...
pip uninstall huggingface-hub -y

echo.
echo Step 2: Installing compatible version...
pip install huggingface-hub==0.16.4

echo.
echo Step 3: Reinstalling sentence-transformers...
pip install --upgrade --force-reinstall sentence-transformers==2.2.2

echo.
echo ========================================
echo Fix Complete!
echo ========================================
echo.
echo Now you can run: python app.py
echo.
pause

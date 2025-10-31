@echo off
echo ============================================================
echo FIXING ANSWER EVALUATION SYSTEM DEPENDENCIES
echo ============================================================
echo.

echo Step 1: Uninstalling problematic packages...
pip uninstall -y pyzstd transformers accelerate

echo.
echo Step 2: Reinstalling PyTorch with CUDA 12.1 support...
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121

echo.
echo Step 3: Installing transformers and accelerate...
pip install transformers==4.46.3
pip install accelerate==1.2.1

echo.
echo Step 4: Installing pyzstd correctly...
pip install --upgrade pyzstd

echo.
echo Step 5: Installing missing packages...
pip install pytesseract==0.3.10
pip install reportlab==4.0.7

echo.
echo ============================================================
echo SETUP FIXED! Now testing...
echo ============================================================
echo.

python test_setup.py

pause

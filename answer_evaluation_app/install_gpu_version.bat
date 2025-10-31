@echo off
echo ========================================
echo Installing GPU-Optimized Packages
echo CUDA 12.1 Version
echo ========================================
echo.

echo This will install all packages optimized for your GPU
echo Estimated time: 5-10 minutes
echo.
pause

echo Step 1: Installing Flask and web dependencies...
pip install Flask==3.0.0 PyPDF2==3.0.1 Pillow==10.1.0 pytesseract==0.3.10 pdf2image==1.16.3 reportlab==4.0.7 werkzeug==3.0.1

echo.
echo Step 2: Installing ML dependencies...
pip install chromadb==0.4.18 scikit-learn==1.3.2 numpy==1.26.2

echo.
echo Step 3: Installing sentence-transformers and huggingface-hub...
pip install sentence-transformers==2.7.0 huggingface-hub==0.24.0

echo.
echo Step 4: Installing PyTorch with CUDA 12.1 support...
pip install torch==2.5.1+cu121 torchvision==0.20.1+cu121 torchaudio==2.5.1+cu121 --extra-index-url https://download.pytorch.org/whl/cu121

echo.
echo Step 5: Installing transformers and accelerate...
pip install transformers==4.45.0 accelerate==0.34.0

echo.
echo Step 6: Installing DeepSeek-OCR dependencies...
pip install addict==2.4.0 timm==0.9.12 einops==0.7.0

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Testing GPU availability...
python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'CUDA Version: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}'); print(f'GPU Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"

echo.
echo Now you can run: python app.py
echo.
pause

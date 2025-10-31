@echo off
echo ================================================================
echo                    SYSTEM VERIFICATION TOOL
echo ================================================================
echo.

echo [1/5] Checking Python Installation...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)
echo [SUCCESS] Python is installed
echo.

echo [2/5] Checking CUDA/GPU Availability...
python -c "import torch; print('[SUCCESS] PyTorch installed'); print('CUDA Available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No GPU detected')"
if %errorlevel% neq 0 (
    echo [WARNING] PyTorch not installed yet - will be installed with requirements.txt
)
echo.

echo [3/5] Checking Poppler Installation...
pdfinfo -v >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Poppler not found in PATH
    echo Please run: fix_poppler.bat
) else (
    echo [SUCCESS] Poppler is installed
    pdfinfo -v
)
echo.

echo [4/5] Checking Required Directories...
if not exist "uploads" (
    echo Creating uploads directory...
    mkdir uploads
)
if not exist "results" (
    echo Creating results directory...
    mkdir results
)
if not exist "vector_db" (
    echo Creating vector_db directory...
    mkdir vector_db
)
echo [SUCCESS] All directories exist
echo.

echo [5/5] Checking Python Dependencies...
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Flask not installed
    echo Run: pip install -r requirements.txt
) else (
    echo [SUCCESS] Flask is installed
)

python -c "import PyPDF2" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] PyPDF2 not installed
) else (
    echo [SUCCESS] PyPDF2 is installed
)

python -c "import pdf2image" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] pdf2image not installed
) else (
    echo [SUCCESS] pdf2image is installed
)
echo.

echo ================================================================
echo                    VERIFICATION COMPLETE
echo ================================================================
echo.
echo Next Steps:
echo 1. If Poppler is missing: run fix_poppler.bat
echo 2. If dependencies are missing: run pip install -r requirements.txt
echo 3. To start the application: run python app.py
echo.
pause

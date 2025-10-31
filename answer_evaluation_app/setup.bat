@echo off
echo ========================================
echo   Setup - AI Answer Evaluation System
echo ========================================
echo.

echo [1/6] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.9 or higher.
    pause
    exit /b 1
)

echo.
echo [2/6] Creating virtual environment...
if exist "venv\" (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    echo Virtual environment created successfully!
)

echo.
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [4/6] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [5/6] Installing PyTorch with CUDA support...
echo This may take several minutes...
pip install torch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 --index-url https://download.pytorch.org/whl/cu118

echo.
echo [6/6] Installing other dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Testing GPU availability...
python -c "import torch; print('CUDA Available:', torch.cuda.is_available())"
echo.

if %errorlevel% equ 0 (
    echo [SUCCESS] Installation completed successfully!
    echo.
    echo Next steps:
    echo 1. Run start.bat to start the application
    echo 2. Open http://localhost:5000 in your browser
    echo 3. Upload question paper, answer key, and student papers
    echo.
    echo For detailed instructions, see INSTALLATION.md
) else (
    echo [WARNING] Some issues detected. Check the output above.
)

echo.
pause

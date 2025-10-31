@echo off
echo ============================================================
echo   Starting Ollama LLM Answer Evaluation System
echo ============================================================
echo.

REM Check if Ollama is running
echo Checking Ollama installation...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Ollama is not installed!
    echo Please install from: https://ollama.ai
    echo.
    pause
    exit /b 1
)

echo [OK] Ollama is installed
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if model is available
echo Checking if llama3.2 model is available...
ollama list | findstr /i "llama3.2" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo WARNING: llama3.2 model not found!
    echo Would you like to download it now? (This may take a few minutes)
    set /p download="Download llama3.2? (y/n): "
    if /i "%download%"=="y" (
        echo Downloading llama3.2...
        ollama pull llama3.2
    ) else (
        echo Please run: ollama pull llama3.2
        pause
        exit /b 1
    )
)

echo [OK] llama3.2 model is available
echo.

REM Start the application
echo ============================================================
echo   Starting Flask Application
echo ============================================================
echo.
echo Server will start at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
echo ============================================================
echo.

python app_ollama.py

pause

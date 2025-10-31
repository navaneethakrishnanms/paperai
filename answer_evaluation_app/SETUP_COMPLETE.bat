@echo off
echo ================================================================
echo   AI-Powered Answer Evaluation System - Complete Setup
echo ================================================================
echo.

echo [1/5] Checking Python...
python --version
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)
echo [OK] Python is installed
echo.

echo [2/5] Checking Ollama...
ollama --version
if errorlevel 1 (
    echo [ERROR] Ollama is not installed!
    echo.
    echo Please install Ollama:
    echo 1. Go to https://ollama.ai
    echo 2. Download and install for Windows
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)
echo [OK] Ollama is installed
echo.

echo [3/5] Checking Ollama model...
ollama list | findstr "llama3.1" >nul
if errorlevel 1 (
    echo [INFO] llama3.1 model not found. Pulling now...
    echo This may take 5-10 minutes (4.7GB download)
    echo.
    ollama pull llama3.1:latest
    if errorlevel 1 (
        echo [ERROR] Failed to pull model
        pause
        exit /b 1
    )
    echo [OK] Model downloaded successfully
) else (
    echo [OK] llama3.1 model is available
)
echo.

echo [4/5] Installing Python dependencies...
echo This may take 3-5 minutes...
echo.
pip install -r requirements_complete.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    echo.
    echo Try manually:
    echo pip install -r requirements_complete.txt
    echo.
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

echo [5/5] Running system tests...
echo.
python test_complete_system_new.py
if errorlevel 1 (
    echo.
    echo [WARNING] Some tests failed
    echo The system may still work, but check the errors above
    echo.
) else (
    echo.
    echo [OK] All tests passed!
)

echo.
echo ================================================================
echo   Setup Complete!
echo ================================================================
echo.
echo Your AI-powered answer evaluation system is ready!
echo.
echo Next steps:
echo   1. Run: start_complete_system.bat
echo   2. Open browser: http://localhost:5000
echo   3. Upload question paper, answer key, and student paper
echo   4. Get AI-powered evaluation results!
echo.
echo Documentation:
echo   - Quick Start: START_HERE.md
echo   - Full Guide: COMPLETE_SYSTEM_GUIDE.md
echo   - Checklist: QUICKSTART_CHECKLIST.md
echo.
echo ================================================================
pause

@echo off
echo ========================================
echo AI-Powered Answer Evaluation System
echo OCR + Text PDF + Ollama Integration
echo ========================================
echo.

echo Checking Ollama...
ollama list
if errorlevel 1 (
    echo.
    echo [ERROR] Ollama is not installed!
    echo Please install Ollama from: https://ollama.ai
    echo.
    pause
    exit /b 1
)

echo.
echo Checking if llama3.1 model is available...
ollama list | findstr "llama3.1" >nul
if errorlevel 1 (
    echo.
    echo [INFO] llama3.1 model not found. Pulling model...
    echo This may take several minutes...
    ollama pull llama3.1:latest
)

echo.
echo Starting Flask application...
echo.
python app_ollama_complete.py

pause

@echo off
echo.
echo ================================================================
echo  AI-Powered Answer Evaluation System with Ollama LLM
echo ================================================================
echo.
echo Features:
echo   - DeepSeek-OCR for handwritten text extraction
echo   - Ollama LLM for concept-based evaluation
echo   - Automated question and answer key processing
echo   - Detailed PDF reports with feedback
echo.
echo ================================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Check if Ollama is installed
echo.
echo Checking Ollama installation...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Ollama is not installed!
    echo.
    echo Please install Ollama from: https://ollama.ai
    echo.
    echo After installation, run: ollama pull llama3.1:latest
    echo.
    pause
    exit /b 1
)

echo Ollama is installed ✓
echo.

REM Check if model is available
echo Checking for Ollama models...
ollama list | findstr "llama3.1" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Warning: llama3.1 model not found
    echo Pulling llama3.1 model (this may take a few minutes)...
    ollama pull llama3.1:latest
    echo.
)

echo Model ready ✓
echo.

REM Start the application
echo Starting Answer Evaluation System...
echo.
echo Access the application at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
python app_ollama_integrated.py

pause

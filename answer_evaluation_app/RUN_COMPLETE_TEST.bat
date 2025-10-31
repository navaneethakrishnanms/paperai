@echo off
echo ================================================================
echo   Testing Complete Handwritten Answer Evaluation Pipeline
echo ================================================================
echo.
echo This will test:
echo   1. Handwritten PDF to Text PDF conversion (DeepSeek-OCR)
echo   2. Question and Answer extraction
echo   3. Concept-based evaluation (Ollama LLM)
echo   4. Result PDF generation
echo.
echo ================================================================
echo.
pause

python test_handwritten_evaluation.py

echo.
echo ================================================================
echo   Test Complete!
echo ================================================================
pause

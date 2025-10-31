@echo off
echo ====================================================
echo Diagnostic Tool for Answer Evaluation App
echo ====================================================
echo.

cd /d %~dp0

echo Step 1: Checking ChromaDB contents...
echo ====================================================
python debug_db.py
echo.
echo.

echo Step 2: Testing PDF extraction...
echo ====================================================
python test_extraction.py
echo.
echo.

echo ====================================================
echo Diagnostic complete!
echo ====================================================
echo.
echo If you see "0 questions" or "0 answers", the PDFs 
echo are either:
echo   1. Not in the expected format
echo   2. Text cannot be extracted
echo   3. Regular expression patterns don't match
echo.
echo Check the output above to identify the issue.
echo.
pause

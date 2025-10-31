@echo off
cls
echo.
echo ========================================
echo    FAST EXTRACTION - READY TO TEST!
echo ========================================
echo.
echo Your document format: "1. Answer text"
echo Expected result: 3 answers extracted
echo Processing time: ^<1 second
echo.
echo ========================================
echo.
pause
echo.
echo Running test...
echo.

python test_student_extraction.py

echo.
echo ========================================
echo.
echo If you see "3 answers extracted" above,
echo your system is ready!
echo.
echo Next step: Run start.bat to launch app
echo.
pause

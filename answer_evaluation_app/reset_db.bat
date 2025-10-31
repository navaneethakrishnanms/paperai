@echo off
echo ====================================
echo Quick Fix for Database Issues
echo ====================================
echo.

echo Backing up and clearing vector database...
if exist "vector_db\chroma.sqlite3" (
    echo Found existing database, backing up...
    copy "vector_db\chroma.sqlite3" "vector_db\chroma.sqlite3.backup" >nul 2>&1
    del "vector_db\chroma.sqlite3" >nul 2>&1
    echo Database backed up and cleared!
)

echo.
echo Clearing Python cache...
if exist "__pycache__" (
    rmdir /s /q "__pycache__" >nul 2>&1
)

echo.
echo Database reset complete!
echo.
echo Now run: python app.py
echo.

pause

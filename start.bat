@echo off
echo ========================================
echo   Project Samarth - Starting Server
echo ========================================
echo.
echo Checking dependencies...

pip install -r requirements.txt --quiet

echo.
echo Starting Flask server...
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

pause


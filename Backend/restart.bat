@echo off
echo ================================================
echo Student Attendance System - Restart Script
echo ================================================
echo.

echo Stopping any running Flask processes...
taskkill /f /im python.exe 2>nul

echo.
echo Starting Flask application...
python app.py

pause
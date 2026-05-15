@echo off
echo ================================================
echo Student Attendance System - Installation Script
echo ================================================
echo.

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Installation completed!
echo.
echo To run the application:
echo   python app.py
echo   OR
echo   python run.py
echo.
echo Then open your browser and go to: http://localhost:5000
echo.
echo Default Admin Login:
echo   Email: admin@school.com
echo   Password: admin123
echo.
pause
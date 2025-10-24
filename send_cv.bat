@echo off
title Email Automation Script
echo.
echo ========================================
echo    Email Automation Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "send_cv.py" (
    echo ERROR: send_cv.py not found
    pause
    exit /b 1
)

if not exist "config.txt" (
    echo ERROR: config.txt not found
    echo Please create config.txt with your email settings
    pause
    exit /b 1
)

if not exist "recipients.csv" (
    echo ERROR: recipients.csv not found
    echo Please create recipients.csv with your target emails
    pause
    exit /b 1
)

echo Starting email automation...
echo.
echo Press Ctrl+C to stop the script at any time
echo.

REM Run the Python script
python send_cv.py

echo.
echo Script finished. Check email_log.txt for details.
pause

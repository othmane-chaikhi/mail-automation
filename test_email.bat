@echo off
title Email Configuration Test
echo.
echo ========================================
echo    Email Configuration Test
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

echo Testing your email configuration...
echo.

REM Run the test script
python test_email.py

echo.
pause

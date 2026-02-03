@echo off
REM Startup script for Content Search and Publishing System (Windows)

echo ===================================
echo Content Search System - energo-audit.by
echo ===================================
echo.

REM Check if .env exists
if not exist .env (
    echo Error: .env file not found!
    echo Please copy .env.example to .env and configure your API keys.
    echo.
    echo Run: copy .env.example .env
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Create necessary directories
echo Creating directories...
if not exist data mkdir data
if not exist logs mkdir logs

REM Get mode from command line or use default
set MODE=%1
if "%MODE%"=="" set MODE=scheduler

echo.
echo Starting in mode: %MODE%
echo.

REM Run the application
python main.py --mode %MODE%

REM Deactivate virtual environment on exit
call deactivate

pause

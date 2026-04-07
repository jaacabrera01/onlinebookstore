@echo off
REM Setup script for BookCart Automation Testing Framework on Windows

setlocal enabledelayedexpansion

echo ==========================================
echo BookCart Test Automation Framework Setup
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Checking Python version...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python version: %PYTHON_VERSION%
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv\" (
    echo Setting up virtual environment...
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed
echo.

REM Install Playwright
echo Installing Playwright browsers...
echo This may take a few minutes...
playwright install
if errorlevel 1 (
    echo ERROR: Failed to install Playwright
    pause
    exit /b 1
)
echo Playwright installed
echo.

REM Install Playwright system dependencies
echo Installing Playwright system dependencies...
python -m playwright install-deps
echo.

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo .env file created from .env.example
    echo Please update .env with your configuration
) else (
    echo .env file already exists
)
echo.

REM Create necessary directories
echo Creating directories...
if not exist "test-results\screenshots" mkdir test-results\screenshots
if not exist "logs" mkdir logs
if not exist "allure-results" mkdir allure-results
echo Directories created
echo.

REM Run smoke tests to verify setup
echo Running smoke tests to verify setup...
echo.
call pytest -m smoke -v --tb=short
if errorlevel 1 (
    echo.
    echo ==========================================
    echo Setup completed but smoke tests failed
    echo ==========================================
    echo.
    echo This might be expected if the application is down.
    echo You can still run tests manually with:
    echo   pytest tests/ -v
    echo.
) else (
    echo.
    echo ==========================================
    echo Setup completed successfully!
    echo ==========================================
    echo.
    echo Next steps:
    echo 1. Run all tests:        pytest tests/ -v
    echo 2. Run smoke tests:      pytest -m smoke -v
    echo 3. Run critical tests:   pytest -m critical -v
    echo 4. View test report:     pytest tests/ --alluredir=allure-results ^&^& allure serve allure-results
    echo.
    echo See README.md for more information
)

pause

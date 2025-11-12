@echo off
REM EcoSnake Game - One-Click Launcher (Windows)

cls
echo =========================================
echo   EcoSnake Game Launcher
echo =========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Python not found!
        echo.
        echo Please install Python: https://python.org
        pause
        exit /b 1
    )
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)

echo [OK] Python found!
%PYTHON_CMD% --version
echo.

REM Check if virtual environment exists
if not exist .venv (
    echo [SETUP] First time setup...
    echo.
    
    REM Create virtual environment
    echo [*] Creating virtual environment...
    %PYTHON_CMD% -m venv .venv
    
    REM Activate
    call .venv\Scripts\activate.bat
    
    REM Install Pygame
    echo [*] Installing Pygame...
    python -m pip install --quiet --upgrade pip
    python -m pip install --quiet pygame
    
    if %errorlevel% equ 0 (
        echo [OK] Setup completed!
        echo.
    ) else (
        echo [ERROR] Setup failed!
        pause
        exit /b 1
    )
) else (
    REM Activate virtual environment
    call .venv\Scripts\activate.bat
)

REM Start the game
echo =========================================
echo   Starting game...
echo =========================================
echo.

python EcoSnake.py

REM Keep window open if error occurs
if %errorlevel% neq 0 (
    echo.
    echo An error occurred!
    pause
)

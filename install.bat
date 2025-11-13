@echo off
echo ========================================
echo   Lean Six Sigma - Windows Installer
echo ========================================
echo.

echo [1/3] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo.

echo [2/3] Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo.

echo [3/3] Installation complete!
echo.
echo ========================================
echo   Ready to run!
echo ========================================
echo.
echo To start the app, run: run.bat
echo Or type: streamlit run app.py
echo.
pause

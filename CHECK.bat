@echo off
echo ========================================
echo   System Check - Lean Six Sigma App
echo ========================================
echo.

echo [1] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not installed!
    echo Download from: https://www.python.org/downloads/
    echo.
    goto :error
) else (
    echo OK: Python found
)
echo.

echo [2] Checking pip...
python -m pip --version
if errorlevel 1 (
    echo ERROR: pip not found!
    goto :error
) else (
    echo OK: pip found
)
echo.

echo [3] Checking current directory...
echo Current directory: %CD%
if exist requirements.txt (
    echo OK: requirements.txt found
) else (
    echo ERROR: requirements.txt NOT found!
    echo Make sure you are in the lean_six_sigma_app folder
    goto :error
)
echo.

echo [4] Checking app files...
if exist app.py (
    echo OK: app.py found
) else (
    echo ERROR: app.py NOT found!
    goto :error
)
echo.

echo [5] Listing all files...
dir /b
echo.

echo ========================================
echo   All checks PASSED!
echo ========================================
echo.
echo Next steps:
echo   1. Run: install.bat  (to install dependencies)
echo   2. Run: run.bat      (to start the app)
echo.
pause
exit /b 0

:error
echo.
echo ========================================
echo   ERROR: Some checks FAILED!
echo ========================================
echo.
echo Please fix the errors above and try again.
echo.
pause
exit /b 1

@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   CAI DAT HOAN CHINH - LEAN SIX SIGMA
echo ========================================
echo.

REM Kiem tra Python
echo [Step 1/12] Kiem tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python khong duoc cai dat!
    echo Tai tai: https://www.python.org/downloads/
    echo Nho tick "Add Python to PATH"!
    pause
    exit /b 1
)
python --version
echo.

REM Upgrade pip
echo [Step 2/12] Nang cap pip...
python -m pip install --upgrade pip
echo.

REM Upgrade setuptools va wheel
echo [Step 3/12] Nang cap setuptools va wheel...
python -m pip install --upgrade setuptools wheel
echo.

REM Cai streamlit
echo [Step 4/12] Cai dat Streamlit...
python -m pip install streamlit
if errorlevel 1 (
    echo WARNING: Co loi khi cai Streamlit
    echo Thu cai lai...
    python -m pip install --no-cache-dir streamlit
)
echo.

REM Cai pandas
echo [Step 5/12] Cai dat Pandas...
python -m pip install pandas
echo.

REM Cai plotly
echo [Step 6/12] Cai dat Plotly...
python -m pip install plotly
echo.

REM Cai python-docx
echo [Step 7/12] Cai dat python-docx...
python -m pip install python-docx
echo.

REM Cai openpyxl
echo [Step 8/12] Cai dat openpyxl...
python -m pip install openpyxl
echo.

REM Cai reportlab
echo [Step 9/12] Cai dat ReportLab...
python -m pip install reportlab
echo.

REM Cai matplotlib
echo [Step 10/12] Cai dat Matplotlib...
python -m pip install matplotlib
echo.

REM Cai numpy
echo [Step 11/12] Cai dat NumPy...
python -m pip install numpy
echo.

REM Cai cac thu vien bo sung
echo [Step 12/12] Cai dat cac thu vien bo sung...
python -m pip install python-dateutil xlsxwriter
echo.

REM Kiem tra lai
echo ========================================
echo   KIEM TRA CAI DAT
echo ========================================
echo.

set ERROR_COUNT=0

echo Kiem tra Streamlit...
python -c "import streamlit; print('OK - Version:', streamlit.__version__)" 2>nul
if errorlevel 1 (
    echo FAILED
    set /a ERROR_COUNT+=1
) else (
    echo PASS
)

echo Kiem tra Pandas...
python -c "import pandas; print('OK')" 2>nul
if errorlevel 1 (
    echo FAILED
    set /a ERROR_COUNT+=1
) else (
    echo PASS
)

echo Kiem tra Plotly...
python -c "import plotly; print('OK')" 2>nul
if errorlevel 1 (
    echo FAILED
    set /a ERROR_COUNT+=1
) else (
    echo PASS
)

echo Kiem tra python-docx...
python -c "import docx; print('OK')" 2>nul
if errorlevel 1 (
    echo FAILED
    set /a ERROR_COUNT+=1
) else (
    echo PASS
)

echo Kiem tra ReportLab...
python -c "import reportlab; print('OK')" 2>nul
if errorlevel 1 (
    echo FAILED
    set /a ERROR_COUNT+=1
) else (
    echo PASS
)

echo.

if !ERROR_COUNT! gtr 0 (
    echo ========================================
    echo   CO !ERROR_COUNT! THU VIEN BI LOI!
    echo ========================================
    echo.
    echo Hay thu cai lai bang tay:
    echo   python -m pip install --force-reinstall streamlit pandas plotly
    echo.
    pause
    exit /b 1
) else (
    echo ========================================
    echo   CAI DAT THANH CONG 100%%!
    echo ========================================
    echo.
    echo Tat ca thu vien da duoc cai dat!
    echo.
    echo De chay ung dung:
    echo   run.bat
    echo.
    echo Hoac:
    echo   streamlit run app.py
    echo.
    pause
    exit /b 0
)

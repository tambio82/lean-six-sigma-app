@echo off
echo ================================================
echo   CHUONG TRINH CAI DAT THU VIEN
echo   Lean Six Sigma App
echo ================================================
echo.

echo [1/11] Upgrade pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: Khong the upgrade pip!
    echo Thu voi: py -m pip install --upgrade pip
    pause
    exit /b 1
)
echo OK: pip upgraded
echo.

echo [2/11] Installing streamlit...
python -m pip install streamlit
if errorlevel 1 echo WARNING: streamlit co van de
echo.

echo [3/11] Installing pandas...
python -m pip install pandas
if errorlevel 1 echo WARNING: pandas co van de
echo.

echo [4/11] Installing plotly...
python -m pip install plotly
if errorlevel 1 (
    echo ERROR: Khong the cai plotly!
    pause
    exit /b 1
)
echo OK: plotly installed
echo.

echo [5/11] Installing python-docx...
python -m pip install python-docx
if errorlevel 1 echo WARNING: python-docx co van de
echo.

echo [6/11] Installing openpyxl...
python -m pip install openpyxl
if errorlevel 1 echo WARNING: openpyxl co van de
echo.

echo [7/11] Installing reportlab...
python -m pip install reportlab
if errorlevel 1 echo WARNING: reportlab co van de
echo.

echo [8/11] Installing Pillow...
python -m pip install Pillow
if errorlevel 1 echo WARNING: Pillow co van de
echo.

echo [9/11] Installing matplotlib...
python -m pip install matplotlib
if errorlevel 1 echo WARNING: matplotlib co van de
echo.

echo [10/11] Installing numpy...
python -m pip install numpy
if errorlevel 1 echo WARNING: numpy co van de
echo.

echo [11/11] Checking plotly...
python -c "import plotly; print('Plotly OK!')"
if errorlevel 1 (
    echo ERROR: Plotly van chua cai duoc!
    echo.
    echo Thu cai lai bang tay:
    echo python -m pip install plotly --force-reinstall
    pause
    exit /b 1
)
echo.

echo ================================================
echo   CAI DAT THANH CONG!
echo ================================================
echo.
echo Tat ca thu vien da duoc cai dat.
echo.
echo De chay ung dung, go:
echo   streamlit run app.py
echo.
echo Hoac chay file: run.bat
echo.
pause

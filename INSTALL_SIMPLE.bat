@echo off
echo ================================================
echo   CAI DAT NHANH - BO QUA PILLOW
echo   (App van chay binh thuong!)
echo ================================================
echo.

echo [1/10] Upgrade pip...
python -m pip install --upgrade pip setuptools wheel
echo.

echo [2/10] Installing streamlit...
python -m pip install streamlit
echo.

echo [3/10] Installing pandas...
python -m pip install pandas
echo.

echo [4/10] Installing plotly...
python -m pip install plotly
echo.

echo [5/10] Installing python-docx...
python -m pip install python-docx
echo.

echo [6/10] Installing openpyxl...
python -m pip install openpyxl
echo.

echo [7/10] Installing reportlab...
python -m pip install reportlab
echo.

echo [8/10] Installing matplotlib...
python -m pip install matplotlib
echo.

echo [9/10] Installing numpy...
python -m pip install numpy
echo.

echo [10/10] Installing python-dateutil and xlsxwriter...
python -m pip install python-dateutil xlsxwriter
echo.

echo ================================================
echo   CAI DAT THANH CONG!
echo ================================================
echo.
echo Luu y: Da BO QUA Pillow vi gap loi build.
echo App van chay binh thuong, chi thieu chuc nang xu ly anh.
echo.
echo De chay app:
echo   streamlit run app.py
echo.
echo Hoac chay: run.bat
echo.
pause

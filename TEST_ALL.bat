@echo off
echo ========================================
echo   KIEM TRA TOAN DIEN HE THONG
echo ========================================
echo.

echo [1/10] Kiem tra Python...
python --version
if errorlevel 1 (
    echo ERROR: Python khong co!
    goto :error
)
echo OK
echo.

echo [2/10] Kiem tra pip...
python -m pip --version
if errorlevel 1 (
    echo ERROR: pip khong co!
    goto :error
)
echo OK
echo.

echo [3/10] Kiem tra thu muc...
dir app.py >nul 2>&1
if errorlevel 1 (
    echo ERROR: Khong tim thay app.py!
    echo Ban dang o sai thu muc!
    goto :error
)
echo OK - Dang o dung thu muc
echo.

echo [4/10] Kiem tra streamlit...
python -c "import streamlit; print('Streamlit version:', streamlit.__version__)" 2>nul
if errorlevel 1 (
    echo WARNING: Streamlit chua cai!
    echo Dang cai dat...
    python -m pip install streamlit
)
echo.

echo [5/10] Kiem tra pandas...
python -c "import pandas; print('Pandas OK')" 2>nul
if errorlevel 1 (
    echo WARNING: Pandas chua cai!
    python -m pip install pandas
)
echo.

echo [6/10] Kiem tra plotly...
python -c "import plotly; print('Plotly OK')" 2>nul
if errorlevel 1 (
    echo WARNING: Plotly chua cai!
    python -m pip install plotly
)
echo.

echo [7/10] Kiem tra python-docx...
python -c "import docx; print('python-docx OK')" 2>nul
if errorlevel 1 (
    echo WARNING: python-docx chua cai!
    python -m pip install python-docx
)
echo.

echo [8/10] Kiem tra reportlab...
python -c "import reportlab; print('ReportLab OK')" 2>nul
if errorlevel 1 (
    echo WARNING: reportlab chua cai!
    python -m pip install reportlab
)
echo.

echo [9/10] Kiem tra cac module...
python -c "from database import ProjectDatabase; from gantt_chart import create_gantt_chart; from dashboard import create_status_chart; from export_pdf import create_project_pdf; print('Tat ca modules OK!')" 2>nul
if errorlevel 1 (
    echo ERROR: Co loi import modules!
    echo Hay kiem tra lai cac file .py
    goto :error
)
echo OK
echo.

echo [10/10] Kiem tra database...
python -c "from database import ProjectDatabase; db = ProjectDatabase(); projects = db.get_all_projects(); print(f'Database OK - Co {len(projects)} du an')" 2>nul
if errorlevel 1 (
    echo WARNING: Database co van de hoac chua khoi tao
    echo Se tu dong khoi tao khi chay app
)
echo.

echo ========================================
echo   TAT CA KIEM TRA HOAN TAT!
echo ========================================
echo.
echo He thong san sang chay!
echo.
echo De chay ung dung:
echo   run.bat
echo.
echo Hoac:
echo   streamlit run app.py
echo.
pause
exit /b 0

:error
echo.
echo ========================================
echo   CO LOI XAY RA!
echo ========================================
echo.
echo Hay sua cac loi tren roi chay lai.
echo.
pause
exit /b 1

@echo off
echo ========================================
echo   RESET DATABASE
echo ========================================
echo.
echo CANH BAO: Script nay se XOA database hien tai
echo va tao lai database moi voi du lieu mau.
echo.
echo Nhan ENTER de tiep tuc, hoac dong cua so nay de huy.
pause
echo.

echo [1/3] Xoa database cu...
if exist lean_projects.db (
    del lean_projects.db
    echo OK - Da xoa database cu
) else (
    echo Database chua ton tai
)
echo.

echo [2/3] Tao database moi...
python -c "from database import ProjectDatabase; db = ProjectDatabase(); print('Database moi da duoc tao!')"
if errorlevel 1 (
    echo ERROR: Khong the tao database!
    pause
    exit /b 1
)
echo.

echo [3/3] Them du lieu mau...
python create_sample_data.py
if errorlevel 1 (
    echo WARNING: Khong the them du lieu mau
    echo Nhung database da duoc tao!
)
echo.

echo ========================================
echo   HOAN TAT!
echo ========================================
echo.
echo Database da duoc reset thanh cong!
echo.
echo De chay ung dung:
echo   run.bat
echo.
pause

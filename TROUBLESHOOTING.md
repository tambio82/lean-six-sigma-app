# 🆘 XỬ LÝ LỖI - TROUBLESHOOTING GUIDE

## 📋 MỤC LỤC LỖI THƯỜNG GẶP

1. [Lỗi Python không tìm thấy](#loi-1-python-not-found)
2. [Lỗi No module named 'streamlit'](#loi-2-no-module-named-streamlit)
3. [Lỗi use_column_width](#loi-3-use_column_width)
4. [Lỗi Pillow không cài được](#loi-4-pillow-build-error)
5. [Lỗi xuất PDF](#loi-5-pdf-export-error)
6. [Lỗi Address already in use](#loi-6-address-in-use)
7. [Lỗi Database](#loi-7-database-error)
8. [App không mở tự động](#loi-8-browser-not-opening)

---

## LỖI 1: Python Not Found

### Triệu chứng:
```
'python' is not recognized as an internal or external command
```

### Giải pháp:

**Cách 1**: Cài lại Python
1. Tải Python từ: https://www.python.org/downloads/
2. Chạy installer
3. **QUAN TRỌNG**: Tick vào "Add Python to PATH"
4. Cài đặt
5. Khởi động lại Command Prompt

**Cách 2**: Thêm Python vào PATH thủ công
1. Tìm thư mục Python (VD: `C:\Python313\`)
2. Windows Search → "Environment Variables"
3. Edit "Path"
4. Add đường dẫn Python
5. Khởi động lại CMD

**Cách 3**: Dùng `py` launcher
```cmd
py --version
py -m pip install streamlit
py -m streamlit run app.py
```

---

## LỖI 2: No module named 'streamlit'

### Triệu chứng:
```
ModuleNotFoundError: No module named 'streamlit'
```

### Giải pháp:

**Đơn giản nhất**:
```cmd
INSTALL_COMPLETE.bat
```

**Hoặc thủ công**:
```cmd
python -m pip install streamlit pandas plotly python-docx openpyxl reportlab matplotlib numpy
```

**Nếu vẫn lỗi**:
```cmd
python -m pip install --force-reinstall streamlit
```

**Kiểm tra**:
```cmd
python -c "import streamlit; print(streamlit.__version__)"
```

---

## LỖI 3: use_column_width

### Triệu chứng:
```
TypeError: got an unexpected keyword argument 'use_column_width'
Did you mean 'use_container_width'?
```

### Giải pháp:

Tải file `app.py` đã sửa:
[app_FIXED.py](computer:///mnt/user-data/outputs/app_FIXED.py)

Thay thế file cũ và chạy lại.

**ĐÃ SỬA**: Tất cả `use_column_width` → `use_container_width`

---

## LỖI 4: Pillow Build Error

### Triệu chứng:
```
ERROR: Failed to build 'Pillow' when getting requirements to build wheel
```

### Giải pháp:

**Bỏ qua Pillow** (App vẫn chạy 99% chức năng):
```cmd
python -m pip install streamlit pandas plotly python-docx openpyxl reportlab matplotlib numpy
```

**Nếu muốn cài Pillow**:

**Thử 1**:
```cmd
python -m pip install --upgrade pip setuptools wheel
python -m pip install Pillow --only-binary :all:
```

**Thử 2**:
```cmd
python -m pip install Pillow==9.5.0
```

**Thử 3**: Cài Microsoft Visual C++ Build Tools
- Tải: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Cài đặt
- Chạy lại: `python -m pip install Pillow`

---

## LỖI 5: PDF Export Error

### Triệu chứng:
```
[Errno 2] No such file or directory: '/home/claude/project_XXX.pdf'
```

### Giải pháp:

Tải file `app.py` mới đã sửa:
[app_FIXED.py](computer:///mnt/user-data/outputs/app_FIXED.py)

**ĐÃ SỬA**: Dùng `tempfile` thay vì đường dẫn cố định

---

## LỖI 6: Address Already in Use

### Triệu chứng:
```
OSError: [Errno 98] Address already in use
```

### Nguyên nhân:
Port 8501 đang được dùng bởi instance khác

### Giải pháp:

**Cách 1**: Dừng process cũ
- Windows: Task Manager → Tìm Python → End Task
- CMD: `Ctrl + C` trong cửa sổ đang chạy Streamlit

**Cách 2**: Dùng port khác
```cmd
streamlit run app.py --server.port 8502
```

Sau đó mở: http://localhost:8502

**Cách 3**: Kill port 8501
```cmd
netstat -ano | findstr :8501
taskkill /PID [PID_NUMBER] /F
```

---

## LỖI 7: Database Error

### Triệu chứng:
```
sqlite3.OperationalError: database is locked
```

### Giải pháp:

**Cách 1**: Đóng tất cả instances của app
```cmd
taskkill /IM python.exe /F
```

**Cách 2**: Reset database
```cmd
RESET_DATABASE.bat
```

**Cách 3**: Xóa database lock
```cmd
del lean_projects.db-journal
```

### Triệu chứng 2:
```
No such table: projects
```

### Giải pháp:
```cmd
RESET_DATABASE.bat
```

---

## LỖI 8: Browser Not Opening

### Triệu chứng:
App chạy nhưng browser không tự mở

### Giải pháp:

**Tự mở browser**:
1. Mở Chrome/Edge/Firefox
2. Gõ: `http://localhost:8501`
3. Enter

**Nếu vẫn không mở**:
```cmd
streamlit run app.py --server.headless false
```

---

## 🔧 CÔNG CỤ KIỂM TRA

### TEST_ALL.bat
Kiểm tra toàn bộ hệ thống:
```cmd
TEST_ALL.bat
```

Kiểm tra:
- ✅ Python installed
- ✅ pip hoạt động
- ✅ Đúng thư mục
- ✅ Tất cả thư viện
- ✅ Database OK
- ✅ Modules import được

### INSTALL_COMPLETE.bat
Cài đặt với error handling:
```cmd
INSTALL_COMPLETE.bat
```

### RESET_DATABASE.bat
Reset database về trạng thái ban đầu:
```cmd
RESET_DATABASE.bat
```

---

## 📞 QUY TRÌNH DEBUG CHUẨN

Khi gặp lỗi, làm theo thứ tự:

### Bước 1: Chạy TEST_ALL.bat
```cmd
TEST_ALL.bat
```

Xem báo cáo → Sửa những gì FAILED

### Bước 2: Kiểm tra Python
```cmd
python --version
```

Phải thấy: Python 3.8+

### Bước 3: Kiểm tra thư viện
```cmd
python -c "import streamlit, pandas, plotly; print('OK')"
```

Nếu lỗi → Chạy `INSTALL_COMPLETE.bat`

### Bước 4: Kiểm tra files
```cmd
dir app.py database.py
```

Phải thấy các file chính

### Bước 5: Kiểm tra database
```cmd
python -c "from database import ProjectDatabase; db = ProjectDatabase(); print('OK')"
```

Nếu lỗi → Chạy `RESET_DATABASE.bat`

### Bước 6: Test chạy app
```cmd
streamlit run app.py
```

### Bước 7: Nếu vẫn lỗi
Gửi cho tôi:
1. Screenshot lỗi
2. Kết quả `TEST_ALL.bat`
3. Version Python: `python --version`
4. Version Streamlit: `python -c "import streamlit; print(streamlit.__version__)"`

---

## 🎯 CHECKLIST HOÀN CHỈNH

Trước khi chạy app:

- ☑️ Python 3.8+ đã cài
- ☑️ Python trong PATH
- ☑️ pip hoạt động
- ☑️ Streamlit đã cài
- ☑️ Các thư viện đã cài đủ
- ☑️ Đang ở đúng thư mục
- ☑️ File app.py phiên bản mới nhất
- ☑️ Database tồn tại
- ☑️ Port 8501 chưa được dùng

**TẤT CẢ OK** → Chạy: `run.bat` hoặc `streamlit run app.py`

---

## 💡 MẸO NÂNG CAO

### Xóa cache Streamlit
```cmd
streamlit cache clear
```

### Upgrade tất cả packages
```cmd
python -m pip install --upgrade streamlit pandas plotly python-docx openpyxl reportlab matplotlib numpy
```

### Check process đang chạy
```cmd
netstat -ano | findstr :8501
```

### Chạy ở chế độ debug
```cmd
streamlit run app.py --logger.level=debug
```

### Xem log errors
```cmd
streamlit run app.py 2>&1 | tee error.log
```

---

## 📝 GHI CHÚ PHIÊN BẢN

### Version hiện tại:
- Python: 3.8+
- Streamlit: 1.31.0
- Pandas: 2.2.0
- Plotly: 5.18.0

### Đã sửa:
- ✅ use_column_width → use_container_width
- ✅ PDF export path (Linux → tempfile)
- ✅ Pillow optional
- ✅ Button parameters

---

## 🆘 LIÊN HỆ HỖ TRỢ

Nếu vẫn gặp vấn đề, gửi cho tôi:

1. **Screenshot lỗi**
2. **Kết quả lệnh**:
```cmd
python --version
python -m pip list
dir
TEST_ALL.bat
```

3. **Mô tả chi tiết**:
   - Bước nào bị lỗi
   - Đã thử những cách nào
   - Hệ điều hành (Windows version)

---

**CẬP NHẬT**: 2024-11-13  
**VERSION**: 1.0.0 (Hoàn chỉnh)

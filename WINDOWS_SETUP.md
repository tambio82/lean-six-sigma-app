# 🪟 HƯỚNG DẪN CÀI ĐẶT TRÊN WINDOWS

## ❗ LỖI THƯỜNG GẶP VÀ GIẢI PHÁP

### Lỗi: "Could not open requirements file"

**Nguyên nhân**: Bạn đang ở sai thư mục!

**Giải pháp**:

#### Cách 1: Sử dụng Windows Explorer
1. Mở Windows Explorer (phím Windows + E)
2. Tìm thư mục `lean_six_sigma_app` (nơi bạn giải nén)
3. Nhấn vào thanh địa chỉ ở trên cùng
4. Gõ `cmd` và nhấn Enter
5. Command Prompt sẽ mở ngay tại thư mục đó
6. Chạy: `CHECK.bat` để kiểm tra

#### Cách 2: Dùng lệnh cd
```cmd
REM Kiểm tra thư mục hiện tại
cd

REM Di chuyển đến thư mục đúng (thay đổi đường dẫn cho đúng)
cd C:\Users\Surface\Downloads\lean_six_sigma_app

REM Hoặc nếu ở Desktop
cd C:\Users\Surface\Desktop\lean_six_sigma_app

REM Liệt kê files để kiểm tra
dir

REM Phải thấy: requirements.txt, app.py, etc.
```

---

## 📋 HƯỚNG DẪN CÀI ĐẶT NHANH (WINDOWS)

### Bước 1: Kiểm tra Python đã cài chưa

Mở Command Prompt (cmd) và gõ:
```cmd
python --version
```

**Kết quả mong đợi**: `Python 3.8.x` hoặc cao hơn

**Nếu báo lỗi**: Cài Python từ https://www.python.org/downloads/
- ✅ **QUAN TRỌNG**: Tick vào "Add Python to PATH"

### Bước 2: Giải nén file

1. Tải file `lean_six_sigma_app.zip`
2. Click phải → Extract All
3. Chọn thư mục giải nén (VD: `C:\Users\Surface\Downloads\`)
4. Nhấn Extract

### Bước 3: Mở Command Prompt tại thư mục app

**CÁCH DỄ NHẤT:**
1. Mở Windows Explorer
2. Vào thư mục `lean_six_sigma_app`
3. Click vào thanh địa chỉ ở trên
4. Gõ `cmd` → Enter
5. Command Prompt mở ngay tại thư mục này

**CÁCH 2:**
1. Mở Command Prompt
2. Dùng lệnh `cd` để di chuyển:
```cmd
cd C:\Users\Surface\Downloads\lean_six_sigma_app
```

### Bước 4: Kiểm tra files

```cmd
CHECK.bat
```

Kết quả phải hiện: "All checks PASSED!"

### Bước 5: Cài đặt thư viện

**CÁCH ĐƠN GIẢN NHẤT:**
```cmd
install.bat
```

**CÁCH THỦ CÔNG:**
```cmd
python -m pip install -r requirements.txt
```

⏱️ Quá trình này mất khoảng 2-3 phút

### Bước 6: Chạy ứng dụng

**CÁCH ĐơN GIẢN:**
```cmd
run.bat
```

**CÁCH THỦ CÔNG:**
```cmd
streamlit run app.py
```

### Bước 7: Mở trình duyệt

Tự động mở hoặc truy cập: **http://localhost:8501**

---

## 🔧 CÁC FILE .BAT HỖ TRỢ

### 1. CHECK.bat
Kiểm tra môi trường:
- Python đã cài chưa
- pip có hoạt động không
- Có đang ở đúng thư mục không
- Các files có đầy đủ không

```cmd
CHECK.bat
```

### 2. install.bat
Cài đặt tự động tất cả thư viện:
```cmd
install.bat
```

### 3. run.bat
Chạy ứng dụng:
```cmd
run.bat
```

---

## 🐛 XỬ LÝ LỖI KHÁC

### Lỗi: "python is not recognized"

**Nguyên nhân**: Python chưa được thêm vào PATH

**Giải pháp**:
1. Gỡ cài Python
2. Cài lại và **NHỚ TICK** "Add Python to PATH"
3. Khởi động lại Command Prompt

### Lỗi: "pip is not recognized"

**Giải pháp**:
```cmd
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### Lỗi: "Access is denied"

**Giải pháp**: Chạy Command Prompt với quyền Administrator
1. Tìm "cmd" trong Start Menu
2. Click phải → "Run as administrator"
3. Chạy lại lệnh cài đặt

### Lỗi: "No module named 'streamlit'"

**Nguyên nhân**: Chưa cài đặt thư viện

**Giải pháp**:
```cmd
install.bat
```

### Lỗi: "Address already in use"

**Nguyên nhân**: Port 8501 đang được dùng

**Giải pháp**: Dùng port khác
```cmd
streamlit run app.py --server.port 8502
```

### Lỗi khi cài đặt các package

**Nếu bị lỗi với phiên bản cụ thể**, thử cài không chỉ định version:
```cmd
pip install streamlit pandas plotly python-docx openpyxl reportlab
```

---

## 📂 CẤU TRÚC THƯ MỤC

Sau khi giải nén, bạn phải thấy:

```
lean_six_sigma_app/
│
├── CHECK.bat              ⭐ Kiểm tra hệ thống
├── install.bat            ⭐ Cài đặt tự động
├── run.bat                ⭐ Chạy ứng dụng
│
├── START_HERE.md          Bắt đầu tại đây
├── WINDOWS_SETUP.md       File này
├── README.md              Tài liệu chính
│
├── app.py                 Main app
├── database.py            
├── dashboard.py           
├── gantt_chart.py         
├── export_pdf.py          
│
├── requirements.txt       Danh sách thư viện
├── lean_projects.db       Database mẫu
└── ...
```

Nếu KHÔNG thấy các file này → Kiểm tra lại nơi giải nén!

---

## ✅ KIỂM TRA LẦN CUỐI

Trước khi bắt đầu, hãy chắc chắn:

1. ✅ Python đã cài (version 3.8+)
2. ✅ Đã giải nén file ZIP
3. ✅ Đang ở ĐÚNG thư mục `lean_six_sigma_app`
4. ✅ Thấy file `requirements.txt` khi gõ `dir`
5. ✅ CHECK.bat chạy OK
6. ✅ install.bat chạy xong không lỗi

Nếu TẤT CẢ đều OK → Chạy `run.bat`

---

## 🎯 HƯỚNG DẪN TỪNG BƯỚC CHO NGƯỜI MỚI

### Bước 1: Mở Command Prompt
- Nhấn phím Windows
- Gõ "cmd"
- Enter

### Bước 2: Di chuyển đến thư mục (thay đổi đường dẫn cho đúng)
```cmd
cd C:\Users\Surface\Downloads\lean_six_sigma_app
```

### Bước 3: Kiểm tra
```cmd
dir
```
Phải thấy: `requirements.txt`, `app.py`, `CHECK.bat`, etc.

### Bước 4: Kiểm tra hệ thống
```cmd
CHECK.bat
```

### Bước 5: Cài đặt
```cmd
install.bat
```
Đợi 2-3 phút

### Bước 6: Chạy
```cmd
run.bat
```

### Bước 7: Vào trình duyệt
http://localhost:8501

---

## 📞 VẪN GẶP VẤN ĐỀ?

Gửi cho tôi kết quả của các lệnh sau:

```cmd
REM 1. Kiểm tra Python
python --version

REM 2. Kiểm tra thư mục hiện tại
cd

REM 3. Liệt kê files
dir

REM 4. Kiểm tra requirements.txt
type requirements.txt
```

Copy toàn bộ output và gửi lại để tôi giúp debug!

---

## 🎉 CHÚC MỪNG!

Nếu app đã chạy, bạn sẽ thấy:
- Trình duyệt tự động mở
- Giao diện app Lean Six Sigma
- Có sẵn 5 dự án mẫu để xem

**Chúc bạn sử dụng hiệu quả!** 🚀

---

_Phiên bản: 1.0.0 | Windows Edition_

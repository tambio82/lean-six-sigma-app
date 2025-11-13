# 🔧 Hướng dẫn Cài đặt Chi tiết

## Yêu cầu Hệ thống

- **Python**: 3.8 hoặc mới hơn
- **Hệ điều hành**: Windows, macOS, hoặc Linux
- **RAM**: Tối thiểu 2GB
- **Dung lượng**: ~500MB (bao gồm dependencies)

## Cài đặt Từng Bước

### Bước 1: Cài đặt Python

#### Windows
1. Tải Python từ [python.org](https://www.python.org/downloads/)
2. Chạy installer
3. ✅ **Quan trọng**: Tick vào "Add Python to PATH"
4. Click "Install Now"

#### macOS
```bash
# Sử dụng Homebrew
brew install python3

# Hoặc tải từ python.org
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

### Bước 2: Kiểm tra Python

```bash
python3 --version
# Phải hiện: Python 3.8.x hoặc cao hơn

pip3 --version
# Phải hiện: pip x.x.x
```

### Bước 3: Giải nén Project

```bash
# Di chuyển vào thư mục project
cd lean_six_sigma_app
```

### Bước 4: Cài đặt Dependencies

#### Option 1: Cài đặt toàn cục (Đơn giản)
```bash
pip install -r requirements.txt
```

#### Option 2: Sử dụng Virtual Environment (Khuyến nghị)
```bash
# Tạo virtual environment
python3 -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### Bước 5: Tạo Dữ liệu Mẫu (Tùy chọn)

```bash
python3 create_sample_data.py
```

Lệnh này sẽ tạo:
- 8 Phòng/Ban mẫu
- 5 Dự án mẫu với đầy đủ thông tin
- Team members, Stakeholders
- Kế hoạch Gantt theo DMAIC
- Thông tin ký tên

### Bước 6: Chạy Ứng dụng

#### Cách 1: Sử dụng Script (Khuyến nghị)
```bash
# Unix/Linux/macOS
./run.sh

# Windows
# Mở run.sh bằng Git Bash hoặc dùng cách 2
```

#### Cách 2: Chạy trực tiếp
```bash
streamlit run app.py
```

#### Cách 3: Chỉ định Port khác
```bash
streamlit run app.py --server.port 8502
```

### Bước 7: Truy cập Ứng dụng

1. Mở trình duyệt web
2. Truy cập: **http://localhost:8501**
3. Ứng dụng sẽ tự động mở trong trình duyệt

## ✅ Kiểm tra Cài đặt

Chạy script test:
```bash
python3 test_app.py
```

Nếu thấy "✅ All tests passed!" thì cài đặt thành công!

## 🐛 Xử lý Lỗi Thường gặp

### Lỗi 1: "python: command not found"
**Nguyên nhân**: Python chưa được cài đặt hoặc chưa thêm vào PATH

**Giải pháp**:
```bash
# Thử với python3
python3 --version

# Nếu vẫn lỗi, cài đặt lại Python và tick "Add to PATH"
```

### Lỗi 2: "No module named 'streamlit'"
**Nguyên nhân**: Dependencies chưa được cài đặt

**Giải pháp**:
```bash
pip install streamlit pandas plotly python-docx openpyxl reportlab
```

### Lỗi 3: "Address already in use"
**Nguyên nhân**: Port 8501 đang được sử dụng

**Giải pháp**:
```bash
# Option 1: Dừng process đang dùng port
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Linux/macOS:
lsof -ti:8501 | xargs kill -9

# Option 2: Dùng port khác
streamlit run app.py --server.port 8502
```

### Lỗi 4: PDF không hiển thị tiếng Việt
**Nguyên nhân**: Thiếu font DejaVu

**Giải pháp**:
```bash
# Ubuntu/Debian:
sudo apt-get install fonts-dejavu

# macOS:
# Font đã có sẵn

# Windows:
# Tải và cài đặt DejaVu fonts từ dejavu-fonts.github.io
```

### Lỗi 5: "Permission denied" khi chạy run.sh
**Nguyên nhân**: File chưa có quyền thực thi

**Giải pháp**:
```bash
chmod +x run.sh
./run.sh
```

### Lỗi 6: Database locked
**Nguyên nhân**: Có nhiều session đang mở database

**Giải pháp**:
```bash
# Đóng tất cả session Streamlit
# Xóa file database và tạo lại
rm lean_projects.db
python3 create_sample_data.py
```

## 🔄 Cập nhật Ứng dụng

```bash
# Pull code mới (nếu dùng git)
git pull

# Cập nhật dependencies
pip install -U -r requirements.txt

# Backup database trước khi cập nhật
cp lean_projects.db lean_projects.db.backup
```

## 📦 Cài đặt trên Server

### Sử dụng với Nginx (Production)

1. Cài đặt Nginx
```bash
sudo apt-get install nginx
```

2. Cấu hình Nginx reverse proxy
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

3. Chạy Streamlit như service
```bash
# Tạo systemd service file
sudo nano /etc/systemd/system/lean-app.service

# Thêm nội dung:
[Unit]
Description=Lean Six Sigma App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/lean_six_sigma_app
ExecStart=/usr/bin/streamlit run app.py
Restart=always

[Install]
WantedBy=multi-user.target

# Enable và start service
sudo systemctl enable lean-app
sudo systemctl start lean-app
```

## 🔒 Bảo mật

### Thêm Authentication (Nếu cần)

Chỉnh sửa `.streamlit/config.toml`:
```toml
[server]
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

### Backup Database định kỳ

```bash
# Tạo script backup
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp lean_projects.db backups/lean_projects_$DATE.db

# Thêm vào crontab (chạy mỗi ngày lúc 2AM)
crontab -e
0 2 * * * /path/to/backup-script.sh
```

## 💡 Tips

1. **Luôn dùng Virtual Environment** để tránh conflict với packages khác
2. **Backup database thường xuyên** (file `lean_projects.db`)
3. **Export dữ liệu định kỳ** qua tính năng Export trong app
4. **Monitor logs** khi chạy production
5. **Cập nhật dependencies** định kỳ để có bugfix và features mới

## 📞 Hỗ trợ

Nếu gặp vấn đề không được đề cập ở đây:

1. Chạy `python3 test_app.py` để xem lỗi cụ thể
2. Kiểm tra logs: `tail -f streamlit.log`
3. Liên hệ support: support@hospital.com

---

**Cập nhật lần cuối**: 12/11/2024

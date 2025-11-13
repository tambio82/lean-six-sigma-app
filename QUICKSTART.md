# 🚀 Quick Start Guide

Hướng dẫn nhanh để bắt đầu sử dụng Hệ thống Quản lý Dự án Lean Six Sigma.

## ⚡ Cài đặt Nhanh (5 phút)

### Bước 1: Cài đặt Python
```bash
# Kiểm tra Python đã cài chưa
python3 --version

# Nếu chưa có, cài đặt Python 3.8+
# Ubuntu/Debian:
sudo apt-get update
sudo apt-get install python3 python3-pip

# macOS:
brew install python3
```

### Bước 2: Cài đặt Dependencies
```bash
# Di chuyển vào thư mục project
cd lean_six_sigma_app

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### Bước 3: Chạy Ứng dụng
```bash
# Cách 1: Dùng script (Unix/Linux/macOS)
./run.sh

# Cách 2: Chạy trực tiếp
streamlit run app.py

# Cách 3: Windows
python -m streamlit run app.py
```

### Bước 4: Truy cập
Mở trình duyệt và truy cập: **http://localhost:8501**

## 🎯 Demo với Dữ liệu Mẫu

Để test nhanh với dữ liệu mẫu:

```bash
# Tạo dữ liệu mẫu
python create_sample_data.py

# Chạy app
streamlit run app.py
```

Dữ liệu mẫu bao gồm:
- ✅ 8 Phòng/Ban
- ✅ 5 Dự án mẫu
- ✅ Thành viên, Stakeholders
- ✅ Kế hoạch Gantt theo DMAIC
- ✅ Thông tin ký tên

## 📱 Sử dụng Cơ bản (10 phút)

### 1. Tạo Phòng/Ban đầu tiên
1. Menu → **🏢 Quản lý Phòng/Ban**
2. Nhập tên: "Khoa Nội"
3. Nhấn **Thêm**

### 2. Tạo Dự án đầu tiên
1. Menu → **➕ Thêm dự án mới**
2. Điền thông tin:
   - Mã dự án: `LSS-2024-001`
   - Tên: `Giảm thời gian chờ khám`
   - Phòng/Ban: Chọn "Khoa Nội"
   - Danh mục: Chọn từ 5 nhóm Lean
3. Nhấn **Lưu dự án**

### 3. Thêm Team Members
1. Menu → **📝 Quản lý dự án**
2. Chọn dự án vừa tạo
3. Tab **👥 Thành viên**
4. Thêm thành viên với vai trò

### 4. Tạo Kế hoạch Gantt
1. Tab **📅 Kế hoạch**
2. Thêm công việc theo 5 phases:
   - Define
   - Measure
   - Analyze
   - Improve
   - Control
3. Xem biểu đồ Gantt

### 5. Xem Dashboard
1. Menu → **📊 Dashboard & Thống kê**
2. Xem các biểu đồ tổng quan

### 6. Xuất Báo cáo
1. Vào dự án → Tab **📤 Xuất báo cáo**
2. Chọn format: PDF, Excel, hoặc CSV
3. Tải xuống

## 🎓 DMAIC Workflow

Quy trình chuẩn khi làm dự án Lean Six Sigma:

```
1. DEFINE (Xác định)
   └─ Xác định vấn đề
   └─ Lập team
   └─ Xác định scope

2. MEASURE (Đo lường)
   └─ Thu thập dữ liệu baseline
   └─ Đo lường hiện trạng

3. ANALYZE (Phân tích)
   └─ Phân tích nguyên nhân
   └─ Root cause analysis

4. IMPROVE (Cải tiến)
   └─ Đề xuất giải pháp
   └─ Pilot test
   └─ Triển khai

5. CONTROL (Kiểm soát)
   └─ Standardize
   └─ Monitoring
   └─ Handover
```

## 💡 Tips & Tricks

### Tối ưu hiệu suất
- Backup database thường xuyên (file `lean_projects.db`)
- Export dữ liệu định kỳ
- Cập nhật tiến độ thường xuyên

### Làm việc nhóm
- Đặt tên dự án rõ ràng, dễ hiểu
- Ghi chú đầy đủ trong mô tả
- Cập nhật stakeholders kịp thời
- Review Gantt chart mỗi tuần

### Báo cáo
- Sử dụng Dashboard để present
- Export PDF cho formal reports
- Export Excel để phân tích thêm

## 🔧 Troubleshooting

### App không khởi động?
```bash
# Kiểm tra port 8501 đã được dùng chưa
lsof -i :8501

# Hoặc chạy với port khác
streamlit run app.py --server.port 8502
```

### Lỗi import module?
```bash
# Reinstall requirements
pip install --upgrade -r requirements.txt
```

### Database bị lỗi?
```bash
# Xóa database cũ và tạo mới
rm lean_projects.db
python create_sample_data.py
```

### PDF không có tiếng Việt?
```bash
# Cài font DejaVu
sudo apt-get install fonts-dejavu
```

## 📞 Cần Hỗ trợ?

- 📖 Xem **README.md** để biết chi tiết
- ❓ Menu → **Hướng dẫn sử dụng** trong app
- 📧 Email: support@hospital.com
- 📱 Hotline: 0123-456-789

## 🎉 Bắt đầu ngay!

```bash
cd lean_six_sigma_app
./run.sh
```

Chúc bạn quản lý dự án thành công! 🚀

# 🚀 BẮT ĐẦU NGAY - 3 PHÚT!

## ⚡ Cài đặt Nhanh Chóng

### 1️⃣ Cài đặt Python (nếu chưa có)
- **Windows**: [Tải Python](https://www.python.org/downloads/) → Chạy installer → ✅ Tick "Add to PATH"
- **macOS**: `brew install python3`
- **Linux**: `sudo apt-get install python3 python3-pip`

### 2️⃣ Cài đặt Thư viện
```bash
cd lean_six_sigma_app
pip install -r requirements.txt
```

### 3️⃣ Chạy App
```bash
# Unix/Linux/macOS
./run.sh

# Hoặc
python3 -m streamlit run app.py
```

### 4️⃣ Mở Trình duyệt
➡️ **http://localhost:8501**

---

## 🎉 App đã có Dữ liệu Mẫu!

Tôi đã tạo sẵn dữ liệu demo cho bạn:
- ✅ 8 Phòng/Ban
- ✅ 5 Dự án hoàn chỉnh
- ✅ Team members & Stakeholders
- ✅ Kế hoạch Gantt theo DMAIC
- ✅ Thông tin ký tên

Bạn có thể xem ngay và bắt đầu sử dụng!

---

## 📚 Tài liệu Chi tiết

- **README.md** - Hướng dẫn đầy đủ về tính năng
- **QUICKSTART.md** - Hướng dẫn nhanh 5 phút
- **INSTALL.md** - Hướng dẫn cài đặt chi tiết
- **CHANGELOG.md** - Lịch sử phát triển

---

## ✅ Kiểm tra Cài đặt

Chạy script test:
```bash
python3 test_app.py
```

Nếu thấy "✅ All tests passed!" → Bạn đã sẵn sàng!

---

## 🎯 Các Bước Tiếp Theo

### Tùy chọn A: Xem Demo
1. Chạy app với dữ liệu mẫu có sẵn
2. Khám phá các tính năng
3. Xem Dashboard, Gantt chart, Export PDF...

### Tùy chọn B: Bắt đầu Fresh
```bash
# Xóa dữ liệu mẫu
rm lean_projects.db

# Chạy app - database mới sẽ tự động được tạo
streamlit run app.py
```

### Tùy chọn C: Tạo lại Dữ liệu Mẫu
```bash
python3 create_sample_data.py
```

---

## 💡 Menu Chính trong App

🏠 **Trang chủ** - Tổng quan và thống kê  
➕ **Thêm dự án mới** - Tạo dự án Lean Six Sigma  
📝 **Quản lý dự án** - Chỉnh sửa, team, stakeholders, Gantt  
📊 **Dashboard** - Biểu đồ và phân tích  
🏢 **Phòng/Ban** - Quản lý danh mục  
📤 **Import/Export** - Sao lưu và khôi phục  
❓ **Hướng dẫn** - Hướng dẫn chi tiết trong app  

---

## 🐛 Lỗi Thường Gặp

### "python: command not found"
➡️ Dùng `python3` thay vì `python`

### "No module named 'streamlit'"
➡️ Chạy: `pip install -r requirements.txt`

### "Address already in use"
➡️ Chạy: `streamlit run app.py --server.port 8502`

### Chi tiết hơn
➡️ Xem **INSTALL.md** phần "Xử lý Lỗi"

---

## 🎓 DMAIC Workflow

Khi tạo dự án Lean Six Sigma, tuân theo 5 giai đoạn:

1. **Define** - Xác định vấn đề và mục tiêu
2. **Measure** - Đo lường hiện trạng
3. **Analyze** - Phân tích nguyên nhân
4. **Improve** - Triển khai cải tiến
5. **Control** - Kiểm soát và duy trì

---

## 📞 Cần Hỗ trợ?

📧 Email: support@hospital.com  
📱 Hotline: 0123-456-789  
📖 Xem docs trong thư mục project  

---

## 🌟 Các Tính Năng Chính

✅ Quản lý đầy đủ thông tin dự án Lean Six Sigma  
✅ Gantt Chart timeline với DMAIC phases  
✅ Dashboard thống kê đa dạng  
✅ Xuất báo cáo PDF, Excel, CSV  
✅ 5 danh mục Lean tại bệnh viện  
✅ Quản lý team members & stakeholders  
✅ Theo dõi tiến độ và cảnh báo quá hạn  
✅ Import/Export dữ liệu  

---

## 🚀 Bắt đầu Ngay!

```bash
cd lean_six_sigma_app
pip install -r requirements.txt
python3 -m streamlit run app.py
```

**➡️ http://localhost:8501**

Chúc bạn quản lý dự án thành công! 🎉

---

_Phiên bản: 1.0.0 | Cập nhật: 12/11/2024_

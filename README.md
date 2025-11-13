# 🏥 Hệ thống Quản lý Dự án Lean Six Sigma

Web application quản lý thông tin các dự án Lean Six Sigma cho bệnh viện, được xây dựng bằng Streamlit.

## ✨ Tính năng chính

### 1. Quản lý Thông tin Dự án
- **Thông tin chung**: Mã dự án, tên, phòng ban, danh mục, trạng thái, ngày tháng
- **Thành viên**: Quản lý team members với vai trò và thông tin liên hệ
- **Stakeholders**: Theo dõi các bên liên quan với mức độ ảnh hưởng
- **Phạm vi dự án**: Mô tả vấn đề, mục tiêu, phạm vi
- **Ngân sách**: Theo dõi ngân sách dự kiến và chi phí thực tế

### 2. Kế hoạch Chi tiết (Gantt Chart)
- Tạo kế hoạch theo DMAIC phases (Define, Measure, Analyze, Improve, Control)
- Biểu đồ Gantt trực quan với nhiều kiểu hiển thị
- Theo dõi tiến độ từng công việc
- Cảnh báo công việc quá hạn

### 3. Bảng Ký tên
- Quản lý thông tin người ký duyệt
- Ghi chú và ngày ký

### 4. Dashboard & Thống kê
- Biểu đồ theo trạng thái, danh mục, phòng ban
- So sánh ngân sách vs chi phí thực tế
- Heatmap số lượng dự án theo thời gian
- Tùy chỉnh loại biểu đồ (Pie, Bar, Heatmap, Funnel...)

### 5. Quản lý Danh mục
- 5 nhóm mục đích Lean Six Sigma:
  1. An toàn người bệnh
  2. Hướng đến Hài lòng cho người bệnh
  3. Hướng đến hài lòng cho nhân viên
  4. Nâng cao chất lượng chuyên môn
  5. Bệnh viện thông minh

### 6. Xuất báo cáo
- **PDF**: Báo cáo đầy đủ định dạng chuyên nghiệp với tiếng Việt
- **Excel**: Dữ liệu chi tiết với nhiều sheets
- **CSV**: Dữ liệu để phân tích

### 7. Import/Export
- Import dữ liệu từ Excel/CSV
- Export toàn bộ database

## 🚀 Cài đặt

### Yêu cầu
- Python 3.8 trở lên
- pip

### Các bước cài đặt

1. **Clone hoặc tải project về**
```bash
cd lean_six_sigma_app
```

2. **Cài đặt thư viện**
```bash
pip install -r requirements.txt
```

3. **Chạy ứng dụng**
```bash
streamlit run app.py
```

4. **Truy cập ứng dụng**
- Mở trình duyệt và truy cập: `http://localhost:8501`

## 📁 Cấu trúc thư mục

```
lean_six_sigma_app/
│
├── app.py                 # File chính của Streamlit app
├── database.py            # Quản lý database SQLite
├── gantt_chart.py         # Tạo biểu đồ Gantt
├── export_pdf.py          # Xuất báo cáo PDF
├── dashboard.py           # Tạo dashboard và biểu đồ thống kê
├── requirements.txt       # Danh sách thư viện cần thiết
├── README.md             # File hướng dẫn này
│
└── lean_projects.db      # Database SQLite (tự động tạo khi chạy)
```

## 💾 Database

Ứng dụng sử dụng SQLite để lưu trữ dữ liệu với các bảng:

1. **projects**: Thông tin dự án
2. **team_members**: Thành viên dự án
3. **stakeholders**: Các bên liên quan
4. **project_tasks**: Kế hoạch chi tiết (Gantt)
5. **signoffs**: Thông tin ký tên
6. **departments**: Danh mục phòng/ban

Database được tạo tự động khi chạy ứng dụng lần đầu.

## 📖 Hướng dẫn sử dụng

### Bước 1: Thêm Phòng/Ban
1. Vào menu "🏢 Quản lý Phòng/Ban"
2. Thêm các phòng/ban/khoa trong bệnh viện
3. Ví dụ: Khoa Nội, Khoa Ngoại, Phòng Kế hoạch...

### Bước 2: Tạo Dự án Mới
1. Vào menu "➕ Thêm dự án mới"
2. Điền thông tin:
   - Mã dự án (bắt buộc)
   - Tên dự án (bắt buộc)
   - Phòng/Ban (bắt buộc)
   - Danh mục theo 5 nhóm Lean (bắt buộc)
   - Các thông tin khác
3. Nhấn "Lưu dự án"

### Bước 3: Quản lý Chi tiết Dự án
1. Vào menu "📝 Quản lý dự án"
2. Chọn dự án cần quản lý
3. Sử dụng các tab:
   - **Thông tin**: Chỉnh sửa thông tin dự án
   - **Thành viên**: Thêm team members
   - **Stakeholders**: Thêm các bên liên quan
   - **Kế hoạch**: Tạo timeline theo DMAIC
   - **Ký tên**: Thêm thông tin phê duyệt
   - **Xuất báo cáo**: Export PDF/Excel/CSV

### Bước 4: Theo dõi và Báo cáo
1. Vào menu "📊 Dashboard & Thống kê"
2. Xem các biểu đồ tổng quan
3. Chọn loại biểu đồ phù hợp để phân tích

## 🎯 Best Practices

### DMAIC Methodology
Khi tạo kế hoạch, nên tuân theo 5 giai đoạn của Lean Six Sigma:

1. **Define**: Xác định vấn đề và mục tiêu
   - Xác định phạm vi dự án
   - Lập team và stakeholders
   - Xác định VOC (Voice of Customer)

2. **Measure**: Đo lường hiện trạng
   - Thu thập dữ liệu baseline
   - Xác định các metrics chính
   - Đo lường hiệu suất hiện tại

3. **Analyze**: Phân tích nguyên nhân gốc rễ
   - Phân tích dữ liệu
   - Xác định root causes
   - Validate nguyên nhân

4. **Improve**: Cải tiến
   - Đề xuất giải pháp
   - Pilot test
   - Triển khai cải tiến

5. **Control**: Kiểm soát và duy trì
   - Standardize quy trình mới
   - Monitoring và control
   - Handover và close project

### Tips sử dụng
- Cập nhật tiến độ thường xuyên để theo dõi hiệu quả
- Sao lưu dữ liệu định kỳ bằng Export
- Ghi rõ thông tin stakeholders để quản lý kỳ vọng
- Sử dụng Gantt chart để visualize timeline
- Review dashboard để có cái nhìn tổng quan

## 🔧 Tùy chỉnh

### Thay đổi danh mục dự án
Chỉnh sửa biến `LEAN_CATEGORIES` trong file `app.py`:
```python
LEAN_CATEGORIES = [
    "Danh mục 1",
    "Danh mục 2",
    # ...
]
```

### Thay đổi trạng thái dự án
Chỉnh sửa biến `PROJECT_STATUS` trong file `app.py`:
```python
PROJECT_STATUS = [
    "Trạng thái 1",
    "Trạng thái 2",
    # ...
]
```

## ⚠️ Lưu ý

1. **Backup dữ liệu**: File `lean_projects.db` chứa toàn bộ dữ liệu. Nên backup định kỳ.
2. **Font tiếng Việt trong PDF**: Cần cài đặt font DejaVu để hiển thị tiếng Việt trong PDF:
   ```bash
   sudo apt-get install fonts-dejavu
   ```
3. **Performance**: Với số lượng dự án lớn (>1000), nên cân nhắc chuyển sang PostgreSQL

## 🐛 Troubleshooting

### Lỗi font khi export PDF
```bash
sudo apt-get install fonts-dejavu fonts-dejavu-core fonts-dejavu-extra
```

### Lỗi Plotly không hiển thị
```bash
pip install --upgrade plotly
```

### Lỗi database locked
- Đóng tất cả các session đang mở
- Restart ứng dụng

## 📞 Liên hệ & Hỗ trợ

Nếu gặp vấn đề hoặc có đề xuất cải tiến, vui lòng liên hệ:
- Email: support@hospital.com
- Hotline: 0123-456-789

## 📄 License

Copyright © 2024. All rights reserved.

## 🙏 Acknowledgments

- Streamlit Framework
- Plotly for visualizations
- ReportLab for PDF generation
- SQLite for database

---

**Phiên bản**: 1.0.0  
**Cập nhật**: 12/11/2024

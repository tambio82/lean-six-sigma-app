# 🌟 Tính Năng Chi Tiết

## Tổng quan

Hệ thống Quản lý Dự án Lean Six Sigma được thiết kế đặc biệt cho bệnh viện, giúp quản lý và theo dõi các dự án cải tiến chất lượng theo phương pháp Lean Six Sigma.

---

## 1. 🏠 Trang Chủ

### Metrics Dashboard
- **Tổng số dự án**: Hiển thị số lượng dự án trong hệ thống
- **Tổng ngân sách**: Tổng ngân sách của tất cả dự án
- **Chi phí thực tế**: Tổng chi phí đã sử dụng
- **Tỷ lệ sử dụng ngân sách**: Phần trăm ngân sách đã dùng

### Danh sách Dự án Gần đây
- Hiển thị 10 dự án mới nhất
- Thông tin: Mã, tên, phòng ban, danh mục, trạng thái, ngày tháng
- Sắp xếp theo thời gian tạo mới nhất

---

## 2. ➕ Thêm Dự án Mới

### Thông tin Cơ bản
- **Mã dự án** (*): Mã định danh duy nhất (VD: LSS-2024-001)
- **Tên dự án** (*): Tên đầy đủ của dự án
- **Phòng/Ban** (*): Chọn từ danh sách có sẵn
- **Danh mục** (*): Chọn từ 5 nhóm Lean:
  1. An toàn người bệnh
  2. Hướng đến Hài lòng cho người bệnh
  3. Hướng đến hài lòng cho nhân viên
  4. Nâng cao chất lượng chuyên môn
  5. Bệnh viện thông minh

### Thông tin Chi tiết
- **Trạng thái**: Lên kế hoạch / Đang thực hiện / Tạm dừng / Hoàn thành / Hủy bỏ
- **Ngày bắt đầu & Kết thúc**: Date picker
- **Ngân sách**: Nhập số tiền (VNĐ)
- **Mô tả chung**: Mô tả ngắn gọn
- **Mô tả vấn đề**: Vấn đề cần giải quyết
- **Mục tiêu**: Mục tiêu cụ thể của dự án
- **Phạm vi**: Phạm vi và giới hạn

### Validation
- Các trường bắt buộc (*) phải điền đầy đủ
- Mã dự án phải duy nhất (không trùng)
- Ngày kết thúc phải sau ngày bắt đầu

---

## 3. 📝 Quản lý Dự án

### 3.1 📄 Thông tin Dự án

#### Chức năng
- Xem và chỉnh sửa tất cả thông tin dự án
- Cập nhật chi phí thực tế
- Thay đổi trạng thái dự án
- Xóa dự án (với xác nhận 2 lần)

#### Hiển thị
- Mã dự án (không thay đổi được)
- Ngày tạo và cập nhật lần cuối
- Form chỉnh sửa với tất cả các trường

### 3.2 👥 Thành viên Dự án

#### Danh sách Thành viên
- Hiển thị dạng expandable cards
- Thông tin: Tên, vai trò, phòng ban, email, điện thoại
- Nút xóa cho từng thành viên

#### Thêm Thành viên Mới
- **Họ tên** (*): Tên đầy đủ
- **Vai trò** (*): VD: Trưởng nhóm, Thành viên, Sponsor...
- **Phòng/Ban**: Chọn từ danh sách
- **Email**: Địa chỉ email
- **Điện thoại**: Số điện thoại liên hệ

### 3.3 🤝 Stakeholders (Bên liên quan)

#### Danh sách Stakeholders
- Hiển thị dạng expandable cards
- Thông tin: Tên, vai trò, phòng ban, mức độ ảnh hưởng, mức độ tham gia
- Nút xóa cho từng stakeholder

#### Thêm Stakeholder Mới
- **Họ tên** (*): Tên đầy đủ
- **Vai trò** (*): Chức vụ / vai trò
- **Phòng/Ban**: Khoa/phòng đang công tác
- **Mức độ ảnh hưởng**: Thấp / Trung bình / Cao / Rất cao
- **Mức độ tham gia**: Ít / Vừa phải / Tích cực / Rất tích cực

### 3.4 📅 Kế hoạch Chi tiết (Gantt Chart)

#### Biểu đồ Gantt
- **Gantt Chart cơ bản**: Timeline tổng quan
- **DMAIC Gantt**: Phân theo 5 phases với màu sắc riêng
  - Define: Xanh dương
  - Measure: Tím
  - Analyze: Đỏ cam
  - Improve: Xanh lá
  - Control: Xám

#### Metrics
- **Tiến độ tổng thể**: Phần trăm hoàn thành trung bình
- **Tóm tắt theo Phase**: Số công việc và tiến độ từng phase
- **Cảnh báo quá hạn**: Danh sách tasks đã quá deadline

#### Danh sách Công việc
- Bảng hiển thị tất cả tasks
- Thông tin: Phase, tên, ngày, người phụ trách, trạng thái, tiến độ
- Sắp xếp theo thời gian

#### Thêm Công việc Mới
- **Phase** (*): Chọn từ Define/Measure/Analyze/Improve/Control
- **Tên công việc** (*): Mô tả ngắn gọn
- **Ngày bắt đầu & Kết thúc** (*): Date picker
- **Người phụ trách**: Tên người chịu trách nhiệm
- **Trạng thái**: Chưa bắt đầu / Đang thực hiện / Hoàn thành / Tạm dừng
- **Tiến độ**: Slider 0-100%

### 3.5 ✍️ Bảng Ký tên

#### Danh sách Người ký
- Hiển thị dạng expandable cards
- Thông tin: Vai trò, người ký, ngày ký, ghi chú
- Nút xóa cho từng record

#### Thêm Người ký
- **Vai trò/Chức vụ** (*): VD: Trưởng khoa, Giám đốc...
- **Họ tên người ký**: Tên đầy đủ
- **Ngày ký**: Date picker
- **Ghi chú**: Ghi chú thêm (nếu có)

### 3.6 📤 Xuất Báo cáo

#### Xuất PDF
- Báo cáo đầy đủ định dạng chuyên nghiệp
- Hỗ trợ tiếng Việt với font DejaVu
- Bao gồm:
  - Thông tin dự án
  - Team members
  - Stakeholders
  - Kế hoạch chi tiết
  - Bảng ký tên
- Download ngay sau khi tạo

#### Xuất Excel
- File Excel với nhiều sheets:
  - Sheet 1: Thông tin dự án
  - Sheet 2: Thành viên
  - Sheet 3: Stakeholders
  - Sheet 4: Kế hoạch
  - Sheet 5: Ký tên
- Format chuẩn, dễ đọc và phân tích

#### Xuất CSV
- Dữ liệu kế hoạch (tasks) định dạng CSV
- Dễ import vào Excel, Google Sheets
- Phù hợp cho phân tích dữ liệu

---

## 4. 📊 Dashboard & Thống kê

### Metrics Tổng quan
Hiển thị ở đầu trang:
- Tổng số dự án
- Tổng ngân sách
- Chi phí thực tế
- Tỷ lệ sử dụng ngân sách

### Tùy chọn Biểu đồ
Người dùng chọn loại biểu đồ muốn xem:
- ☑️ Trạng thái
- ☑️ Danh mục
- ☑️ Phòng/Ban
- ☑️ Ngân sách
- ☑️ Heatmap
- ☑️ Timeline

### Các loại Biểu đồ

#### Biểu đồ Trạng thái
- **Pie Chart**: Phân bố dự án theo trạng thái
- Màu sắc khác nhau cho mỗi trạng thái
- Hiển thị phần trăm và số lượng

#### Biểu đồ Danh mục
- **Bar Chart**: Số lượng dự án theo 5 danh mục Lean
- Hiển thị số lượng trên mỗi cột
- Sắp xếp theo số lượng

#### Biểu đồ Phòng/Ban
- **Bar Chart**: Phân bố theo phòng ban
- Màu gradient theo số lượng
- Có thể chuyển sang Pie hoặc Treemap

#### Biểu đồ Ngân sách
- **Grouped Bar Chart**: So sánh ngân sách vs chi phí thực tế
- 2 cột: Ngân sách dự kiến (xanh) và Chi phí thực tế (cam)
- Hiển thị giá trị VNĐ

#### Heatmap
- **Heatmap**: Số lượng dự án theo tháng/năm
- Màu đậm hơn = nhiều dự án hơn
- Dễ dàng nhận biết xu hướng theo thời gian

#### Dashboard Tổng quan
- Kết hợp 4 biểu đồ trong 1 view
- Layout 2x2 grid
- Tổng quan toàn diện

---

## 5. 🏢 Quản lý Phòng/Ban

### Danh sách Phòng/Ban
- Hiển thị tất cả phòng ban đã tạo
- Thông tin: Tên và mô tả
- Nút xóa cho từng phòng ban

### Thêm Phòng/Ban Mới
- **Tên Phòng/Ban** (*): Tên đầy đủ
- **Mô tả**: Mô tả ngắn gọn về chức năng

### Sử dụng
- Danh sách này dùng cho dropdown trong:
  - Thêm dự án mới
  - Thêm thành viên
  - Thêm stakeholders

---

## 6. 📤 Import/Export Dữ liệu

### Import (Đang phát triển)
- Upload file Excel hoặc CSV
- Xem trước dữ liệu
- Import vào hệ thống

### Export

#### Export Tất cả Dự án (Excel)
- Xuất toàn bộ dữ liệu dự án
- Format: .xlsx
- Filename: All_Projects_YYYYMMDD.xlsx

#### Export Tất cả Dự án (CSV)
- Xuất toàn bộ dữ liệu dự án
- Format: .csv
- Filename: All_Projects_YYYYMMDD.csv

### Backup & Restore
- File database: `lean_projects.db`
- Copy file này để backup
- Replace file để restore

---

## 7. ❓ Hướng dẫn Sử dụng

### Nội dung Hướng dẫn
- Giới thiệu từng menu
- Hướng dẫn chi tiết từng chức năng
- Mẹo sử dụng
- Best practices cho Lean Six Sigma
- DMAIC workflow
- Thông tin liên hệ hỗ trợ

### Format
- Markdown với formatting rõ ràng
- Có phân cấp heading
- Dễ đọc, dễ hiểu
- Có ví dụ minh họa

---

## 🎯 Tính Năng Đặc Biệt

### DMAIC Integration
- Kế hoạch được tổ chức theo 5 phases chuẩn
- Màu sắc riêng biệt cho mỗi phase
- Timeline rõ ràng theo từng phase

### Cảnh báo Thông minh
- Tự động cảnh báo tasks quá hạn
- Hiển thị rõ trong Gantt
- Danh sách chi tiết tasks cần chú ý

### Responsive Design
- Giao diện thân thiện
- Hoạt động tốt trên desktop
- Layout tối ưu cho nhiều kích thước màn hình

### Tiếng Việt Full Support
- Toàn bộ giao diện tiếng Việt
- PDF export hỗ trợ tiếng Việt
- Font DejaVu cho tài liệu

---

## 🔐 Bảo mật & Quyền

### Hiện tại
- Single user mode
- Local database
- No authentication

### Có thể mở rộng
- Multi-user authentication
- Role-based access control (RBAC)
- Audit logs
- Data encryption

---

## 🚀 Performance

### Tối ưu
- SQLite database nhanh và nhẹ
- Caching với Streamlit
- Lazy loading cho dữ liệu lớn
- Pagination tự động

### Giới hạn
- Phù hợp cho <1000 dự án
- Nếu lớn hơn, nên chuyển sang PostgreSQL
- Single user - không hỗ trợ concurrent writes

---

## 💡 Tips & Best Practices

1. **Tạo Phòng/Ban trước**: Sẽ tiện cho việc chọn sau này
2. **Cập nhật tiến độ đều đặn**: Mỗi tuần update một lần
3. **Backup thường xuyên**: Export dữ liệu mỗi tháng
4. **Tuân theo DMAIC**: Tạo tasks theo đúng 5 phases
5. **Ghi chú đầy đủ**: Giúp theo dõi tốt hơn
6. **Review Gantt thường xuyên**: Phát hiện sớm vấn đề
7. **Cập nhật stakeholders**: Communicate kịp thời

---

_Để biết thêm chi tiết, xem README.md hoặc hướng dẫn trong app._

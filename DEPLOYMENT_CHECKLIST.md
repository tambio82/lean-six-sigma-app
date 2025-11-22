# ✅ DEPLOYMENT CHECKLIST
## Phase 2 - PDCA/PDSA + Bug Fixes

**Thời gian ước tính: 45 phút**

---

## 📥 CHUẨN BỊ (5 phút)

- [ ] Đã download tất cả 9 files trong folder này
- [ ] Đã đọc qua DEPLOYMENT_SUMMARY.txt
- [ ] Đã đọc qua README.md
- [ ] Đã có access vào:
  - [ ] GitHub repository
  - [ ] Streamlit Cloud dashboard
  - [ ] Supabase database

---

## 💾 BACKUP (5 phút)

- [ ] Backup code hiện tại:
  ```bash
  git add .
  git commit -m "Backup before Phase 2"
  git push origin main
  ```

- [ ] Backup database Supabase:
  - [ ] Vào Supabase Dashboard
  - [ ] Settings → Database → Backups
  - [ ] Create manual backup

---

## 📁 THAY THẾ FILES (10 phút)

- [ ] Copy các file collaboration files:
  - [ ] collaboration.py → thay file cũ
  - [ ] comments_manager.py → thay file cũ
  - [ ] activity_tracker.py → thay file cũ
  - [ ] meeting_manager.py → thay file cũ
  - [ ] notification_service.py → thay file cũ

- [ ] Copy file mới:
  - [ ] pdca_pdsa_tools.py → thêm vào project root

- [ ] Verify files đã đúng vị trí:
  ```bash
  ls -la *.py | grep -E "(collaboration|comments|activity|meeting|notification|pdca)"
  ```

---

## ✏️ CẬP NHẬT APP.PY (15 phút)

### Bước 1: Thêm Import
- [ ] Mở file app.py
- [ ] Tìm dòng ~12 (sau `from dmaic_tools import DMAICTools`)
- [ ] Thêm dòng:
  ```python
  from pdca_pdsa_tools import PDCATools
  ```
- [ ] Save file

### Bước 2: Update Function
- [ ] Tìm function `render_dmaic_tracking()` (dòng 308-343)
- [ ] XÓA toàn bộ function cũ
- [ ] PASTE function mới từ APP_UPDATE_SNIPPET.py
- [ ] Verify syntax (không có lỗi đỏ trong editor)
- [ ] Save file

---

## 🗄️ CẬP NHẬT DATABASE (10 phút)

- [ ] Mở Supabase Dashboard
- [ ] Vào SQL Editor
- [ ] Copy SQL từ INTEGRATION_GUIDE.md (section Database Update)
- [ ] Chạy CREATE TABLE statements:
  - [ ] methodology_data
  - [ ] methodology_actions
  - [ ] methodology_metrics
  - [ ] methodology_measurements
  - [ ] methodology_issues
  - [ ] methodology_lessons
  - [ ] methodology_rollout

- [ ] Verify trong Table Editor:
  - [ ] 7 tables mới đã được tạo
  - [ ] Indexes đã được tạo

---

## 🚀 DEPLOY (5 phút)

- [ ] Commit changes:
  ```bash
  git add .
  git status  # Kiểm tra files thay đổi
  git commit -m "Phase 2: PDCA/PDSA support + bug fixes"
  ```

- [ ] Push to GitHub:
  ```bash
  git push origin main
  ```

- [ ] Theo dõi deployment:
  - [ ] Vào Streamlit Cloud dashboard
  - [ ] Xem logs deploy
  - [ ] Đợi status = "Running"

---

## ✅ KIỂM TRA (10 phút)

### Test Cơ Bản
- [ ] App khởi động không lỗi
- [ ] Không có error trong logs
- [ ] Có thể tạo project mới
- [ ] Existing DMAIC projects vẫn hoạt động

### Test Collaboration (Bug Fixes)
- [ ] Vào project bất kỳ
- [ ] Click tab "Cộng tác"
- [ ] Kiểm tra:
  - [ ] Activity Log hiển thị
  - [ ] Không có error "get_activities limit"
  - [ ] Có thể post comment
  - [ ] Autocomplete team members hoạt động
  - [ ] Không có error "str has no attribute get"

### Test PDCA (New Feature)
- [ ] Tạo project mới
- [ ] Chọn methodology = "PDCA"
- [ ] Vào tab "Tracking"
- [ ] Verify 4 tabs hiển thị:
  - [ ] Plan
  - [ ] Do
  - [ ] Check
  - [ ] Act
- [ ] Test mỗi tab:
  - [ ] Có thể save dữ liệu
  - [ ] Charts hiển thị đúng
  - [ ] Data persist sau refresh

### Test PDSA (New Feature)
- [ ] Tạo project mới
- [ ] Chọn methodology = "PDSA"
- [ ] Vào tab "Tracking"
- [ ] Verify 4 tabs hiển thị:
  - [ ] Plan
  - [ ] Do
  - [ ] Study (thay vì Check)
  - [ ] Act
- [ ] Test cơ bản tương tự PDCA

---

## 🎉 HOÀN THÀNH

- [ ] Tất cả tests passed
- [ ] Không có errors trong logs
- [ ] App chạy smooth
- [ ] Data saving correctly

---

## 📝 POST-DEPLOYMENT

- [ ] Thông báo team về update
- [ ] Train users về PDCA/PDSA
- [ ] Monitor usage trong vài ngày đầu
- [ ] Gather feedback
- [ ] Document any issues

---

## 🐛 NẾU CÓ VẤN ĐỀ

### Gặp Import Error
```bash
# Kiểm tra file tồn tại
ls -la pdca_pdsa_tools.py

# Restart Streamlit
# (Streamlit Cloud tự restart khi push)
```

### Gặp Database Error
```sql
-- Kiểm tra tables trong Supabase Table Editor
-- Re-run CREATE TABLE statements nếu cần
```

### Collaboration vẫn bị lỗi
```bash
# Đảm bảo đã thay đúng file
cp collaboration.py /your/project/collaboration.py
cp comments_manager.py /your/project/comments_manager.py

# Push lại
git add .
git commit -m "Fix: ensure correct collaboration files"
git push origin main
```

### Data không save
- [ ] Check Supabase connection
- [ ] Verify database methods exist
- [ ] Check browser console
- [ ] Review Streamlit logs

---

## 📞 NEED HELP?

1. Check INTEGRATION_GUIDE.md
2. Review DEPLOYMENT_SUMMARY.txt
3. Check Streamlit Cloud logs
4. Verify database schema
5. Test with simple case

---

## ✨ SUCCESS CRITERIA

Deployment thành công khi:

✅ App khởi động không lỗi
✅ Collaboration features work (no bugs)
✅ PDCA methodology fully functional
✅ PDSA methodology fully functional
✅ DMAIC methodology still works (unchanged)
✅ Data saves and loads correctly
✅ No errors in console/logs
✅ Users happy! 😊

---

═══════════════════════════════════════════════════════
DEPLOYMENT CHECKLIST - Phase 2
Version 2.0 | November 22, 2025
Tam Mai - Lean Six Sigma Hospital App
═══════════════════════════════════════════════════════

**Print this checklist and check items as you complete them!**

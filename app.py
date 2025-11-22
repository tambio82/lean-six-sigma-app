"""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║              📋 READY-TO-COPY CODE SNIPPETS 📋                          ║
║                                                                          ║
║              Copy & Paste trực tiếp vào app.py của bạn                  ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

# ==================== SNIPPET 1: FOR render_add_project() ====================
# Vị trí: SAU dòng budget = st.number_input(...)
# Copy toàn bộ đoạn code từ đây:

        # ==================== METHODOLOGY SELECTION ====================
        st.write("---")
        st.write("### 🔧 Phương pháp Cải tiến")
        
        col_method1, col_method2 = st.columns([3, 1])
        
        with col_method1:
            methodology = st.selectbox(
                "Chọn Methodology *",
                ["DMAIC", "PDCA", "PDSA"],
                index=0,
                help="""
                • DMAIC: Define → Measure → Analyze → Improve → Control (Six Sigma)
                • PDCA: Plan → Do → Check → Act (Deming Cycle)
                • PDSA: Plan → Do → Study → Act (Quality Improvement)
                """
            )
        
        with col_method2:
            methodology_icons = {
                'DMAIC': '🔵',
                'PDCA': '🟢',
                'PDSA': '🟡'
            }
            st.markdown(f"### {methodology_icons.get(methodology, '⚪')} {methodology}")
        
        # Info expander
        methodology_info = {
            'DMAIC': {
                'name': 'DMAIC - Six Sigma',
                'phases': '5 phases: Define → Measure → Analyze → Improve → Control',
                'best_for': '✅ Dự án phức tạp, cần phân tích dữ liệu chi tiết',
                'example': 'Ví dụ: Giảm thời gian chờ khám từ 60 phút xuống 30 phút'
            },
            'PDCA': {
                'name': 'PDCA - Deming Cycle',
                'phases': '4 phases: Plan → Do → Check → Act',
                'best_for': '✅ Cải tiến quy trình, tiêu chuẩn hóa công việc',
                'example': 'Ví dụ: Triển khai quy trình rửa tay 5 bước'
            },
            'PDSA': {
                'name': 'PDSA - Quality Improvement',
                'phases': '4 phases: Plan → Do → Study → Act',
                'best_for': '✅ Đổi mới sáng tạo, học hỏi từ thử nghiệm',
                'example': 'Ví dụ: Pilot chương trình giáo dục bệnh nhân tiểu đường'
            }
        }
        
        info = methodology_info[methodology]
        
        with st.expander(f"ℹ️ Tìm hiểu về {methodology}"):
            st.write(f"**{info['name']}**")
            st.write(f"📊 {info['phases']}")
            st.write(f"{info['best_for']}")
            st.write(f"💡 {info['example']}")
        # ==================== END METHODOLOGY SELECTION ====================

# Đến đây! Paste vào app.py


# ==================== SNIPPET 2: FOR project_data dict ====================
# Vị trí: Trong render_add_project(), khi tạo project_data
# TÌM dòng có 'budget': budget,
# THÊM dòng này NGAY SAU nó:

                    'methodology': methodology,

# Ví dụ đầy đủ:
"""
                project_data = {
                    'project_code': project_code,
                    'project_name': project_name,
                    'department': department,
                    'category': category,
                    'status': status,
                    'start_date': str(start_date),
                    'end_date': str(end_date),
                    'budget': budget,
                    'methodology': methodology,  # ⬅️ THÊM DÒNG NÀY
                    'description': description,
                    'problem_statement': problem_statement,
                    'goal': goal,
                    'scope': scope,
                    'actual_cost': 0
                }
"""


# ==================== SNIPPET 3: FOR render_project_info() - EDIT FORM ====================
# Vị trí: Trong render_project_info(), sau dropdown category
# Copy toàn bộ đoạn code từ đây:

            # Methodology selection
            current_methodology = project.get('methodology', 'DMAIC')
            methodology_options = ['DMAIC', 'PDCA', 'PDSA']
            methodology_index = methodology_options.index(current_methodology) if current_methodology in methodology_options else 0
            
            methodology = st.selectbox(
                "Phương pháp",
                methodology_options,
                index=methodology_index
            )

# Đến đây! Paste vào app.py


# ==================== SNIPPET 4: FOR updated_data dict ====================
# Vị trí: Trong render_project_info(), khi update project
# TÌM dòng có 'budget': budget,
# THÊM dòng này NGAY SAU nó:

                'methodology': methodology,

# Ví dụ đầy đủ:
"""
            updated_data = {
                'project_name': project_name,
                'department': department,
                'category': category,
                'status': status,
                'start_date': str(start_date),
                'end_date': str(end_date),
                'budget': budget,
                'methodology': methodology,  # ⬅️ THÊM DÒNG NÀY
                'description': description,
                'problem_statement': problem_statement,
                'goal': goal,
                'scope': scope
            }
"""


# ==================== VISUAL GUIDE ====================
"""
┌─────────────────────────────────────────────────────────────────────────┐
│                        TRƯỚC KHI THÊM CODE                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   with col2:                                                            │
│       status = st.selectbox("Trạng thái *", PROJECT_STATUS)            │
│       start_date = st.date_input("Ngày bắt đầu *", ...)                │
│       end_date = st.date_input("Ngày kết thúc *", ...)                 │
│       budget = st.number_input("Ngân sách (VNĐ)", ...)                 │
│                                                                         │
│   # ⬇️⬇️⬇️ THÊM SNIPPET 1 VÀO ĐÂY ⬇️⬇️⬇️                               │
│                                                                         │
│   st.write("---")                                                       │
│   st.write("### 2. Mô tả dự án")                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                         SAU KHI THÊM CODE                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   with col2:                                                            │
│       status = st.selectbox("Trạng thái *", PROJECT_STATUS)            │
│       start_date = st.date_input("Ngày bắt đầu *", ...)                │
│       end_date = st.date_input("Ngày kết thúc *", ...)                 │
│       budget = st.number_input("Ngân sách (VNĐ)", ...)                 │
│                                                                         │
│   # ==================== METHODOLOGY SELECTION ====================    │
│   st.write("---")                                                       │
│   st.write("### 🔧 Phương pháp Cải tiến")                              │
│                                                                         │
│   col_method1, col_method2 = st.columns([3, 1])                        │
│                                                                         │
│   with col_method1:                                                     │
│       methodology = st.selectbox(                                       │
│           "Chọn Methodology *",                                         │
│           ["DMAIC", "PDCA", "PDSA"],                                   │
│           index=0                                                       │
│       )                                                                 │
│                                                                         │
│   with col_method2:                                                     │
│       st.markdown(f"### {icon} {methodology}")                         │
│                                                                         │
│   # ... methodology info expander ...                                  │
│   # ==================== END METHODOLOGY ====================          │
│                                                                         │
│   st.write("---")                                                       │
│   st.write("### 2. Mô tả dự án")                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
"""


# ==================== QUICK CHECKLIST ====================
"""
□ STEP 1: Copy SNIPPET 1 → Paste sau dòng budget trong render_add_project()

□ STEP 2: Copy SNIPPET 2 → Add 'methodology': methodology vào project_data

□ STEP 3: Copy SNIPPET 3 → Paste sau dropdown category trong render_project_info()

□ STEP 4: Copy SNIPPET 4 → Add 'methodology': methodology vào updated_data

□ STEP 5: Save file

□ STEP 6: Git commit & push

□ STEP 7: Test!
"""


# ==================== COMPLETE EXAMPLE ====================
# Đây là VÍ DỤ HOÀN CHỈNH của render_add_project() sau khi thêm code:

def render_add_project_EXAMPLE():
    """Complete example - FOR REFERENCE ONLY"""
    st.subheader("➕ Thêm Dự Án Mới")
    
    with st.form("add_project_form"):
        st.write("### 1. Thông tin chung")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Generate project code
            all_projects = db.get_all_projects()
            if len(all_projects) > 0:
                last_code = all_projects['project_code'].iloc[0]
                try:
                    num = int(last_code.split('-')[2]) + 1
                    project_code = f"LSS-2024-{num:03d}"
                except:
                    project_code = "LSS-2024-001"
            else:
                project_code = "LSS-2024-001"
            
            project_code = st.text_input("Mã dự án *", value=project_code)
            project_name = st.text_input("Tên dự án *")
            
            departments = db.get_departments()
            dept_list = departments['name'].tolist() if not departments.empty else []
            department = st.selectbox("Phòng/Ban *", dept_list)
            
            category = st.selectbox("Danh mục *", LEAN_CATEGORIES)
        
        with col2:
            status = st.selectbox("Trạng thái *", PROJECT_STATUS)
            start_date = st.date_input("Ngày bắt đầu *", value=date.today())
            end_date = st.date_input("Ngày kết thúc *", value=date.today())
            budget = st.number_input("Ngân sách (VNĐ)", min_value=0, value=0)
        
        # ⬇️⬇️⬇️ SNIPPET 1 STARTS HERE ⬇️⬇️⬇️
        st.write("---")
        st.write("### 🔧 Phương pháp Cải tiến")
        
        col_method1, col_method2 = st.columns([3, 1])
        
        with col_method1:
            methodology = st.selectbox(
                "Chọn Methodology *",
                ["DMAIC", "PDCA", "PDSA"],
                index=0,
                help="Chọn phương pháp cải tiến phù hợp"
            )
        
        with col_method2:
            methodology_icons = {
                'DMAIC': '🔵',
                'PDCA': '🟢',
                'PDSA': '🟡'
            }
            st.markdown(f"### {methodology_icons.get(methodology, '⚪')} {methodology}")
        
        methodology_info = {
            'DMAIC': {
                'name': 'DMAIC - Six Sigma',
                'phases': '5 phases: Define → Measure → Analyze → Improve → Control',
                'best_for': '✅ Dự án phức tạp, cần phân tích dữ liệu chi tiết'
            },
            'PDCA': {
                'name': 'PDCA - Deming Cycle',
                'phases': '4 phases: Plan → Do → Check → Act',
                'best_for': '✅ Cải tiến quy trình, tiêu chuẩn hóa'
            },
            'PDSA': {
                'name': 'PDSA - Quality Improvement',
                'phases': '4 phases: Plan → Do → Study → Act',
                'best_for': '✅ Đổi mới sáng tạo, học hỏi từ thử nghiệm'
            }
        }
        
        info = methodology_info[methodology]
        
        with st.expander(f"ℹ️ Tìm hiểu về {methodology}"):
            st.write(f"**{info['name']}**")
            st.write(f"📊 {info['phases']}")
            st.write(f"{info['best_for']}")
        # ⬆️⬆️⬆️ SNIPPET 1 ENDS HERE ⬆️⬆️⬆️
        
        st.write("---")
        st.write("### 2. Mô tả dự án")
        
        description = st.text_area("Mô tả chung", placeholder="Mô tả ngắn gọn về dự án")
        problem_statement = st.text_area("Mô tả vấn đề", placeholder="Vấn đề cần giải quyết")
        goal = st.text_area("Mục tiêu", placeholder="Mục tiêu của dự án")
        scope = st.text_area("Phạm vi dự án", placeholder="Phạm vi và giới hạn của dự án")
        
        submitted = st.form_submit_button("💾 Lưu dự án", type="primary")
        
        if submitted:
            if not project_code or not project_name or not department or not category:
                st.error("⚠️ Vui lòng điền đầy đủ các trường bắt buộc (*)")
            else:
                try:
                    # ⬇️⬇️⬇️ SNIPPET 2 IS HERE ⬇️⬇️⬇️
                    project_data = {
                        'project_code': project_code,
                        'project_name': project_name,
                        'department': department,
                        'category': category,
                        'status': status,
                        'start_date': str(start_date),
                        'end_date': str(end_date),
                        'budget': budget,
                        'methodology': methodology,  # ⬅️ SNIPPET 2
                        'description': description,
                        'problem_statement': problem_statement,
                        'goal': goal,
                        'scope': scope,
                        'actual_cost': 0
                    }
                    # ⬆️⬆️⬆️ SNIPPET 2 ENDS HERE ⬆️⬆️⬆️
                    
                    project_id = db.add_project(project_data)
                    st.success(f"✅ Đã tạo dự án {project_code} với phương pháp {methodology}!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Lỗi khi tạo dự án: {str(e)}")


# ==================== END OF SNIPPETS ====================
"""
Hướng dẫn sử dụng:

1. Copy SNIPPET 1 → Paste vào app.py
2. Copy SNIPPET 2 → Add vào project_data
3. Copy SNIPPET 3 → Paste vào render_project_info()
4. Copy SNIPPET 4 → Add vào updated_data
5. Save, commit, push!

Đơn giản vậy thôi! 💪
"""

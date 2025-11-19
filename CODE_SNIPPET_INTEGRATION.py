# ========================================
# CODE SNIPPET ĐỂ THÊM VÀO APP.PY
# ========================================

# 1. THÊM VÀO ĐẦU FILE (sau các import khác)
# ------------------------------------------
from dmaic_tools import DMAICTools

# 2. CẬP NHẬT FORM TẠO DỰ ÁN MỚI
# ------------------------------------------
# Tìm phần tạo dự án mới, thêm field methodology:

methodology = st.selectbox(
    "Phương pháp cải tiến *",
    ["DMAIC", "PDCA", "PDSA"],
    help="Chọn phương pháp Lean Six Sigma sử dụng cho dự án này"
)

# Khi lưu project_data, thêm:
project_data = {
    'project_code': project_code,
    'project_name': project_name,
    'methodology': methodology,  # <-- THÊM DÒNG NÀY
    'department': department,
    ...
}

# 3. CẬP NHẬT CHI TIẾT DỰ ÁN
# ------------------------------------------
# Tìm phần hiển thị chi tiết dự án (function hoặc section show project details)
# Tìm dòng tạo tabs, sửa lại như sau:

# TRƯỚC:
# project_tabs = st.tabs(["📊 Thông tin chung", "👥 Team", "📅 Kế hoạch", "✍️ Ký tên"])

# SAU:
project_tabs = st.tabs([
    "📊 Thông tin chung", 
    "👥 Team & Stakeholders", 
    "📅 Kế hoạch", 
    "✍️ Ký tên",
    "🔄 DMAIC Tracking",  # MỚI
    "📄 Tài liệu",
    "💬 Cộng tác"
])

# Thêm tab mới cho DMAIC:
with project_tabs[4]:  # Tab DMAIC Tracking
    if project_info.get('methodology') == 'DMAIC':
        dmaic_tools = DMAICTools(db)
        dmaic_tools.render_dmaic_tracker(selected_project, project_info)
    elif project_info.get('methodology') == 'PDCA':
        st.info("🔄 PDCA tracking sẽ có sẵn trong phiên bản tiếp theo")
    elif project_info.get('methodology') == 'PDSA':
        st.info("🔄 PDSA tracking sẽ có sẵn trong phiên bản tiếp theo")
    else:
        st.warning("Vui lòng chọn phương pháp cải tiến cho dự án")

with project_tabs[5]:  # Tab Tài liệu (placeholder)
    st.info("📄 Quản lý tài liệu sẽ có sẵn trong phiên bản tiếp theo")

with project_tabs[6]:  # Tab Cộng tác (placeholder)
    st.info("💬 Tính năng cộng tác sẽ có sẵn trong phiên bản tiếp theo")

# 4. CẬP NHẬT BẢNG HIỂN THI DỰ ÁN
# ------------------------------------------
# Tìm nơi hiển thị bảng danh sách dự án
# Thêm cột Methodology:

# Nếu dùng st.dataframe:
display_columns = [
    'project_code', 
    'project_name', 
    'methodology',  # <-- THÊM DÒNG NÀY
    'department', 
    'status', 
    'category',
    'start_date', 
    'end_date'
]

# 5. HIỂN THỊ METHODOLOGY BADGE
# ------------------------------------------
# Trong phần hiển thị thông tin dự án, thêm:

methodology_colors = {
    'DMAIC': '🔵',
    'PDCA': '🟢', 
    'PDSA': '🟡'
}

methodology = project_info.get('methodology', 'DMAIC')
st.write(f"{methodology_colors.get(methodology, '⚪')} **Phương pháp:** {methodology}")

# 6. FILTER THEO METHODOLOGY (Optional)
# ------------------------------------------
# Trong sidebar hoặc filter section:

methodology_filter = st.multiselect(
    "Lọc theo phương pháp",
    options=['DMAIC', 'PDCA', 'PDSA'],
    default=['DMAIC', 'PDCA', 'PDSA']
)

# Khi filter projects:
if methodology_filter:
    projects_df = projects_df[projects_df['methodology'].isin(methodology_filter)]

# ========================================
# VÍ DỤ HOÀN CHỈNH: SECTION QUẢN LÝ DỰ ÁN
# ========================================

def render_project_management():
    st.header("📋 Quản lý Dự án")
    
    # Load projects
    projects_df = db.get_all_projects()
    
    if len(projects_df) > 0:
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.multiselect(
                "Trạng thái",
                options=projects_df['status'].unique(),
                default=projects_df['status'].unique()
            )
        with col2:
            dept_filter = st.multiselect(
                "Phòng ban",
                options=projects_df['department'].unique(),
                default=projects_df['department'].unique()
            )
        with col3:
            method_filter = st.multiselect(
                "Phương pháp",
                options=['DMAIC', 'PDCA', 'PDSA'],
                default=['DMAIC', 'PDCA', 'PDSA']
            )
        
        # Apply filters
        filtered_df = projects_df[
            (projects_df['status'].isin(status_filter)) &
            (projects_df['department'].isin(dept_filter)) &
            (projects_df['methodology'].isin(method_filter))
        ]
        
        # Display
        st.dataframe(filtered_df[['project_code', 'project_name', 'methodology', 
                                  'department', 'status', 'start_date']], 
                    use_container_width=True)
        
        # Project selection
        selected_code = st.selectbox(
            "Chọn dự án để xem chi tiết",
            options=filtered_df['project_code'].tolist()
        )
        
        if selected_code:
            project_row = filtered_df[filtered_df['project_code'] == selected_code].iloc[0]
            project_id = project_row['id']
            
            # Project tabs
            tabs = st.tabs([
                "📊 Thông tin", 
                "👥 Team", 
                "📅 Kế hoạch", 
                "✍️ Ký tên",
                "🔄 DMAIC",  # NEW
                "📄 Docs",    # NEW
                "💬 Collab"   # NEW
            ])
            
            with tabs[0]:
                render_project_info(project_id, project_row)
            
            with tabs[1]:
                render_team_stakeholders(project_id)
            
            with tabs[2]:
                render_project_plan(project_id)
            
            with tabs[3]:
                render_signoffs(project_id)
            
            with tabs[4]:  # DMAIC
                if project_row['methodology'] == 'DMAIC':
                    dmaic_tools = DMAICTools(db)
                    dmaic_tools.render_dmaic_tracker(project_id, project_row.to_dict())
                else:
                    st.info(f"Dự án này sử dụng phương pháp {project_row['methodology']}")
            
            with tabs[5]:  # Documents
                st.info("📄 Coming soon")
            
            with tabs[6]:  # Collaboration
                st.info("💬 Coming soon")
    else:
        st.info("Chưa có dự án nào")

# ========================================
# NOTES
# ========================================

# - Các function như render_project_info, render_team_stakeholders, etc. 
#   là các function đã có sẵn trong app.py hiện tại
# - Chỉ cần thêm import DMAICTools và gọi render_dmaic_tracker
# - Database đã có field methodology, sẽ tự động = 'DMAIC' cho dự án cũ
# - Không cần migrate data cũ

# ========================================
# END OF CODE SNIPPET
# ========================================

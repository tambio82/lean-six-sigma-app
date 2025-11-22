import streamlit as st
import pandas as pd
from datetime import datetime, date
import io
import json
import tempfile
import os

# Import các modules
from database import ProjectDatabase
from dmaic_tools import DMAICTools  # ← THÊM MỚI
from collaboration import render_collaboration_tab, initialize_collaboration  # ← COLLABORATION
from gantt_chart import (
    create_gantt_chart, create_dmaic_gantt, 
    get_project_progress, get_phase_summary, 
    check_overdue_tasks
)
from export_pdf import create_project_pdf
from dashboard import (
    create_status_chart, create_category_chart, 
    create_department_chart, create_budget_chart,
    create_overview_dashboard, create_metrics_cards,
    create_heatmap, create_funnel_chart
)

# Cấu hình trang
st.set_page_config(
    page_title="Quản lý Dự án Lean Six Sigma",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f4788;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #2e5c8a;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f4788;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Khởi tạo database
def init_db():
    return ProjectDatabase()

db = init_db()

# Danh mục dự án Lean
LEAN_CATEGORIES = [
    "(1) An toàn người bệnh",
    "(2) Hướng đến Hài lòng cho người bệnh",
    "(3) Hướng đến hài lòng cho nhân viên",
    "(4) Nâng cao chất lượng chuyên môn",
    "(5) Bệnh viện thông minh"
]

# Trạng thái dự án
PROJECT_STATUS = [
    "Lên kế hoạch",
    "Đang thực hiện",
    "Tạm dừng",
    "Hoàn thành",
    "Hủy bỏ"
]

# DMAIC Phases
DMAIC_PHASES = ["Define", "Measure", "Analyze", "Improve", "Control"]

# ==================== SIDEBAR ====================
def render_sidebar():
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80/1f4788/FFFFFF?text=Lean+Six+Sigma", width=200)
        
        st.markdown("---")
        
        menu = st.radio(
            "📋 MENU CHÍNH",
            [
                "🏠 Trang chủ",
                "➕ Thêm dự án mới",
                "📝 Quản lý dự án",
                "📊 Dashboard & Thống kê",
                "🏢 Quản lý Phòng/Ban",
                "📤 Import/Export",
                "❓ Hướng dẫn sử dụng"
            ]
        )
        
        st.markdown("---")
        st.info("💡 **Gợi ý**: Sử dụng menu bên trái để điều hướng")
        
        return menu

# ==================== TRANG CHỦ ====================
def render_home():
    st.markdown('<h1 class="main-header">🏥 HỆ THỐNG QUẢN LÝ DỰ ÁN LEAN SIX SIGMA</h1>', unsafe_allow_html=True)
    
    # Thống kê tổng quan
    stats = db.get_statistics()
    metrics = create_metrics_cards(stats)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📁 Tổng số dự án",
            value=metrics['total_projects']
        )
    
    with col2:
        st.metric(
            label="💰 Tổng ngân sách",
            value=f"{metrics['total_budget']:,.0f} VNĐ"
        )
    
    with col3:
        st.metric(
            label="💸 Tổng chi phí",
            value=f"{metrics['total_cost']:,.0f} VNĐ"
        )
    
    with col4:
        st.metric(
            label="📊 Tỷ lệ sử dụng ngân sách",
            value=f"{metrics['budget_utilization']}%"
        )
    
    st.markdown("---")
    
    # Danh sách dự án gần đây
    st.subheader("📋 Dự án gần đây")
    
    projects = db.get_all_projects()
    
    if not projects.empty:
        # Hiển thị top 10 dự án mới nhất
        recent_projects = projects.head(10)
        
        display_df = recent_projects[['project_code', 'project_name', 'methodology', 'department', 
                                       'category', 'status', 'start_date', 'end_date']]
        display_df.columns = ['Mã dự án', 'Tên dự án', 'Phương pháp', 'Phòng/Ban', 
                              'Danh mục', 'Trạng thái', 'Ngày bắt đầu', 'Ngày kết thúc']
        
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("Chưa có dự án nào. Hãy thêm dự án mới!")

# ==================== THÊM DỰ ÁN MỚI ====================
def render_add_project():
    st.header("➕ Thêm Dự án Mới")
    
    with st.form("add_project_form"):
        st.subheader("1. Thông tin chung")
        
        col1, col2 = st.columns(2)
        
        with col1:
            project_code = st.text_input("Mã dự án *", placeholder="LSS-2024-001")
            project_name = st.text_input("Tên dự án *", placeholder="Tên dự án")
            
            # Lấy danh sách phòng ban
            departments = db.get_departments()
            dept_list = [""] + departments['name'].tolist() if not departments.empty else [""]
            
            department = st.selectbox("Phòng/Ban *", dept_list)
            category = st.selectbox("Danh mục *", [""] + LEAN_CATEGORIES)
        
        with col2:
            # ← THÊM MỚI: Methodology selector
            methodology = st.selectbox(
                "Phương pháp cải tiến *",
                ["DMAIC", "PDCA", "PDSA"],
                index=0,
                help="Chọn phương pháp Lean Six Sigma cho dự án này"
            )
            
            status = st.selectbox("Trạng thái *", PROJECT_STATUS)
            start_date = st.date_input("Ngày bắt đầu *")
            end_date = st.date_input("Ngày kết thúc *")
            budget = st.number_input("Ngân sách (VNĐ)", min_value=0, value=0, step=1000000)
        
        st.subheader("2. Mô tả dự án")
        
        description = st.text_area("Mô tả chung", placeholder="Mô tả ngắn gọn về dự án")
        problem_statement = st.text_area("Mô tả vấn đề", placeholder="Vấn đề cần giải quyết")
        goal = st.text_area("Mục tiêu", placeholder="Mục tiêu của dự án")
        scope = st.text_area("Phạm vi dự án", placeholder="Phạm vi và giới hạn của dự án")
        
        submitted = st.form_submit_button("💾 Lưu dự án", type="primary")
        
        if submitted:
            if not project_code or not project_name or not department or not category:
                st.error("⚠️ Vui lòng điền đầy đủ các trường bắt buộc (*)")
            else:
                project_data = {
                    'project_code': project_code,
                    'project_name': project_name,
                    'department': department,
                    'category': category,
                    'methodology': methodology,  # ← THÊM MỚI
                    'status': status,
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'budget': budget,
                    'actual_cost': 0,
                    'description': description,
                    'problem_statement': problem_statement,
                    'goal': goal,
                    'scope': scope
                }
                
                try:
                    project_id = db.add_project(project_data)
                    st.success(f"✅ Đã thêm dự án thành công! ID: {project_id}")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Lỗi: {str(e)}")

# ==================== QUẢN LÝ DỰ ÁN ====================
def render_manage_projects():
    st.header("📝 Quản lý Dự án")
    
    projects = db.get_all_projects()
    
    if projects.empty:
        st.warning("Chưa có dự án nào. Hãy thêm dự án mới!")
        return
    
    # Chọn dự án
    project_options = {f"{row['project_code']} - {row['project_name']}": row['id'] 
                       for _, row in projects.iterrows()}
    
    selected_project_name = st.selectbox(
        "Chọn dự án để quản lý:",
        options=list(project_options.keys())
    )
    
    if selected_project_name:
        project_id = project_options[selected_project_name]
        project = db.get_project(project_id)
        
        if project:
            # ← TABS MỚI: Thêm DMAIC Tracking
            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
                "📄 Thông tin", 
                "👥 Thành viên", 
                "🤝 Stakeholders",
                "📅 Kế hoạch (Gantt)",
                "🔄 DMAIC Tracking",  # Tab 5 - DMAIC
                "💬 Cộng tác",  # Tab 6 - COLLABORATION (NEW!)
                "✍️ Ký tên",  # Tab 7 (was tab6)
                "📤 Xuất báo cáo"  # Tab 8 (was tab7)
            ])
            
            # Tab 1: Thông tin dự án
            with tab1:
                render_project_info(project_id, project)
            
            # Tab 2: Thành viên
            with tab2:
                render_team_members(project_id)
            
            # Tab 3: Stakeholders
            with tab3:
                render_stakeholders(project_id)
            
            # Tab 4: Kế hoạch Gantt
            with tab4:
                render_gantt_plan(project_id)
            
            # Tab 5: DMAIC TRACKING
            with tab5:
                render_dmaic_tracking(project_id, project)
            
            # Tab 6: CỘNG TÁC (NEW!)
            with tab6:
                current_user = st.session_state.get('user_name', 'Current User')
                render_collaboration_tab(
                    project_id=project_id,
                    project=project,
                    database=db,
                    current_user=current_user
                )
            
            # Tab 7: Ký tên (was tab6)
            with tab7:
                render_signoffs(project_id)
            
            # Tab 8: Xuất báo cáo (was tab7)
            with tab8:
                render_export_report(project_id, project)

# ← FUNCTION MỚI: Render DMAIC Tracking
def render_dmaic_tracking(project_id, project):
    """Render DMAIC methodology tracking interface"""
    methodology = project.get('methodology', 'DMAIC')
    
    # Hiển thị methodology badge
    methodology_icons = {
        'DMAIC': '🔵',
        'PDCA': '🟢',
        'PDSA': '🟡'
    }
    
    st.write(f"{methodology_icons.get(methodology, '⚪')} **Phương pháp:** {methodology}")
    
    if methodology == 'DMAIC':
        # Render DMAIC tools
        dmaic_tools = DMAICTools(db)
        dmaic_tools.render_dmaic_tracker(project_id, project)
    
    elif methodology == 'PDCA':
        st.info("🔄 **PDCA Tracking**")
        st.write("**Plan → Do → Check → Act**")
        st.write("Tính năng PDCA tracking sẽ có sẵn trong phiên bản tiếp theo.")
        st.write("")
        st.write("Hiện tại bạn có thể sử dụng tab **Kế hoạch (Gantt)** để theo dõi tiến độ.")
    
    elif methodology == 'PDSA':
        st.info("🔄 **PDSA Tracking**")
        st.write("**Plan → Do → Study → Act**")
        st.write("Tính năng PDSA tracking sẽ có sẵn trong phiên bản tiếp theo.")
        st.write("")
        st.write("Hiện tại bạn có thể sử dụng tab **Kế hoạch (Gantt)** để theo dõi tiến độ.")
    
    else:
        st.warning("Vui lòng chọn phương pháp cải tiến cho dự án trong tab **Thông tin**")

def render_project_info(project_id, project):
    st.subheader("Thông tin Dự án")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form(f"edit_project_{project_id}"):
            project_name = st.text_input("Tên dự án", value=project.get('project_name', ''))
            
            departments = db.get_departments()
            dept_list = departments['name'].tolist() if not departments.empty else []
            current_dept = project.get('department', '')
            dept_index = dept_list.index(current_dept) if current_dept in dept_list else 0
            
            department = st.selectbox("Phòng/Ban", dept_list, index=dept_index)
            
            current_cat = project.get('category', '')
            cat_index = LEAN_CATEGORIES.index(current_cat) if current_cat in LEAN_CATEGORIES else 0
            category = st.selectbox("Danh mục", LEAN_CATEGORIES, index=cat_index)
            
            # ← THÊM MỚI: Methodology selector trong edit form
            methodology_list = ["DMAIC", "PDCA", "PDSA"]
            current_methodology = project.get('methodology', 'DMAIC')
            methodology_index = methodology_list.index(current_methodology) if current_methodology in methodology_list else 0
            methodology = st.selectbox("Phương pháp cải tiến", methodology_list, index=methodology_index)
            
            current_status = project.get('status', 'Lên kế hoạch')
            status_index = PROJECT_STATUS.index(current_status) if current_status in PROJECT_STATUS else 0
            status = st.selectbox("Trạng thái", PROJECT_STATUS, index=status_index)
            
            col_a, col_b = st.columns(2)
            with col_a:
                start_date = st.date_input("Ngày bắt đầu", 
                    value=pd.to_datetime(project.get('start_date')).date() if project.get('start_date') else date.today())
            with col_b:
                end_date = st.date_input("Ngày kết thúc",
                    value=pd.to_datetime(project.get('end_date')).date() if project.get('end_date') else date.today())
            
            budget = st.number_input("Ngân sách (VNĐ)", value=int(project.get('budget', 0)), step=1000000)
            actual_cost = st.number_input("Chi phí thực tế (VNĐ)", value=int(project.get('actual_cost', 0)), step=1000000)
            
            description = st.text_area("Mô tả", value=project.get('description', ''))
            problem_statement = st.text_area("Mô tả vấn đề", value=project.get('problem_statement', ''))
            goal = st.text_area("Mục tiêu", value=project.get('goal', ''))
            scope = st.text_area("Phạm vi", value=project.get('scope', ''))
            
            col_save, col_delete = st.columns([3, 1])
            
            with col_save:
                submitted = st.form_submit_button("💾 Cập nhật", type="primary")
            
            with col_delete:
                delete = st.form_submit_button("🗑️ Xóa", type="secondary")
            
            if submitted:
                update_data = {
                    'project_name': project_name,
                    'department': department,
                    'category': category,
                    'methodology': methodology,  # ← THÊM MỚI
                    'status': status,
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'budget': budget,
                    'actual_cost': actual_cost,
                    'description': description,
                    'problem_statement': problem_statement,
                    'goal': goal,
                    'scope': scope
                }
                
                db.update_project(project_id, update_data)
                st.success("✅ Đã cập nhật thông tin dự án!")
                st.rerun()
            
            if delete:
                if st.session_state.get(f'confirm_delete_{project_id}'):
                    db.delete_project(project_id)
                    st.success("✅ Đã xóa dự án!")
                    st.rerun()
                else:
                    st.session_state[f'confirm_delete_{project_id}'] = True
                    st.warning("⚠️ Nhấn lại nút Xóa để xác nhận!")
    
    with col2:
        # ← HIỂN THỊ METHODOLOGY
        methodology_icons = {
            'DMAIC': '🔵',
            'PDCA': '🟢',
            'PDSA': '🟡'
        }
        methodology = project.get('methodology', 'DMAIC')
        
        st.info(f"""
        **Mã dự án:** {project.get('project_code', 'N/A')}
        
        {methodology_icons.get(methodology, '⚪')} **Phương pháp:** {methodology}
        
        **Ngày tạo:** {pd.to_datetime(project.get('created_at')).strftime('%d/%m/%Y %H:%M') if project.get('created_at') else 'N/A'}
        
        **Cập nhật lần cuối:** {pd.to_datetime(project.get('updated_at')).strftime('%d/%m/%Y %H:%M') if project.get('updated_at') else 'N/A'}
        """)

def render_team_members(project_id):
    st.subheader("Danh sách Thành viên")
    
    members = db.get_team_members(project_id)
    
    # Hiển thị danh sách
    if not members.empty:
        for _, member in members.iterrows():
            with st.expander(f"👤 {member['name']} - {member.get('role', 'N/A')}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Vai trò:** {member.get('role', 'N/A')}")
                    st.write(f"**Phòng/Ban:** {member.get('department', 'N/A')}")
                    st.write(f"**Email:** {member.get('email', 'N/A')}")
                    st.write(f"**Điện thoại:** {member.get('phone', 'N/A')}")
                
                with col2:
                    if st.button("🗑️ Xóa", key=f"del_member_{member['id']}"):
                        db.delete_team_member(member['id'])
                        st.success("✅ Đã xóa thành viên!")
                        st.rerun()
    else:
        st.info("Chưa có thành viên nào.")
    
    # Form thêm thành viên mới
    st.markdown("---")
    st.subheader("➕ Thêm thành viên mới")
    
    with st.form(f"add_member_{project_id}"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Họ tên *")
            role = st.text_input("Vai trò *", placeholder="VD: Trưởng nhóm, Thành viên...")
        
        with col2:
            departments = db.get_departments()
            dept_list = [""] + departments['name'].tolist() if not departments.empty else [""]
            department = st.selectbox("Phòng/Ban", dept_list)
            
            email = st.text_input("Email")
        
        phone = st.text_input("Điện thoại")
        
        submitted = st.form_submit_button("💾 Thêm thành viên", type="primary")
        
        if submitted:
            if not name or not role:
                st.error("⚠️ Vui lòng điền họ tên và vai trò!")
            else:
                member_data = {
                    'project_id': project_id,
                    'name': name,
                    'role': role,
                    'department': department,
                    'email': email,
                    'phone': phone
                }
                
                db.add_team_member(member_data)
                st.success("✅ Đã thêm thành viên!")
                st.rerun()

def render_stakeholders(project_id):
    st.subheader("Danh sách Stakeholders")
    
    stakeholders = db.get_stakeholders(project_id)
    
    # Hiển thị danh sách
    if not stakeholders.empty:
        for _, stake in stakeholders.iterrows():
            with st.expander(f"🤝 {stake['name']} - {stake.get('role', 'N/A')}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Vai trò:** {stake.get('role', 'N/A')}")
                    st.write(f"**Phòng/Ban:** {stake.get('department', 'N/A')}")
                    st.write(f"**Mức độ ảnh hưởng:** {stake.get('impact_level', 'N/A')}")
                    st.write(f"**Mức độ tham gia:** {stake.get('engagement_level', 'N/A')}")
                
                with col2:
                    if st.button("🗑️ Xóa", key=f"del_stake_{stake['id']}"):
                        db.delete_stakeholder(stake['id'])
                        st.success("✅ Đã xóa stakeholder!")
                        st.rerun()
    else:
        st.info("Chưa có stakeholder nào.")
    
    # Form thêm stakeholder mới
    st.markdown("---")
    st.subheader("➕ Thêm Stakeholder mới")
    
    with st.form(f"add_stake_{project_id}"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Họ tên *")
            role = st.text_input("Vai trò *")
            
            departments = db.get_departments()
            dept_list = [""] + departments['name'].tolist() if not departments.empty else [""]
            department = st.selectbox("Phòng/Ban", dept_list)
        
        with col2:
            impact_level = st.selectbox("Mức độ ảnh hưởng", 
                ["", "Thấp", "Trung bình", "Cao", "Rất cao"])
            engagement_level = st.selectbox("Mức độ tham gia",
                ["", "Ít", "Vừa phải", "Tích cực", "Rất tích cực"])
        
        submitted = st.form_submit_button("💾 Thêm Stakeholder", type="primary")
        
        if submitted:
            if not name or not role:
                st.error("⚠️ Vui lòng điền họ tên và vai trò!")
            else:
                stake_data = {
                    'project_id': project_id,
                    'name': name,
                    'role': role,
                    'department': department,
                    'impact_level': impact_level,
                    'engagement_level': engagement_level
                }
                
                db.add_stakeholder(stake_data)
                st.success("✅ Đã thêm stakeholder!")
                st.rerun()

def render_gantt_plan(project_id):
    st.subheader("📅 Kế hoạch Chi tiết - Gantt Chart")
    
    # ← LẤY METHODOLOGY TỪ PROJECT
    project = db.get_project(project_id)
    methodology = project.get('methodology', 'DMAIC') if project else 'DMAIC'
    
    # ← DEFINE PHASES CHO TỪNG METHODOLOGY
    METHODOLOGY_PHASES = {
        'DMAIC': ["Define", "Measure", "Analyze", "Improve", "Control"],
        'PDCA': ["Plan", "Do", "Check", "Act"],
        'PDSA': ["Plan", "Do", "Study", "Act"]
    }
    
    phases = METHODOLOGY_PHASES.get(methodology, METHODOLOGY_PHASES['DMAIC'])
    
    # ← HIỂN THỊ METHODOLOGY HIỆN TẠI
    methodology_icons = {
        'DMAIC': '🔵',
        'PDCA': '🟢',
        'PDSA': '🟡'
    }
    st.info(f"{methodology_icons.get(methodology, '⚪')} **Phương pháp:** {methodology} ({len(phases)} phases)")
    
    tasks = db.get_tasks(project_id)
    
    # Hiển thị Gantt Chart
    if not tasks.empty:
        # Tiến độ tổng thể
        progress = get_project_progress(tasks)
        st.metric("Tiến độ tổng thể", f"{progress}%")
        
        # Chọn loại biểu đồ
        chart_type = st.radio("Chọn kiểu hiển thị:", 
            ["Gantt Chart cơ bản", "DMAIC Gantt"], horizontal=True)
        
        if chart_type == "DMAIC Gantt" and methodology == 'DMAIC':
            fig = create_dmaic_gantt(tasks)
        else:
            fig = create_gantt_chart(tasks)
        
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Tóm tắt theo phase
        st.subheader("📊 Tóm tắt theo Phase")
        phase_summary = get_phase_summary(tasks)
        if not phase_summary.empty:
            st.dataframe(phase_summary, use_container_width=True)
        
        # Tasks quá hạn
        overdue = check_overdue_tasks(tasks)
        if not overdue.empty:
            st.warning(f"⚠️ Có {len(overdue)} công việc quá hạn!")
            st.dataframe(overdue, use_container_width=True)
        
        # Danh sách tasks
        st.markdown("---")
        st.subheader("Danh sách công việc")
        
        display_tasks = tasks[['phase', 'task_name', 'start_date', 'end_date', 
                                'responsible', 'status', 'progress']]
        display_tasks.columns = ['Phase', 'Công việc', 'Ngày bắt đầu', 'Ngày kết thúc',
                                  'Người phụ trách', 'Trạng thái', 'Tiến độ (%)']
        
        st.dataframe(display_tasks, use_container_width=True)
        
    else:
        st.info("Chưa có kế hoạch chi tiết.")
    
    # ← FORM THÊM TASK MỚI (DYNAMIC PHASES)
    st.markdown("---")
    st.subheader("➕ Thêm công việc mới")
    
    with st.form(f"add_task_{project_id}"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # ← DYNAMIC PHASE DROPDOWN
            phase = st.selectbox(
                "Phase *", 
                phases,
                help=f"Chọn phase theo phương pháp {methodology}"
            )
            task_name = st.text_input("Tên công việc *")
        
        with col2:
            start_date = st.date_input("Ngày bắt đầu *")
            end_date = st.date_input("Ngày kết thúc *")
        
        with col3:
            responsible = st.text_input("Người phụ trách")
            status = st.selectbox("Trạng thái", 
                ["Chưa bắt đầu", "Đang thực hiện", "Hoàn thành", "Tạm dừng"])
            progress = st.slider("Tiến độ (%)", 0, 100, 0)
        
        submitted = st.form_submit_button("💾 Thêm công việc", type="primary")
        
        if submitted:
            if not task_name:
                st.error("⚠️ Vui lòng nhập tên công việc!")
            else:
                task_data = {
                    'project_id': project_id,
                    'phase': phase,
                    'task_name': task_name,
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'responsible': responsible,
                    'status': status,
                    'progress': progress
                }
                
                db.add_task(task_data)
                st.success("✅ Đã thêm công việc!")
                st.rerun()

def render_signoffs(project_id):
    st.subheader("✍️ Bảng Ký tên")
    
    signoffs = db.get_signoffs(project_id)
    
    # Hiển thị danh sách
    if not signoffs.empty:
        for _, sign in signoffs.iterrows():
            with st.expander(f"✍️ {sign['role']} - {sign.get('name', 'Chưa ký')}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Vai trò:** {sign.get('role', 'N/A')}")
                    st.write(f"**Người ký:** {sign.get('name', 'Chưa ký')}")
                    st.write(f"**Ngày ký:** {sign.get('date', 'N/A')}")
                    st.write(f"**Ghi chú:** {sign.get('notes', 'N/A')}")
                
                with col2:
                    if st.button("🗑️ Xóa", key=f"del_sign_{sign['id']}"):
                        db.delete_signoff(sign['id'])
                        st.success("✅ Đã xóa!")
                        st.rerun()
    else:
        st.info("Chưa có thông tin ký tên.")
    
    # Form thêm signoff
    st.markdown("---")
    st.subheader("➕ Thêm người ký")
    
    with st.form(f"add_signoff_{project_id}"):
        col1, col2 = st.columns(2)
        
        with col1:
            role = st.text_input("Vai trò/Chức vụ *", placeholder="VD: Trưởng khoa, Giám đốc...")
            name = st.text_input("Họ tên người ký")
        
        with col2:
            sign_date = st.date_input("Ngày ký")
            notes = st.text_area("Ghi chú")
        
        submitted = st.form_submit_button("💾 Thêm", type="primary")
        
        if submitted:
            if not role:
                st.error("⚠️ Vui lòng nhập vai trò/chức vụ!")
            else:
                signoff_data = {
                    'project_id': project_id,
                    'role': role,
                    'name': name,
                    'date': sign_date.isoformat(),
                    'notes': notes,
                    'signature': ''
                }
                
                db.add_signoff(signoff_data)
                st.success("✅ Đã thêm!")
                st.rerun()

def render_export_report(project_id, project):
    st.subheader("📤 Xuất Báo cáo")
    
    col1, col2, col3 = st.columns(3)
    
    # Xuất PDF
    with col1:
        if st.button("📄 Xuất PDF", type="primary"):
            with st.spinner("Đang tạo file PDF..."):
                try:
                    # Lấy dữ liệu
                    team_members = db.get_team_members(project_id)
                    stakeholders = db.get_stakeholders(project_id)
                    tasks = db.get_tasks(project_id)
                    signoffs = db.get_signoffs(project_id)
                    
                    # Tạo file PDF trong thư mục tạm
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        output_path = tmp_file.name
                    
                    create_project_pdf(project, team_members, stakeholders, 
                                       tasks, signoffs, output_path)
                    
                    # Đọc file và tạo download button
                    with open(output_path, 'rb') as f:
                        pdf_bytes = f.read()
                    
                    # Xóa file tạm
                    try:
                        os.remove(output_path)
                    except:
                        pass
                    
                    st.download_button(
                        label="⬇️ Tải xuống PDF",
                        data=pdf_bytes,
                        file_name=f"Project_{project['project_code']}.pdf",
                        mime="application/pdf"
                    )
                    
                    st.success("✅ Đã tạo file PDF!")
                    
                except Exception as e:
                    st.error(f"❌ Lỗi: {str(e)}")
    
    # Xuất Excel
    with col2:
        if st.button("📊 Xuất Excel", type="primary"):
            try:
                # Tạo Excel với nhiều sheets
                output = io.BytesIO()
                
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    # Sheet 1: Thông tin dự án
                    project_df = pd.DataFrame([project])
                    project_df.to_excel(writer, sheet_name='Thông tin dự án', index=False)
                    
                    # Sheet 2: Thành viên
                    team_members = db.get_team_members(project_id)
                    if not team_members.empty:
                        team_members.to_excel(writer, sheet_name='Thành viên', index=False)
                    
                    # Sheet 3: Stakeholders
                    stakeholders = db.get_stakeholders(project_id)
                    if not stakeholders.empty:
                        stakeholders.to_excel(writer, sheet_name='Stakeholders', index=False)
                    
                    # Sheet 4: Kế hoạch
                    tasks = db.get_tasks(project_id)
                    if not tasks.empty:
                        tasks.to_excel(writer, sheet_name='Kế hoạch', index=False)
                    
                    # Sheet 5: Ký tên
                    signoffs = db.get_signoffs(project_id)
                    if not signoffs.empty:
                        signoffs.to_excel(writer, sheet_name='Ký tên', index=False)
                
                excel_bytes = output.getvalue()
                
                st.download_button(
                    label="⬇️ Tải xuống Excel",
                    data=excel_bytes,
                    file_name=f"Project_{project['project_code']}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
                st.success("✅ Đã tạo file Excel!")
                
            except Exception as e:
                st.error(f"❌ Lỗi: {str(e)}")
    
    # Xuất CSV
    with col3:
        if st.button("📋 Xuất CSV", type="primary"):
            try:
                tasks = db.get_tasks(project_id)
                
                if not tasks.empty:
                    csv = tasks.to_csv(index=False)
                    
                    st.download_button(
                        label="⬇️ Tải xuống CSV",
                        data=csv,
                        file_name=f"Tasks_{project['project_code']}.csv",
                        mime="text/csv"
                    )
                    
                    st.success("✅ Đã tạo file CSV!")
                else:
                    st.warning("Không có dữ liệu để xuất")
                    
            except Exception as e:
                st.error(f"❌ Lỗi: {str(e)}")

# ==================== DASHBOARD ====================
def render_dashboard():
    st.header("📊 Dashboard & Thống kê")
    
    stats = db.get_statistics()
    projects = db.get_all_projects()
    
    if stats['total_projects'] == 0:
        st.warning("Chưa có dữ liệu để hiển thị dashboard.")
        return
    
    # Metrics cards
    metrics = create_metrics_cards(stats)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📁 Tổng số dự án", metrics['total_projects'])
    
    with col2:
        st.metric("💰 Tổng ngân sách", f"{metrics['total_budget']:,.0f} VNĐ")
    
    with col3:
        st.metric("💸 Chi phí thực tế", f"{metrics['total_cost']:,.0f} VNĐ")
    
    with col4:
        st.metric("📊 Tỷ lệ SD ngân sách", f"{metrics['budget_utilization']}%")
    
    st.markdown("---")
    
    # Chọn loại biểu đồ
    chart_options = st.multiselect(
        "Chọn biểu đồ hiển thị:",
        ["Trạng thái", "Danh mục", "Phòng/Ban", "Ngân sách", "Heatmap", "Timeline"],
        default=["Trạng thái", "Danh mục"]
    )
    
    # Hiển thị biểu đồ
    chart_cols = st.columns(2)
    
    chart_idx = 0
    for chart_type in chart_options:
        with chart_cols[chart_idx % 2]:
            if chart_type == "Trạng thái":
                fig = create_status_chart(stats, 'pie')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == "Danh mục":
                fig = create_category_chart(stats, 'bar')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == "Phòng/Ban":
                fig = create_department_chart(stats, 'bar')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == "Ngân sách":
                fig = create_budget_chart(stats)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == "Heatmap":
                if not projects.empty:
                    fig = create_heatmap(projects)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
        
        chart_idx += 1
    
    # Overview dashboard
    st.markdown("---")
    st.subheader("Dashboard Tổng quan")
    
    overview_fig = create_overview_dashboard(stats)
    if overview_fig:
        st.plotly_chart(overview_fig, use_container_width=True)

# ==================== QUẢN LÝ PHÒNG BAN ====================
def render_departments():
    st.header("🏢 Quản lý Phòng/Ban")
    
    departments = db.get_departments()
    
    # Hiển thị danh sách
    if not departments.empty:
        st.subheader("Danh sách Phòng/Ban")
        
        for _, dept in departments.iterrows():
            col1, col2, col3 = st.columns([3, 5, 1])
            
            with col1:
                st.write(f"**{dept['name']}**")
            
            with col2:
                st.write(dept.get('description', ''))
            
            with col3:
                if st.button("🗑️", key=f"del_dept_{dept['id']}"):
                    db.delete_department(dept['id'])
                    st.success("✅ Đã xóa!")
                    st.rerun()
    else:
        st.info("Chưa có phòng/ban nào.")
    
    # Form thêm phòng ban
    st.markdown("---")
    st.subheader("➕ Thêm Phòng/Ban mới")
    
    with st.form("add_department"):
        name = st.text_input("Tên Phòng/Ban *", placeholder="VD: Khoa Nội, Phòng Kế hoạch...")
        description = st.text_area("Mô tả", placeholder="Mô tả ngắn gọn về phòng/ban")
        
        submitted = st.form_submit_button("💾 Thêm", type="primary")
        
        if submitted:
            if not name:
                st.error("⚠️ Vui lòng nhập tên phòng/ban!")
            else:
                success = db.add_department(name, description)
                if success:
                    st.success("✅ Đã thêm phòng/ban!")
                    st.rerun()
                else:
                    st.error("❌ Phòng/ban đã tồn tại!")

# ==================== IMPORT/EXPORT ====================
def render_import_export():
    st.header("📤 Import/Export Dữ liệu")
    
    tab1, tab2 = st.tabs(["📥 Import", "📤 Export"])
    
    with tab1:
        st.subheader("Import dữ liệu từ Excel/CSV")
        
        uploaded_file = st.file_uploader(
            "Chọn file Excel hoặc CSV",
            type=['xlsx', 'xls', 'csv']
        )
        
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.write("Xem trước dữ liệu:")
                st.dataframe(df.head(), use_container_width=True)
                
                if st.button("✅ Import dữ liệu", type="primary"):
                    # TODO: Implement import logic
                    st.success("Chức năng đang phát triển!")
                    
            except Exception as e:
                st.error(f"❌ Lỗi đọc file: {str(e)}")
    
    with tab2:
        st.subheader("Export toàn bộ dữ liệu")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export tất cả dự án (Excel)", type="primary"):
                try:
                    projects = db.get_all_projects()
                    
                    if not projects.empty:
                        output = io.BytesIO()
                        projects.to_excel(output, index=False, engine='xlsxwriter')
                        excel_bytes = output.getvalue()
                        
                        st.download_button(
                            label="⬇️ Tải xuống",
                            data=excel_bytes,
                            file_name=f"All_Projects_{datetime.now().strftime('%Y%m%d')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        
                        st.success("✅ Đã tạo file!")
                    else:
                        st.warning("Không có dữ liệu để export")
                        
                except Exception as e:
                    st.error(f"❌ Lỗi: {str(e)}")
        
        with col2:
            if st.button("📋 Export tất cả dự án (CSV)", type="primary"):
                try:
                    projects = db.get_all_projects()
                    
                    if not projects.empty:
                        csv = projects.to_csv(index=False)
                        
                        st.download_button(
                            label="⬇️ Tải xuống",
                            data=csv,
                            file_name=f"All_Projects_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                        
                        st.success("✅ Đã tạo file!")
                    else:
                        st.warning("Không có dữ liệu để export")
                        
                except Exception as e:
                    st.error(f"❌ Lỗi: {str(e)}")

# ==================== HƯỚNG DẪN SỬ DỤNG ====================
def render_user_guide():
    st.header("❓ Hướng dẫn Sử dụng")
    
    st.markdown("""
    ## 📖 Hướng dẫn Sử dụng Hệ thống Quản lý Dự án Lean Six Sigma
    
    ### 1. 🏠 Trang chủ
    - Xem tổng quan thống kê các dự án
    - Hiển thị danh sách dự án gần đây
    
    ### 2. ➕ Thêm dự án mới
    - Nhập đầy đủ thông tin dự án theo form
    - **Chọn phương pháp cải tiến:** DMAIC, PDCA, hoặc PDSA
    - Các trường có dấu (*) là bắt buộc
    - Chọn danh mục theo 5 nhóm mục đích Lean Six Sigma
    
    ### 3. 📝 Quản lý dự án
    
    #### 📄 Thông tin dự án
    - Chỉnh sửa thông tin cơ bản
    - Cập nhật phương pháp cải tiến
    - Cập nhật ngân sách và chi phí thực tế
    - Xóa dự án (cần xác nhận 2 lần)
    
    #### 👥 Thành viên
    - Thêm/xóa thành viên trong nhóm dự án
    - Ghi rõ vai trò và thông tin liên hệ
    
    #### 🤝 Stakeholders
    - Quản lý các bên liên quan
    - Đánh giá mức độ ảnh hưởng và tham gia
    
    #### 📅 Kế hoạch (Gantt)
    - Tạo kế hoạch chi tiết theo DMAIC phases
    - Theo dõi tiến độ từng công việc
    - Xem biểu đồ Gantt trực quan
    - Cảnh báo công việc quá hạn
    
    #### 🔄 DMAIC Tracking **← MỚI!**
    - **DEFINE:** SIPOC Diagram, Project Charter, Voice of Customer
    - **MEASURE:** Data Collection, Baseline Metrics, Process Mapping
    - **ANALYZE:** Fishbone, 5 Whys, Pareto Chart, Statistical Analysis
    - **IMPROVE:** Solution Brainstorming, Pilot Testing, Before/After Comparison
    - **CONTROL:** Control Plans, SOPs, Sustainability Planning
    - *Lưu ý:* PDCA và PDSA tracking sẽ có trong phiên bản tiếp theo
    
    #### ✍️ Ký tên
    - Thêm thông tin người ký duyệt
    - Theo dõi trạng thái phê duyệt
    
    #### 📤 Xuất báo cáo
    - Xuất PDF: Báo cáo đầy đủ định dạng chuyên nghiệp
    - Xuất Excel: Dữ liệu chi tiết nhiều sheets
    - Xuất CSV: Dữ liệu kế hoạch để phân tích
    
    ### 4. 📊 Dashboard & Thống kê
    - Xem biểu đồ tổng quan
    - Chọn loại biểu đồ phù hợp (Pie, Bar, Heatmap...)
    - Phân tích theo nhiều tiêu chí
    
    ### 5. 🏢 Quản lý Phòng/Ban
    - Thêm danh sách các phòng/ban/khoa
    - Sử dụng cho dropdown trong các form khác
    
    ### 6. 📤 Import/Export
    - Import dữ liệu từ Excel/CSV (đang phát triển)
    - Export toàn bộ dữ liệu dự án
    
    ---
    
    ## 💡 Mẹo sử dụng
    
    1. **Tạo Phòng/Ban trước**: Nên tạo danh sách phòng/ban trước khi thêm dự án
    2. **Chọn Methodology:** Chọn đúng phương pháp (DMAIC/PDCA/PDSA) khi tạo dự án
    3. **DMAIC Tools:** Sử dụng tab DMAIC Tracking để ghi nhận chi tiết từng giai đoạn
    4. **Cập nhật tiến độ:** Thường xuyên cập nhật tiến độ để theo dõi dự án hiệu quả
    5. **Sao lưu dữ liệu:** Export dữ liệu định kỳ để backup
    
    ---
    
    ## 🆘 Hỗ trợ
    
    Nếu gặp vấn đề hoặc có câu hỏi, vui lòng liên hệ:
    - Email: support@hospital.com
    - Hotline: 0123-456-789
    """)

# ==================== MAIN APP ====================
def main():
    # Render sidebar và lấy menu đã chọn
    selected_menu = render_sidebar()
    
    # Initialize collaboration features
    if 'collaboration_initialized' not in st.session_state:
        collaboration_components = initialize_collaboration(db, enable_scheduler=False)
        st.session_state['collaboration_initialized'] = True
        st.session_state['collaboration_components'] = collaboration_components
    
    # Render nội dung theo menu
    if selected_menu == "🏠 Trang chủ":
        render_home()
    
    elif selected_menu == "➕ Thêm dự án mới":
        render_add_project()
    
    elif selected_menu == "📝 Quản lý dự án":
        render_manage_projects()
    
    elif selected_menu == "📊 Dashboard & Thống kê":
        render_dashboard()
    
    elif selected_menu == "🏢 Quản lý Phòng/Ban":
        render_departments()
    
    elif selected_menu == "📤 Import/Export":
        render_import_export()
    
    elif selected_menu == "❓ Hướng dẫn sử dụng":
        render_user_guide()

if __name__ == "__main__":
    main()

# ========================================
# GANTT CHART UPDATE - Multi-Methodology Support
# ========================================
# 
# Thay thế function render_gantt_plan() trong app.py
# ========================================

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
            # ← DYNAMIC PHASE DROPDOWN BASED ON METHODOLOGY
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


# ========================================
# CHANGES SUMMARY
# ========================================
"""
1. Lấy methodology từ project
2. Define phases cho DMAIC, PDCA, PDSA
3. Dynamic phase dropdown
4. Hiển thị methodology info
5. Conditional DMAIC Gantt (chỉ cho DMAIC)
"""

# ========================================
# USAGE INSTRUCTIONS
# ========================================
"""
1. Mở file app.py
2. Tìm function render_gantt_plan()
3. Thay thế toàn bộ function bằng code trên
4. Lưu và commit
5. Test với dự án DMAIC, PDCA, PDSA
"""

"""
PDCA/PDSA Tools Module
Complete tools for PDCA (Plan-Do-Check-Act) and PDSA (Plan-Do-Study-Act) methodologies
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json


class PDCATools:
    """
    Tools for PDCA/PDSA Methodology
    Supports both PDCA and PDSA with 4 phases each
    """
    
    def __init__(self, database):
        """Initialize PDCA tools with database connection"""
        self.db = database
    
    # ==================== MAIN RENDER METHOD ====================
    
    def render_pdca_interface(self, project_id: int, methodology: str = 'PDCA'):
        """
        Render complete PDCA/PDSA interface
        
        Args:
            project_id: Project ID
            methodology: 'PDCA' or 'PDSA'
        """
        st.subheader(f"🔄 {methodology} Tracking")
        
        # Phase selection tabs
        if methodology == 'PDCA':
            phase_tabs = st.tabs([
                "📋 Plan",
                "🛠️ Do", 
                "✅ Check",
                "🚀 Act"
            ])
            phases = ['Plan', 'Do', 'Check', 'Act']
        else:  # PDSA
            phase_tabs = st.tabs([
                "📋 Plan",
                "🛠️ Do",
                "📊 Study", 
                "🚀 Act"
            ])
            phases = ['Plan', 'Do', 'Study', 'Act']
        
        # Render each phase
        for idx, (tab, phase) in enumerate(zip(phase_tabs, phases)):
            with tab:
                self.render_phase(project_id, phase, methodology)
    
    def render_phase(self, project_id: int, phase: str, methodology: str):
        """Render specific PDCA/PDSA phase"""
        
        if phase == 'Plan':
            self.render_plan_phase(project_id, methodology)
        elif phase == 'Do':
            self.render_do_phase(project_id, methodology)
        elif phase in ['Check', 'Study']:
            self.render_check_study_phase(project_id, phase, methodology)
        elif phase == 'Act':
            self.render_act_phase(project_id, methodology)
    
    # ==================== PLAN PHASE ====================
    
    def render_plan_phase(self, project_id: int, methodology: str):
        """Render Plan phase interface"""
        st.write("### 📋 PLAN - Lập Kế hoạch")
        
        st.info("""
        **Mục tiêu Plan Phase:**
        - Xác định vấn đề và mục tiêu cải tiến
        - Phân tích tình hình hiện tại
        - Lập kế hoạch hành động chi tiết
        - Xác định metrics để đo lường
        """)
        
        # Create sub-tabs for Plan phase
        plan_tabs = st.tabs([
            "🎯 Vấn đề & Mục tiêu",
            "📊 Phân tích Hiện trạng",
            "📝 Kế hoạch Hành động",
            "📈 Metrics & KPIs"
        ])
        
        with plan_tabs[0]:
            self.render_problem_statement(project_id, methodology)
        
        with plan_tabs[1]:
            self.render_current_situation(project_id, methodology)
        
        with plan_tabs[2]:
            self.render_action_plan(project_id, methodology)
        
        with plan_tabs[3]:
            self.render_metrics(project_id, methodology)
    
    def render_problem_statement(self, project_id: int, methodology: str):
        """Render problem statement and objectives"""
        st.write("#### 🎯 Định nghĩa Vấn đề & Mục tiêu")
        
        # Get existing data
        data = self.db.get_pdca_data(project_id, methodology, 'Plan', 'problem_statement')
        
        with st.form(f"problem_form_{project_id}"):
            problem = st.text_area(
                "Vấn đề cần giải quyết",
                value=data.get('problem', '') if data else '',
                height=100,
                help="Mô tả rõ ràng vấn đề hiện tại"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                current_state = st.text_area(
                    "Tình trạng hiện tại",
                    value=data.get('current_state', '') if data else '',
                    height=100
                )
            
            with col2:
                target_state = st.text_area(
                    "Mục tiêu mong muốn",
                    value=data.get('target_state', '') if data else '',
                    height=100
                )
            
            impact = st.text_area(
                "Tác động của vấn đề",
                value=data.get('impact', '') if data else '',
                help="Chi phí, thời gian, chất lượng bị ảnh hưởng"
            )
            
            root_cause = st.text_area(
                "Nguyên nhân gốc rễ (tạm thời)",
                value=data.get('root_cause', '') if data else '',
                help="Sẽ được xác định rõ hơn ở các phase sau"
            )
            
            if st.form_submit_button("💾 Lưu", type="primary"):
                problem_data = {
                    'problem': problem,
                    'current_state': current_state,
                    'target_state': target_state,
                    'impact': impact,
                    'root_cause': root_cause
                }
                
                success = self.db.save_pdca_data(
                    project_id, methodology, 'Plan', 
                    'problem_statement', problem_data
                )
                
                if success:
                    st.success("✅ Đã lưu!")
                    st.rerun()
    
    def render_current_situation(self, project_id: int, methodology: str):
        """Render current situation analysis"""
        st.write("#### 📊 Phân tích Hiện trạng")
        
        data = self.db.get_pdca_data(project_id, methodology, 'Plan', 'current_situation')
        
        with st.form(f"current_situation_{project_id}"):
            # 5W1H Analysis
            st.write("**Phân tích 5W1H**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                what = st.text_area("What - Vấn đề gì?", value=data.get('what', '') if data else '')
                who = st.text_input("Who - Ai liên quan?", value=data.get('who', '') if data else '')
                when = st.text_input("When - Khi nào xảy ra?", value=data.get('when', '') if data else '')
            
            with col2:
                where = st.text_input("Where - Ở đâu?", value=data.get('where', '') if data else '')
                why = st.text_area("Why - Tại sao?", value=data.get('why', '') if data else '')
                how = st.text_area("How - Như thế nào?", value=data.get('how', '') if data else '')
            
            # Current process description
            st.write("**Quy trình hiện tại**")
            current_process = st.text_area(
                "Mô tả quy trình hiện tại",
                value=data.get('current_process', '') if data else '',
                height=100
            )
            
            # Data collection
            st.write("**Dữ liệu thu thập**")
            data_collected = st.text_area(
                "Dữ liệu đã thu thập về vấn đề",
                value=data.get('data_collected', '') if data else '',
                height=80
            )
            
            if st.form_submit_button("💾 Lưu Phân tích", type="primary"):
                situation_data = {
                    'what': what, 'who': who, 'when': when,
                    'where': where, 'why': why, 'how': how,
                    'current_process': current_process,
                    'data_collected': data_collected
                }
                
                success = self.db.save_pdca_data(
                    project_id, methodology, 'Plan',
                    'current_situation', situation_data
                )
                
                if success:
                    st.success("✅ Đã lưu phân tích!")
                    st.rerun()
    
    def render_action_plan(self, project_id: int, methodology: str):
        """Render action plan"""
        st.write("#### 📝 Kế hoạch Hành động")
        
        # Get existing actions
        actions = self.db.get_pdca_actions(project_id, methodology, 'Plan')
        
        # Add new action
        with st.expander("➕ Thêm Hành động mới", expanded=False):
            with st.form(f"new_action_{project_id}"):
                action_name = st.text_input("Tên hành động")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    responsible = st.text_input("Người phụ trách")
                with col2:
                    start_date = st.date_input("Ngày bắt đầu")
                with col3:
                    end_date = st.date_input("Ngày kết thúc")
                
                description = st.text_area("Mô tả chi tiết")
                resources = st.text_input("Nguồn lực cần thiết")
                
                if st.form_submit_button("➕ Thêm hành động"):
                    if action_name and responsible:
                        action_data = {
                            'action_name': action_name,
                            'responsible': responsible,
                            'start_date': str(start_date),
                            'end_date': str(end_date),
                            'description': description,
                            'resources': resources,
                            'status': 'Planned'
                        }
                        
                        success = self.db.add_pdca_action(
                            project_id, methodology, 'Plan', action_data
                        )
                        
                        if success:
                            st.success("✅ Đã thêm hành động!")
                            st.rerun()
        
        # Display actions
        if actions and not actions.empty:
            st.write(f"**Danh sách Hành động ({len(actions)} items)**")
            st.dataframe(
                actions[['action_name', 'responsible', 'start_date', 'end_date', 'status']],
                use_container_width=True
            )
        else:
            st.info("Chưa có hành động nào. Hãy thêm mới!")
    
    def render_metrics(self, project_id: int, methodology: str):
        """Render metrics and KPIs"""
        st.write("#### 📈 Chỉ số Đo lường (Metrics & KPIs)")
        
        metrics = self.db.get_pdca_metrics(project_id, methodology, 'Plan')
        
        # Add new metric
        with st.expander("➕ Thêm Metric mới", expanded=False):
            with st.form(f"new_metric_{project_id}"):
                metric_name = st.text_input("Tên chỉ số")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    baseline = st.number_input("Baseline (hiện tại)", value=0.0)
                with col2:
                    target = st.number_input("Target (mục tiêu)", value=0.0)
                with col3:
                    unit = st.text_input("Đơn vị", value="%")
                
                measurement_method = st.text_area("Phương pháp đo")
                frequency = st.selectbox("Tần suất đo", ["Hàng ngày", "Hàng tuần", "Hàng tháng"])
                
                if st.form_submit_button("➕ Thêm metric"):
                    if metric_name:
                        metric_data = {
                            'metric_name': metric_name,
                            'baseline': baseline,
                            'target': target,
                            'unit': unit,
                            'measurement_method': measurement_method,
                            'frequency': frequency
                        }
                        
                        success = self.db.add_pdca_metric(
                            project_id, methodology, 'Plan', metric_data
                        )
                        
                        if success:
                            st.success("✅ Đã thêm metric!")
                            st.rerun()
        
        # Display metrics
        if metrics and not metrics.empty:
            st.write(f"**Danh sách Metrics ({len(metrics)} items)**")
            
            # Create bar chart
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Baseline',
                x=metrics['metric_name'],
                y=metrics['baseline'],
                marker_color='lightblue'
            ))
            fig.add_trace(go.Bar(
                name='Target',
                x=metrics['metric_name'],
                y=metrics['target'],
                marker_color='green'
            ))
            
            fig.update_layout(
                title="Baseline vs Target",
                barmode='group',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(metrics, use_container_width=True)
    
    # ==================== DO PHASE ====================
    
    def render_do_phase(self, project_id: int, methodology: str):
        """Render Do phase interface"""
        st.write("### 🛠️ DO - Thực hiện")
        
        st.info("""
        **Mục tiêu Do Phase:**
        - Thực hiện kế hoạch đã lập
        - Thu thập dữ liệu trong quá trình thực hiện
        - Ghi chép các vấn đề phát sinh
        - Cập nhật tiến độ
        """)
        
        do_tabs = st.tabs([
            "✅ Thực hiện Kế hoạch",
            "📊 Thu thập Dữ liệu",
            "⚠️ Vấn đề Phát sinh",
            "📈 Tiến độ"
        ])
        
        with do_tabs[0]:
            self.render_implementation_tracking(project_id, methodology)
        
        with do_tabs[1]:
            self.render_data_collection_do(project_id, methodology)
        
        with do_tabs[2]:
            self.render_issues_log(project_id, methodology)
        
        with do_tabs[3]:
            self.render_progress_tracking(project_id, methodology)
    
    def render_implementation_tracking(self, project_id: int, methodology: str):
        """Track implementation of plan"""
        st.write("#### ✅ Theo dõi Thực hiện")
        
        # Get actions from Plan phase
        actions = self.db.get_pdca_actions(project_id, methodology, 'Plan')
        
        if actions is None or actions.empty:
            st.warning("⚠️ Chưa có kế hoạch hành động từ Plan phase!")
            return
        
        # Update action status
        st.write("**Cập nhật Trạng thái Hành động**")
        
        for idx, action in actions.iterrows():
            with st.expander(f"📌 {action['action_name']}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Người phụ trách:** {action['responsible']}")
                    st.write(f"**Thời gian:** {action['start_date']} → {action['end_date']}")
                    st.write(f"**Mô tả:** {action.get('description', 'N/A')}")
                
                with col2:
                    new_status = st.selectbox(
                        "Trạng thái",
                        ["Planned", "In Progress", "Completed", "Delayed"],
                        index=["Planned", "In Progress", "Completed", "Delayed"].index(action.get('status', 'Planned')),
                        key=f"status_{idx}"
                    )
                    
                    if st.button("💾 Cập nhật", key=f"update_{idx}"):
                        success = self.db.update_pdca_action_status(
                            action['id'], new_status
                        )
                        if success:
                            st.success("✅ Đã cập nhật!")
                            st.rerun()
                
                # Add notes
                notes = st.text_area(
                    "Ghi chú thực hiện",
                    value=action.get('notes', ''),
                    key=f"notes_{idx}"
                )
                
                if st.button("📝 Lưu ghi chú", key=f"save_notes_{idx}"):
                    success = self.db.update_pdca_action_notes(action['id'], notes)
                    if success:
                        st.success("✅ Đã lưu ghi chú!")
    
    def render_data_collection_do(self, project_id: int, methodology: str):
        """Data collection during implementation"""
        st.write("#### 📊 Thu thập Dữ liệu")
        
        # Get metrics from Plan
        metrics = self.db.get_pdca_metrics(project_id, methodology, 'Plan')
        
        if metrics is None or metrics.empty:
            st.warning("⚠️ Chưa có metrics từ Plan phase!")
            return
        
        st.write("**Ghi nhận Giá trị Đo lường**")
        
        # Record measurements
        with st.form(f"measurement_form_{project_id}"):
            metric_name = st.selectbox("Chọn Metric", metrics['metric_name'].tolist())
            
            col1, col2 = st.columns(2)
            with col1:
                measured_value = st.number_input("Giá trị đo được", value=0.0)
            with col2:
                measurement_date = st.date_input("Ngày đo")
            
            notes = st.text_area("Ghi chú")
            
            if st.form_submit_button("📊 Lưu Đo lường"):
                measurement_data = {
                    'metric_name': metric_name,
                    'measured_value': measured_value,
                    'measurement_date': str(measurement_date),
                    'notes': notes
                }
                
                success = self.db.add_pdca_measurement(
                    project_id, methodology, 'Do', measurement_data
                )
                
                if success:
                    st.success("✅ Đã lưu dữ liệu!")
                    st.rerun()
        
        # Display measurements
        measurements = self.db.get_pdca_measurements(project_id, methodology, 'Do')
        
        if measurements is not None and not measurements.empty:
            st.write("**Dữ liệu đã thu thập**")
            st.dataframe(measurements, use_container_width=True)
    
    def render_issues_log(self, project_id: int, methodology: str):
        """Log issues during implementation"""
        st.write("#### ⚠️ Nhật ký Vấn đề")
        
        # Add new issue
        with st.expander("➕ Thêm Vấn đề mới", expanded=False):
            with st.form(f"new_issue_{project_id}"):
                issue_title = st.text_input("Tiêu đề vấn đề")
                severity = st.selectbox("Mức độ", ["Low", "Medium", "High", "Critical"])
                description = st.text_area("Mô tả chi tiết")
                action_taken = st.text_area("Hành động đã thực hiện")
                
                if st.form_submit_button("➕ Thêm vấn đề"):
                    if issue_title:
                        issue_data = {
                            'issue_title': issue_title,
                            'severity': severity,
                            'description': description,
                            'action_taken': action_taken,
                            'status': 'Open',
                            'reported_date': str(datetime.now().date())
                        }
                        
                        success = self.db.add_pdca_issue(
                            project_id, methodology, 'Do', issue_data
                        )
                        
                        if success:
                            st.success("✅ Đã ghi nhận vấn đề!")
                            st.rerun()
        
        # Display issues
        issues = self.db.get_pdca_issues(project_id, methodology, 'Do')
        
        if issues is not None and not issues.empty:
            st.write(f"**Danh sách Vấn đề ({len(issues)} items)**")
            
            for idx, issue in issues.iterrows():
                severity_colors = {
                    'Low': '🟢', 'Medium': '🟡',
                    'High': '🟠', 'Critical': '🔴'
                }
                
                with st.expander(f"{severity_colors.get(issue['severity'], '⚪')} {issue['issue_title']}", expanded=False):
                    st.write(f"**Mức độ:** {issue['severity']}")
                    st.write(f"**Ngày báo cáo:** {issue['reported_date']}")
                    st.write(f"**Mô tả:** {issue['description']}")
                    st.write(f"**Hành động:** {issue.get('action_taken', 'N/A')}")
                    
                    new_status = st.selectbox(
                        "Trạng thái",
                        ["Open", "In Progress", "Resolved", "Closed"],
                        index=["Open", "In Progress", "Resolved", "Closed"].index(issue.get('status', 'Open')),
                        key=f"issue_status_{idx}"
                    )
                    
                    if st.button("💾 Cập nhật", key=f"update_issue_{idx}"):
                        success = self.db.update_pdca_issue_status(issue['id'], new_status)
                        if success:
                            st.success("✅ Đã cập nhật!")
                            st.rerun()
        else:
            st.info("Chưa có vấn đề nào được ghi nhận.")
    
    def render_progress_tracking(self, project_id: int, methodology: str):
        """Track overall progress"""
        st.write("#### 📈 Tổng quan Tiến độ")
        
        # Get actions
        actions = self.db.get_pdca_actions(project_id, methodology, 'Plan')
        
        if actions is None or actions.empty:
            st.warning("Chưa có dữ liệu!")
            return
        
        # Calculate progress
        total_actions = len(actions)
        completed = len(actions[actions['status'] == 'Completed'])
        in_progress = len(actions[actions['status'] == 'In Progress'])
        planned = len(actions[actions['status'] == 'Planned'])
        delayed = len(actions[actions['status'] == 'Delayed'])
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Tổng số", total_actions)
        col2.metric("Hoàn thành", completed, f"{(completed/total_actions*100):.1f}%")
        col3.metric("Đang làm", in_progress)
        col4.metric("Trễ hạn", delayed, delta_color="inverse")
        
        # Pie chart
        fig = go.Figure(data=[go.Pie(
            labels=['Completed', 'In Progress', 'Planned', 'Delayed'],
            values=[completed, in_progress, planned, delayed],
            marker_colors=['green', 'blue', 'gray', 'red']
        )])
        fig.update_layout(title="Phân bố Trạng thái Hành động", height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # ==================== CHECK/STUDY PHASE ====================
    
    def render_check_study_phase(self, project_id: int, phase: str, methodology: str):
        """Render Check or Study phase"""
        st.write(f"### ✅ {phase.upper()} - Kiểm tra & Phân tích")
        
        if phase == 'Check':
            info_text = """
            **Mục tiêu Check Phase:**
            - Kiểm tra kết quả so với mục tiêu
            - So sánh Before/After
            - Đánh giá hiệu quả
            - Xác định điểm mạnh/yếu
            """
        else:  # Study
            info_text = """
            **Mục tiêu Study Phase:**
            - Nghiên cứu kết quả chi tiết
            - Phân tích nguyên nhân thành công/thất bại
            - Rút ra bài học kinh nghiệm
            - Xác định best practices
            """
        
        st.info(info_text)
        
        check_tabs = st.tabs([
            "📊 Kết quả So sánh",
            "📈 Phân tích Hiệu quả",
            "💡 Bài học Kinh nghiệm",
            "✅ Đánh giá"
        ])
        
        with check_tabs[0]:
            self.render_results_comparison(project_id, methodology)
        
        with check_tabs[1]:
            self.render_effectiveness_analysis(project_id, methodology)
        
        with check_tabs[2]:
            self.render_lessons_learned(project_id, phase, methodology)
        
        with check_tabs[3]:
            self.render_evaluation(project_id, phase, methodology)
    
    def render_results_comparison(self, project_id: int, methodology: str):
        """Compare before/after results"""
        st.write("#### 📊 So sánh Kết quả (Before vs After)")
        
        # Get metrics and measurements
        metrics = self.db.get_pdca_metrics(project_id, methodology, 'Plan')
        measurements = self.db.get_pdca_measurements(project_id, methodology, 'Do')
        
        if metrics is None or metrics.empty:
            st.warning("Chưa có metrics để so sánh!")
            return
        
        # Create comparison
        comparison_data = []
        
        for _, metric in metrics.iterrows():
            metric_name = metric['metric_name']
            baseline = metric['baseline']
            target = metric['target']
            
            # Get latest measurement
            if measurements is not None and not measurements.empty:
                metric_measurements = measurements[measurements['metric_name'] == metric_name]
                if not metric_measurements.empty:
                    actual = metric_measurements.iloc[-1]['measured_value']
                else:
                    actual = 0
            else:
                actual = 0
            
            improvement = ((actual - baseline) / baseline * 100) if baseline != 0 else 0
            
            comparison_data.append({
                'Metric': metric_name,
                'Baseline': baseline,
                'Target': target,
                'Actual': actual,
                'Improvement (%)': round(improvement, 2),
                'Status': '✅' if actual >= target else '⚠️'
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # Display table
        st.dataframe(comparison_df, use_container_width=True)
        
        # Chart
        fig = go.Figure()
        
        for _, row in comparison_df.iterrows():
            fig.add_trace(go.Bar(
                name=row['Metric'],
                x=['Baseline', 'Target', 'Actual'],
                y=[row['Baseline'], row['Target'], row['Actual']]
            ))
        
        fig.update_layout(
            title="Before vs Target vs Actual",
            barmode='group',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def render_effectiveness_analysis(self, project_id: int, methodology: str):
        """Analyze effectiveness"""
        st.write("#### 📈 Phân tích Hiệu quả")
        
        data = self.db.get_pdca_data(project_id, methodology, 'Check', 'effectiveness')
        
        with st.form(f"effectiveness_form_{project_id}"):
            st.write("**Đánh giá Hiệu quả Tổng thể**")
            
            overall_rating = st.slider(
                "Đánh giá chung (1-10)",
                1, 10,
                value=data.get('overall_rating', 5) if data else 5
            )
            
            st.write("**Đạt được**")
            achievements = st.text_area(
                "Những gì đã đạt được",
                value=data.get('achievements', '') if data else '',
                height=100
            )
            
            st.write("**Chưa đạt được**")
            shortcomings = st.text_area(
                "Những gì chưa đạt được",
                value=data.get('shortcomings', '') if data else '',
                height=100
            )
            
            st.write("**Nguyên nhân**")
            root_causes = st.text_area(
                "Nguyên nhân thành công/thất bại",
                value=data.get('root_causes', '') if data else '',
                height=100
            )
            
            if st.form_submit_button("💾 Lưu Phân tích"):
                effectiveness_data = {
                    'overall_rating': overall_rating,
                    'achievements': achievements,
                    'shortcomings': shortcomings,
                    'root_causes': root_causes
                }
                
                success = self.db.save_pdca_data(
                    project_id, methodology, 'Check',
                    'effectiveness', effectiveness_data
                )
                
                if success:
                    st.success("✅ Đã lưu phân tích!")
                    st.rerun()
    
    def render_lessons_learned(self, project_id: int, phase: str, methodology: str):
        """Document lessons learned"""
        st.write("#### 💡 Bài học Kinh nghiệm")
        
        lessons = self.db.get_pdca_lessons(project_id, methodology, phase)
        
        # Add new lesson
        with st.expander("➕ Thêm Bài học", expanded=False):
            with st.form(f"new_lesson_{project_id}"):
                lesson_title = st.text_input("Tiêu đề")
                category = st.selectbox(
                    "Phân loại",
                    ["Success Factor", "Challenge", "Best Practice", "Mistake to Avoid"]
                )
                description = st.text_area("Mô tả chi tiết")
                recommendation = st.text_area("Khuyến nghị cho lần sau")
                
                if st.form_submit_button("➕ Thêm"):
                    if lesson_title:
                        lesson_data = {
                            'lesson_title': lesson_title,
                            'category': category,
                            'description': description,
                            'recommendation': recommendation
                        }
                        
                        success = self.db.add_pdca_lesson(
                            project_id, methodology, phase, lesson_data
                        )
                        
                        if success:
                            st.success("✅ Đã thêm bài học!")
                            st.rerun()
        
        # Display lessons
        if lessons is not None and not lessons.empty:
            st.write(f"**Danh sách Bài học ({len(lessons)} items)**")
            
            for idx, lesson in lessons.iterrows():
                category_icons = {
                    'Success Factor': '🌟',
                    'Challenge': '⚠️',
                    'Best Practice': '✅',
                    'Mistake to Avoid': '❌'
                }
                
                with st.expander(f"{category_icons.get(lesson['category'], '📝')} {lesson['lesson_title']}", expanded=False):
                    st.write(f"**Phân loại:** {lesson['category']}")
                    st.write(f"**Mô tả:** {lesson['description']}")
                    st.write(f"**Khuyến nghị:** {lesson.get('recommendation', 'N/A')}")
        else:
            st.info("Chưa có bài học nào.")
    
    def render_evaluation(self, project_id: int, phase: str, methodology: str):
        """Overall evaluation"""
        st.write("#### ✅ Đánh giá Tổng quan")
        
        data = self.db.get_pdca_data(project_id, methodology, phase, 'evaluation')
        
        with st.form(f"evaluation_form_{project_id}"):
            decision = st.radio(
                "Quyết định",
                ["✅ Tiếp tục áp dụng (Act)", "🔄 Cần cải tiến thêm (lặp lại PDCA)", "❌ Không áp dụng"],
                index=0
            )
            
            justification = st.text_area(
                "Lý do quyết định",
                value=data.get('justification', '') if data else ''
            )
            
            next_steps = st.text_area(
                "Các bước tiếp theo",
                value=data.get('next_steps', '') if data else ''
            )
            
            if st.form_submit_button("💾 Lưu Đánh giá"):
                eval_data = {
                    'decision': decision,
                    'justification': justification,
                    'next_steps': next_steps
                }
                
                success = self.db.save_pdca_data(
                    project_id, methodology, phase,
                    'evaluation', eval_data
                )
                
                if success:
                    st.success("✅ Đã lưu đánh giá!")
                    st.rerun()
    
    # ==================== ACT PHASE ====================
    
    def render_act_phase(self, project_id: int, methodology: str):
        """Render Act phase"""
        st.write("### 🚀 ACT - Hành động")
        
        st.info("""
        **Mục tiêu Act Phase:**
        - Chuẩn hóa giải pháp thành công
        - Nhân rộng ra toàn bộ tổ chức
        - Cập nhật quy trình/tài liệu
        - Lên kế hoạch cải tiến tiếp theo
        """)
        
        act_tabs = st.tabs([
            "📋 Standardization",
            "📢 Nhân rộng",
            "📚 Tài liệu",
            "🔄 Cải tiến Liên tục"
        ])
        
        with act_tabs[0]:
            self.render_standardization(project_id, methodology)
        
        with act_tabs[1]:
            self.render_rollout_plan(project_id, methodology)
        
        with act_tabs[2]:
            self.render_documentation_update(project_id, methodology)
        
        with act_tabs[3]:
            self.render_continuous_improvement(project_id, methodology)
    
    def render_standardization(self, project_id: int, methodology: str):
        """Standardize successful solutions"""
        st.write("#### 📋 Chuẩn hóa Giải pháp")
        
        data = self.db.get_pdca_data(project_id, methodology, 'Act', 'standardization')
        
        with st.form(f"standard_form_{project_id}"):
            st.write("**Quy trình Chuẩn mới**")
            
            new_standard = st.text_area(
                "Mô tả quy trình chuẩn mới",
                value=data.get('new_standard', '') if data else '',
                height=150
            )
            
            st.write("**Thay đổi so với quy trình cũ**")
            changes = st.text_area(
                "Những gì đã thay đổi",
                value=data.get('changes', '') if data else '',
                height=100
            )
            
            st.write("**Đào tạo cần thiết**")
            training_required = st.text_area(
                "Nội dung đào tạo",
                value=data.get('training_required', '') if data else ''
            )
            
            approval_status = st.selectbox(
                "Trạng thái phê duyệt",
                ["Draft", "Under Review", "Approved", "Implemented"]
            )
            
            if st.form_submit_button("💾 Lưu"):
                standard_data = {
                    'new_standard': new_standard,
                    'changes': changes,
                    'training_required': training_required,
                    'approval_status': approval_status
                }
                
                success = self.db.save_pdca_data(
                    project_id, methodology, 'Act',
                    'standardization', standard_data
                )
                
                if success:
                    st.success("✅ Đã lưu!")
                    st.rerun()
    
    def render_rollout_plan(self, project_id: int, methodology: str):
        """Plan for rollout"""
        st.write("#### 📢 Kế hoạch Nhân rộng")
        
        rollout_plan = self.db.get_pdca_rollout_plan(project_id, methodology)
        
        # Add rollout item
        with st.expander("➕ Thêm Kế hoạch Nhân rộng", expanded=False):
            with st.form(f"rollout_form_{project_id}"):
                department = st.text_input("Phòng/Ban")
                timeline = st.text_input("Thời gian triển khai")
                responsible = st.text_input("Người chịu trách nhiệm")
                resources = st.text_area("Nguồn lực cần thiết")
                
                if st.form_submit_button("➕ Thêm"):
                    if department:
                        rollout_data = {
                            'department': department,
                            'timeline': timeline,
                            'responsible': responsible,
                            'resources': resources,
                            'status': 'Planned'
                        }
                        
                        success = self.db.add_pdca_rollout(
                            project_id, methodology, rollout_data
                        )
                        
                        if success:
                            st.success("✅ Đã thêm!")
                            st.rerun()
        
        # Display rollout plan
        if rollout_plan is not None and not rollout_plan.empty:
            st.write(f"**Kế hoạch Nhân rộng ({len(rollout_plan)} items)**")
            st.dataframe(rollout_plan, use_container_width=True)
        else:
            st.info("Chưa có kế hoạch nhân rộng.")
    
    def render_documentation_update(self, project_id: int, methodology: str):
        """Update documentation"""
        st.write("#### 📚 Cập nhật Tài liệu")
        
        data = self.db.get_pdca_data(project_id, methodology, 'Act', 'documentation')
        
        with st.form(f"doc_update_form_{project_id}"):
            st.write("**Tài liệu cần cập nhật**")
            
            documents = st.text_area(
                "Danh sách tài liệu",
                value=data.get('documents', '') if data else '',
                help="SOP, Work Instructions, Forms, etc."
            )
            
            update_details = st.text_area(
                "Chi tiết cập nhật",
                value=data.get('update_details', '') if data else ''
            )
            
            responsible = st.text_input(
                "Người phụ trách",
                value=data.get('responsible', '') if data else ''
            )
            
            deadline = st.date_input("Deadline")
            
            if st.form_submit_button("💾 Lưu"):
                doc_data = {
                    'documents': documents,
                    'update_details': update_details,
                    'responsible': responsible,
                    'deadline': str(deadline)
                }
                
                success = self.db.save_pdca_data(
                    project_id, methodology, 'Act',
                    'documentation', doc_data
                )
                
                if success:
                    st.success("✅ Đã lưu!")
                    st.rerun()
    
    def render_continuous_improvement(self, project_id: int, methodology: str):
        """Plan for continuous improvement"""
        st.write("#### 🔄 Kế hoạch Cải tiến Liên tục")
        
        data = self.db.get_pdca_data(project_id, methodology, 'Act', 'continuous_improvement')
        
        with st.form(f"ci_form_{project_id}"):
            st.write("**Cơ hội Cải tiến Tiếp theo**")
            
            opportunities = st.text_area(
                "Xác định các cơ hội",
                value=data.get('opportunities', '') if data else '',
                height=100
            )
            
            next_pdca_cycle = st.text_area(
                "Chu kỳ PDCA tiếp theo",
                value=data.get('next_pdca_cycle', '') if data else '',
                help="Vấn đề gì sẽ giải quyết trong chu kỳ sau?"
            )
            
            monitoring_plan = st.text_area(
                "Kế hoạch Giám sát",
                value=data.get('monitoring_plan', '') if data else '',
                help="Làm thế nào để duy trì cải tiến?"
            )
            
            review_frequency = st.selectbox(
                "Tần suất Review",
                ["Weekly", "Monthly", "Quarterly", "Annually"]
            )
            
            if st.form_submit_button("💾 Lưu Kế hoạch"):
                ci_data = {
                    'opportunities': opportunities,
                    'next_pdca_cycle': next_pdca_cycle,
                    'monitoring_plan': monitoring_plan,
                    'review_frequency': review_frequency
                }
                
                success = self.db.save_pdca_data(
                    project_id, methodology, 'Act',
                    'continuous_improvement', ci_data
                )
                
                if success:
                    st.success("✅ Đã lưu kế hoạch cải tiến!")
                    st.rerun()
        
        # Completion summary
        st.markdown("---")
        st.write("### 🎉 Hoàn thành Chu kỳ PDCA/PDSA")
        
        if st.button("✅ Đánh dấu Hoàn thành Chu kỳ", type="primary"):
            success = self.db.mark_pdca_cycle_complete(project_id, methodology)
            if success:
                st.balloons()
                st.success("🎉 Chúc mừng! Đã hoàn thành chu kỳ PDCA/PDSA!")
                st.info("💡 Bạn có thể bắt đầu chu kỳ mới cho cải tiến tiếp theo!")

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime

class DMAICTools:
    def __init__(self, db):
        self.db = db
    
    def render_dmaic_tracker(self, project_id, project_info):
        """Main DMAIC tracking interface"""
        st.header("🔄 DMAIC Methodology Tracker")
        
        # Phase tabs
        dmaic_tabs = st.tabs(["📋 Define", "📊 Measure", "🔍 Analyze", "⚡ Improve", "🎯 Control"])
        
        with dmaic_tabs[0]:
            self.render_define_phase(project_id)
        
        with dmaic_tabs[1]:
            self.render_measure_phase(project_id)
        
        with dmaic_tabs[2]:
            self.render_analyze_phase(project_id)
        
        with dmaic_tabs[3]:
            self.render_improve_phase(project_id)
        
        with dmaic_tabs[4]:
            self.render_control_phase(project_id)
    
    # ==================== DEFINE PHASE ====================
    def render_define_phase(self, project_id):
        st.subheader("📋 Define Phase")
        
        # Load existing data
        define_data = self.db.get_dmaic_define(project_id) or {}
        
        # SIPOC Builder
        with st.expander("🔗 SIPOC Diagram", expanded=True):
            st.write("**SIPOC (Suppliers, Inputs, Process, Outputs, Customers)**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                suppliers = st.text_area(
                    "Suppliers (Nhà cung cấp)",
                    value=define_data.get('sipoc_suppliers', ''),
                    placeholder="Danh sách nhà cung cấp, mỗi dòng một mục",
                    height=100
                )
                
                inputs = st.text_area(
                    "Inputs (Đầu vào)",
                    value=define_data.get('sipoc_inputs', ''),
                    placeholder="Các đầu vào cần thiết",
                    height=100
                )
                
                process = st.text_area(
                    "Process (Quy trình)",
                    value=define_data.get('sipoc_process', ''),
                    placeholder="Các bước quy trình chính",
                    height=100
                )
            
            with col2:
                outputs = st.text_area(
                    "Outputs (Đầu ra)",
                    value=define_data.get('sipoc_outputs', ''),
                    placeholder="Sản phẩm/dịch vụ đầu ra",
                    height=100
                )
                
                customers = st.text_area(
                    "Customers (Khách hàng)",
                    value=define_data.get('sipoc_customers', ''),
                    placeholder="Người nhận đầu ra",
                    height=100
                )
            
            if st.button("💾 Lưu SIPOC", key="save_sipoc"):
                sipoc_data = {
                    'sipoc_suppliers': suppliers,
                    'sipoc_inputs': inputs,
                    'sipoc_process': process,
                    'sipoc_outputs': outputs,
                    'sipoc_customers': customers
                }
                self.db.save_dmaic_define(project_id, sipoc_data)
                st.success("✅ Đã lưu SIPOC!")
                st.rerun()
        
        # Project Charter
        with st.expander("📜 Project Charter", expanded=False):
            business_case = st.text_area(
                "Business Case",
                value=define_data.get('charter_business_case', ''),
                placeholder="Lý do kinh doanh cho dự án này",
                height=100
            )
            
            objectives = st.text_area(
                "Objectives (Mục tiêu)",
                value=define_data.get('charter_objectives', ''),
                placeholder="Các mục tiêu cụ thể, đo lường được",
                height=100
            )
            
            scope = st.text_area(
                "Scope (Phạm vi)",
                value=define_data.get('charter_scope', ''),
                placeholder="Phạm vi dự án (bao gồm và không bao gồm)",
                height=100
            )
            
            milestones = st.text_area(
                "Key Milestones (Cột mốc quan trọng)",
                value=define_data.get('charter_milestones', ''),
                placeholder="Các cột mốc chính và thời gian dự kiến",
                height=100
            )
            
            if st.button("💾 Lưu Project Charter", key="save_charter"):
                charter_data = {
                    'charter_business_case': business_case,
                    'charter_objectives': objectives,
                    'charter_scope': scope,
                    'charter_milestones': milestones
                }
                self.db.save_dmaic_define(project_id, charter_data)
                st.success("✅ Đã lưu Project Charter!")
                st.rerun()
        
        # Voice of Customer (VOC)
        with st.expander("🗣️ Voice of Customer (VOC)", expanded=False):
            st.write("**Thu thập phản hồi từ khách hàng**")
            
            # Load existing VOC data
            voc_list = []
            if define_data.get('voc_data'):
                try:
                    voc_list = json.loads(define_data['voc_data'])
                except:
                    voc_list = []
            
            # Add new VOC entry
            with st.form("voc_form"):
                col1, col2 = st.columns(2)
                with col1:
                    voc_source = st.text_input("Nguồn (Survey, Interview, etc.)")
                    voc_customer = st.text_input("Khách hàng/Nhóm")
                
                with col2:
                    voc_date = st.date_input("Ngày thu thập")
                    voc_category = st.selectbox("Loại", ["Positive", "Negative", "Suggestion", "Question"])
                
                voc_feedback = st.text_area("Phản hồi", height=100)
                
                if st.form_submit_button("➕ Thêm VOC"):
                    voc_list.append({
                        'source': voc_source,
                        'customer': voc_customer,
                        'date': str(voc_date),
                        'category': voc_category,
                        'feedback': voc_feedback
                    })
                    self.db.save_dmaic_define(project_id, {'voc_data': json.dumps(voc_list)})
                    st.success("✅ Đã thêm VOC!")
                    st.rerun()
            
            # Display existing VOC
            if voc_list:
                st.write("**Danh sách VOC đã thu thập:**")
                for idx, voc in enumerate(voc_list):
                    with st.container():
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.write(f"**{voc['customer']}** ({voc['source']})")
                            st.write(voc['feedback'])
                        with col2:
                            st.write(f"📅 {voc['date']}")
                            st.write(f"🏷️ {voc['category']}")
                        with col3:
                            if st.button("🗑️", key=f"del_voc_{idx}"):
                                voc_list.pop(idx)
                                self.db.save_dmaic_define(project_id, {'voc_data': json.dumps(voc_list)})
                                st.rerun()
                        st.divider()
            
            # VOC Summary
            voc_summary = st.text_area(
                "VOC Summary (Tóm tắt phân tích)",
                value=define_data.get('voc_summary', ''),
                placeholder="Tóm tắt các insight chính từ VOC",
                height=150
            )
            
            if st.button("💾 Lưu VOC Summary", key="save_voc_summary"):
                self.db.save_dmaic_define(project_id, {'voc_summary': voc_summary})
                st.success("✅ Đã lưu VOC Summary!")
                st.rerun()
    
    # ==================== MEASURE PHASE ====================
    def render_measure_phase(self, project_id):
        st.subheader("📊 Measure Phase")
        
        measure_data = self.db.get_dmaic_measure(project_id) or {}
        
        # Data Collection Plan
        with st.expander("📋 Data Collection Plan", expanded=True):
            data_plan = st.text_area(
                "Kế hoạch thu thập dữ liệu",
                value=measure_data.get('data_collection_plan', ''),
                placeholder="Mô tả cách thu thập dữ liệu, tần suất, người phụ trách",
                height=150
            )
            
            data_sources = st.text_area(
                "Nguồn dữ liệu",
                value=measure_data.get('data_sources', ''),
                placeholder="Các nguồn dữ liệu: hệ thống EMR, survey, quan sát trực tiếp, etc.",
                height=100
            )
            
            if st.button("💾 Lưu Data Collection Plan", key="save_data_plan"):
                plan_data = {
                    'data_collection_plan': data_plan,
                    'data_sources': data_sources
                }
                self.db.save_dmaic_measure(project_id, plan_data)
                st.success("✅ Đã lưu!")
                st.rerun()
        
        # Baseline Metrics
        with st.expander("📈 Baseline Metrics", expanded=True):
            st.write("**Đo lường hiện trạng (Current State)**")
            
            # Load existing metrics
            baseline_list = []
            if measure_data.get('baseline_metrics'):
                try:
                    baseline_list = json.loads(measure_data['baseline_metrics'])
                except:
                    baseline_list = []
            
            # Add new metric
            with st.form("baseline_form"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    metric_name = st.text_input("Tên chỉ số")
                    metric_unit = st.text_input("Đơn vị đo")
                
                with col2:
                    metric_current = st.number_input("Giá trị hiện tại", value=0.0, format="%.2f")
                    metric_target = st.number_input("Mục tiêu", value=0.0, format="%.2f")
                
                with col3:
                    metric_frequency = st.selectbox("Tần suất đo", ["Hàng ngày", "Hàng tuần", "Hàng tháng", "Theo ca"])
                    metric_date = st.date_input("Ngày đo")
                
                metric_notes = st.text_input("Ghi chú")
                
                if st.form_submit_button("➕ Thêm Baseline Metric"):
                    baseline_list.append({
                        'name': metric_name,
                        'unit': metric_unit,
                        'current': metric_current,
                        'target': metric_target,
                        'frequency': metric_frequency,
                        'date': str(metric_date),
                        'notes': metric_notes
                    })
                    self.db.save_dmaic_measure(project_id, {'baseline_metrics': json.dumps(baseline_list)})
                    st.success("✅ Đã thêm metric!")
                    st.rerun()
            
            # Display metrics
            if baseline_list:
                st.write("**Các chỉ số Baseline:**")
                df = pd.DataFrame(baseline_list)
                st.dataframe(df, use_container_width=True)
                
                # Chart
                if len(baseline_list) > 0:
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        name='Hiện tại',
                        x=[m['name'] for m in baseline_list],
                        y=[m['current'] for m in baseline_list],
                        marker_color='lightblue'
                    ))
                    fig.add_trace(go.Bar(
                        name='Mục tiêu',
                        x=[m['name'] for m in baseline_list],
                        y=[m['target'] for m in baseline_list],
                        marker_color='green'
                    ))
                    fig.update_layout(
                        title="Baseline vs Target",
                        barmode='group',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            current_state = st.text_area(
                "Mô tả hiện trạng tổng quan",
                value=measure_data.get('current_state', ''),
                placeholder="Tóm tắt tình trạng hiện tại của quy trình",
                height=100
            )
            
            if st.button("💾 Lưu Current State", key="save_current_state"):
                self.db.save_dmaic_measure(project_id, {'current_state': current_state})
                st.success("✅ Đã lưu!")
                st.rerun()
        
        # Process Mapping
        with st.expander("🗺️ Process Mapping", expanded=False):
            st.write("**Flowchart / Process Map**")
            st.info("💡 Sử dụng tools như Lucidchart, Draw.io, hoặc PowerPoint để tạo process map, sau đó upload vào Documents")
            
            process_description = st.text_area(
                "Mô tả quy trình",
                value=measure_data.get('process_map_data', ''),
                placeholder="Mô tả các bước trong quy trình hiện tại",
                height=200
            )
            
            if st.button("💾 Lưu Process Description", key="save_process"):
                self.db.save_dmaic_measure(project_id, {'process_map_data': process_description})
                st.success("✅ Đã lưu!")
                st.rerun()
    
    # ==================== ANALYZE PHASE ====================
    def render_analyze_phase(self, project_id):
        st.subheader("🔍 Analyze Phase")
        
        analyze_data = self.db.get_dmaic_analyze(project_id) or {}
        
        # Fishbone Diagram
        with st.expander("🐟 Fishbone Diagram (Ishikawa)", expanded=True):
            st.write("**Root Cause Analysis - Biểu đồ xương cá**")
            
            # Load existing data
            fishbone_dict = {}
            if analyze_data.get('fishbone_categories'):
                try:
                    fishbone_dict = json.loads(analyze_data['fishbone_categories'])
                except:
                    fishbone_dict = {}
            
            # Main categories (6M)
            categories = ["Man (Con người)", "Machine (Thiết bị)", "Material (Vật liệu)", 
                         "Method (Phương pháp)", "Measurement (Đo lường)", "Environment (Môi trường)"]
            
            for category in categories:
                st.write(f"**{category}**")
                causes = st.text_area(
                    f"Nguyên nhân từ {category}",
                    value=fishbone_dict.get(category, ''),
                    placeholder="Liệt kê các nguyên nhân, mỗi dòng một mục",
                    height=80,
                    key=f"fishbone_{category}"
                )
                fishbone_dict[category] = causes
            
            if st.button("💾 Lưu Fishbone Diagram", key="save_fishbone"):
                self.db.save_dmaic_analyze(project_id, {'fishbone_categories': json.dumps(fishbone_dict)})
                st.success("✅ Đã lưu Fishbone!")
                st.rerun()
        
        # 5 Whys
        with st.expander("❓ 5 Whys Analysis", expanded=False):
            st.write("**Phân tích 5 lần Tại sao**")
            
            # Load existing 5 whys
            five_whys_list = []
            if analyze_data.get('five_whys_data'):
                try:
                    five_whys_list = json.loads(analyze_data['five_whys_data'])
                except:
                    five_whys_list = []
            
            problem = st.text_input("Vấn đề ban đầu", key="5why_problem")
            
            whys = []
            for i in range(1, 6):
                why = st.text_input(f"Tại sao {i}?", key=f"why_{i}")
                whys.append(why)
            
            root_cause = st.text_input("Root Cause (Nguyên nhân gốc)", key="5why_root")
            
            if st.button("➕ Thêm 5 Whys Analysis", key="add_5whys"):
                five_whys_list.append({
                    'problem': problem,
                    'why1': whys[0],
                    'why2': whys[1],
                    'why3': whys[2],
                    'why4': whys[3],
                    'why5': whys[4],
                    'root_cause': root_cause
                })
                self.db.save_dmaic_analyze(project_id, {'five_whys_data': json.dumps(five_whys_list)})
                st.success("✅ Đã thêm 5 Whys!")
                st.rerun()
            
            # Display existing 5 whys
            if five_whys_list:
                st.write("**Các phân tích 5 Whys:**")
                for idx, analysis in enumerate(five_whys_list):
                    with st.container():
                        st.write(f"**Vấn đề {idx+1}:** {analysis['problem']}")
                        st.write(f"1️⃣ {analysis['why1']}")
                        st.write(f"2️⃣ {analysis['why2']}")
                        st.write(f"3️⃣ {analysis['why3']}")
                        st.write(f"4️⃣ {analysis['why4']}")
                        st.write(f"5️⃣ {analysis['why5']}")
                        st.write(f"🎯 **Root Cause:** {analysis['root_cause']}")
                        st.divider()
        
        # Pareto Chart
        with st.expander("📊 Pareto Analysis", expanded=False):
            st.write("**Phân tích Pareto (80/20 Rule)**")
            
            # Load existing data
            pareto_list = []
            if analyze_data.get('pareto_data'):
                try:
                    pareto_list = json.loads(analyze_data['pareto_data'])
                except:
                    pareto_list = []
            
            # Add new data
            with st.form("pareto_form"):
                col1, col2 = st.columns(2)
                with col1:
                    category = st.text_input("Loại lỗi/Vấn đề")
                with col2:
                    frequency = st.number_input("Tần suất", min_value=0, value=0)
                
                if st.form_submit_button("➕ Thêm dữ liệu"):
                    pareto_list.append({
                        'category': category,
                        'frequency': frequency
                    })
                    self.db.save_dmaic_analyze(project_id, {'pareto_data': json.dumps(pareto_list)})
                    st.success("✅ Đã thêm!")
                    st.rerun()
            
            # Display and chart
            if pareto_list:
                # Sort by frequency
                pareto_df = pd.DataFrame(pareto_list).sort_values('frequency', ascending=False)
                pareto_df['cumulative_percent'] = (pareto_df['frequency'].cumsum() / pareto_df['frequency'].sum()) * 100
                
                # Pareto chart
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    name='Tần suất',
                    x=pareto_df['category'],
                    y=pareto_df['frequency'],
                    marker_color='steelblue',
                    yaxis='y'
                ))
                fig.add_trace(go.Scatter(
                    name='Tích lũy %',
                    x=pareto_df['category'],
                    y=pareto_df['cumulative_percent'],
                    marker_color='red',
                    yaxis='y2',
                    mode='lines+markers'
                ))
                
                fig.update_layout(
                    title='Pareto Chart',
                    yaxis=dict(title='Tần suất'),
                    yaxis2=dict(title='Phần trăm tích lũy', overlaying='y', side='right', range=[0, 100]),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(pareto_df, use_container_width=True)
        
        # Statistical Analysis
        with st.expander("📈 Statistical Analysis", expanded=False):
            st.write("**Phân tích thống kê**")
            
            # Input data
            data_input = st.text_area(
                "Nhập dữ liệu số (mỗi giá trị một dòng)",
                placeholder="10\n15\n12\n18\n20\n...",
                height=150
            )
            
            if data_input:
                try:
                    values = [float(x.strip()) for x in data_input.split('\n') if x.strip()]
                    
                    if values:
                        df_stats = pd.DataFrame({'values': values})
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Mean (Trung bình)", f"{df_stats['values'].mean():.2f}")
                        with col2:
                            st.metric("Median (Trung vị)", f"{df_stats['values'].median():.2f}")
                        with col3:
                            st.metric("Std Dev (Độ lệch chuẩn)", f"{df_stats['values'].std():.2f}")
                        with col4:
                            st.metric("Count (Số lượng)", len(values))
                        
                        # Histogram
                        fig = px.histogram(df_stats, x='values', nbins=20, title='Distribution')
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Save stats
                        stats_summary = {
                            'mean': df_stats['values'].mean(),
                            'median': df_stats['values'].median(),
                            'std': df_stats['values'].std(),
                            'count': len(values),
                            'min': df_stats['values'].min(),
                            'max': df_stats['values'].max()
                        }
                        
                        if st.button("💾 Lưu Statistical Analysis", key="save_stats"):
                            self.db.save_dmaic_analyze(project_id, {
                                'statistical_data': json.dumps(stats_summary)
                            })
                            st.success("✅ Đã lưu!")
                            st.rerun()
                except Exception as e:
                    st.error(f"Lỗi: {e}")
            
            analysis_summary = st.text_area(
                "Kết luận từ phân tích",
                value=analyze_data.get('analysis_summary', ''),
                placeholder="Tóm tắt các phát hiện chính từ giai đoạn Analyze",
                height=150
            )
            
            if st.button("💾 Lưu Analysis Summary", key="save_analysis_summary"):
                self.db.save_dmaic_analyze(project_id, {'analysis_summary': analysis_summary})
                st.success("✅ Đã lưu!")
                st.rerun()
    
    # ==================== IMPROVE PHASE ====================
    def render_improve_phase(self, project_id):
        st.subheader("⚡ Improve Phase")
        
        improve_data = self.db.get_dmaic_improve(project_id) or {}
        
        # Solution Brainstorming
        with st.expander("💡 Solution Brainstorming", expanded=True):
            st.write("**Các giải pháp đề xuất**")
            
            # Load existing solutions
            solutions_list = []
            if improve_data.get('solutions_brainstormed'):
                try:
                    solutions_list = json.loads(improve_data['solutions_brainstormed'])
                except:
                    solutions_list = []
            
            # Add new solution
            with st.form("solution_form"):
                col1, col2 = st.columns(2)
                with col1:
                    solution_name = st.text_input("Tên giải pháp")
                    solution_type = st.selectbox("Loại", ["Quick Win", "Long-term", "Pilot Required"])
                
                with col2:
                    estimated_cost = st.number_input("Chi phí ước tính (VND)", min_value=0, value=0)
                    estimated_impact = st.selectbox("Tác động dự kiến", ["Cao", "Trung bình", "Thấp"])
                
                solution_description = st.text_area("Mô tả giải pháp", height=100)
                
                if st.form_submit_button("➕ Thêm giải pháp"):
                    solutions_list.append({
                        'name': solution_name,
                        'type': solution_type,
                        'cost': estimated_cost,
                        'impact': estimated_impact,
                        'description': solution_description,
                        'selected': False
                    })
                    self.db.save_dmaic_improve(project_id, {'solutions_brainstormed': json.dumps(solutions_list)})
                    st.success("✅ Đã thêm giải pháp!")
                    st.rerun()
            
            # Display and select solutions
            if solutions_list:
                st.write("**Danh sách giải pháp:**")
                for idx, sol in enumerate(solutions_list):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{sol['name']}** ({sol['type']})")
                        st.write(sol['description'])
                    with col2:
                        st.write(f"💰 {sol['cost']:,.0f} VND")
                        st.write(f"📊 Tác động: {sol['impact']}")
                    with col3:
                        selected = st.checkbox("Chọn", value=sol.get('selected', False), key=f"sel_sol_{idx}")
                        solutions_list[idx]['selected'] = selected
                    st.divider()
                
                if st.button("💾 Lưu lựa chọn", key="save_selections"):
                    self.db.save_dmaic_improve(project_id, {'solutions_brainstormed': json.dumps(solutions_list)})
                    st.success("✅ Đã lưu!")
                    st.rerun()
            
            selection_criteria = st.text_area(
                "Tiêu chí lựa chọn giải pháp",
                value=improve_data.get('selection_criteria', ''),
                placeholder="Mô tả các tiêu chí được sử dụng để lựa chọn giải pháp",
                height=100
            )
            
            if st.button("💾 Lưu Selection Criteria", key="save_criteria"):
                self.db.save_dmaic_improve(project_id, {'selection_criteria': selection_criteria})
                st.success("✅ Đã lưu!")
                st.rerun()
        
        # Pilot Testing
        with st.expander("🧪 Pilot Testing", expanded=False):
            st.write("**Thử nghiệm giải pháp**")
            
            pilot_plan = st.text_area(
                "Kế hoạch Pilot Test",
                value=improve_data.get('pilot_test_plan', ''),
                placeholder="Mô tả kế hoạch thử nghiệm: scope, timeline, success criteria",
                height=150
            )
            
            pilot_results = st.text_area(
                "Kết quả Pilot Test",
                value=improve_data.get('pilot_test_results', ''),
                placeholder="Kết quả và phát hiện từ pilot test",
                height=150
            )
            
            pilot_status = st.selectbox(
                "Trạng thái Pilot",
                ["Chưa bắt đầu", "Đang tiến hành", "Hoàn thành - Thành công", "Hoàn thành - Cần điều chỉnh"],
                index=0 if not improve_data.get('pilot_test_status') else 
                      ["Chưa bắt đầu", "Đang tiến hành", "Hoàn thành - Thành công", "Hoàn thành - Cần điều chỉnh"].index(improve_data.get('pilot_test_status', 'Chưa bắt đầu'))
            )
            
            if st.button("💾 Lưu Pilot Test", key="save_pilot"):
                pilot_data = {
                    'pilot_test_plan': pilot_plan,
                    'pilot_test_results': pilot_results,
                    'pilot_test_status': pilot_status
                }
                self.db.save_dmaic_improve(project_id, pilot_data)
                st.success("✅ Đã lưu!")
                st.rerun()
        
        # Before/After Comparison
        with st.expander("📊 Before/After Comparison", expanded=False):
            st.write("**So sánh Trước và Sau cải tiến**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**TRƯỚC cải tiến**")
                before_input = st.text_area(
                    "Dữ liệu Trước (mỗi giá trị một dòng)",
                    value=improve_data.get('before_data', ''),
                    height=150,
                    key="before_data"
                )
            
            with col2:
                st.write("**SAU cải tiến**")
                after_input = st.text_area(
                    "Dữ liệu Sau (mỗi giá trị một dòng)",
                    value=improve_data.get('after_data', ''),
                    height=150,
                    key="after_data"
                )
            
            if st.button("💾 Lưu Before/After Data", key="save_before_after"):
                comparison_data = {
                    'before_data': before_input,
                    'after_data': after_input
                }
                self.db.save_dmaic_improve(project_id, comparison_data)
                st.success("✅ Đã lưu!")
                st.rerun()
            
            # Visualize if data available
            if before_input and after_input:
                try:
                    before_values = [float(x.strip()) for x in before_input.split('\n') if x.strip()]
                    after_values = [float(x.strip()) for x in after_input.split('\n') if x.strip()]
                    
                    if before_values and after_values:
                        # Comparison metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            before_mean = sum(before_values) / len(before_values)
                            after_mean = sum(after_values) / len(after_values)
                            improvement = ((after_mean - before_mean) / before_mean) * 100
                            st.metric("Cải thiện (%)", f"{improvement:.1f}%")
                        
                        with col2:
                            st.metric("Trước (TB)", f"{before_mean:.2f}")
                        
                        with col3:
                            st.metric("Sau (TB)", f"{after_mean:.2f}")
                        
                        # Chart
                        fig = go.Figure()
                        fig.add_trace(go.Box(y=before_values, name='Trước', marker_color='lightblue'))
                        fig.add_trace(go.Box(y=after_values, name='Sau', marker_color='lightgreen'))
                        fig.update_layout(title='Before vs After Comparison', height=400)
                        st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Lỗi hiển thị: {e}")
    
    # ==================== CONTROL PHASE ====================
    def render_control_phase(self, project_id):
        st.subheader("🎯 Control Phase")
        
        control_data = self.db.get_dmaic_control(project_id) or {}
        
        # Control Plan
        with st.expander("📋 Control Plan", expanded=True):
            st.write("**Kế hoạch kiểm soát để duy trì cải tiến**")
            
            # Load existing control items
            control_items = []
            if control_data.get('control_plan'):
                try:
                    control_items = json.loads(control_data['control_plan'])
                except:
                    control_items = []
            
            # Add new control item
            with st.form("control_item_form"):
                col1, col2 = st.columns(2)
                with col1:
                    what_to_control = st.text_input("Cần kiểm soát gì")
                    how_to_measure = st.text_input("Cách đo lường")
                
                with col2:
                    frequency = st.selectbox("Tần suất", ["Hàng ngày", "Hàng tuần", "Hàng tháng", "Theo ca"])
                    responsible = st.text_input("Người chịu trách nhiệm")
                
                action_if_out = st.text_input("Hành động nếu vượt ngưỡng")
                
                if st.form_submit_button("➕ Thêm Control Item"):
                    control_items.append({
                        'what': what_to_control,
                        'how': how_to_measure,
                        'frequency': frequency,
                        'responsible': responsible,
                        'action': action_if_out
                    })
                    self.db.save_dmaic_control(project_id, {'control_plan': json.dumps(control_items)})
                    st.success("✅ Đã thêm!")
                    st.rerun()
            
            # Display control plan
            if control_items:
                st.write("**Control Plan:**")
                df = pd.DataFrame(control_items)
                st.dataframe(df, use_container_width=True)
            
            monitoring_freq = st.selectbox(
                "Tần suất review tổng thể",
                ["Hàng tuần", "Hai tuần một lần", "Hàng tháng", "Hàng quý"],
                index=0 if not control_data.get('monitoring_frequency') else
                      ["Hàng tuần", "Hai tuần một lần", "Hàng tháng", "Hàng quý"].index(control_data.get('monitoring_frequency', 'Hàng tuần'))
            )
            
            responsible_person = st.text_input(
                "Người chịu trách nhiệm chung",
                value=control_data.get('responsible_person', '')
            )
            
            if st.button("💾 Lưu Control Plan Settings", key="save_control_settings"):
                settings_data = {
                    'monitoring_frequency': monitoring_freq,
                    'responsible_person': responsible_person
                }
                self.db.save_dmaic_control(project_id, settings_data)
                st.success("✅ Đã lưu!")
                st.rerun()
        
        # SOPs
        with st.expander("📄 Standard Operating Procedures (SOPs)", expanded=False):
            st.write("**Quy trình vận hành chuẩn**")
            
            # Load existing SOPs
            sop_list = []
            if control_data.get('sop_documents'):
                try:
                    sop_list = json.loads(control_data['sop_documents'])
                except:
                    sop_list = []
            
            # Add new SOP
            with st.form("sop_form"):
                col1, col2 = st.columns(2)
                with col1:
                    sop_name = st.text_input("Tên SOP")
                    sop_version = st.text_input("Phiên bản", value="1.0")
                
                with col2:
                    sop_owner = st.text_input("Người quản lý SOP")
                    sop_date = st.date_input("Ngày phê duyệt")
                
                sop_description = st.text_area("Mô tả SOP", height=100)
                sop_location = st.text_input("Vị trí lưu trữ", placeholder="Link tới document hoặc file path")
                
                if st.form_submit_button("➕ Thêm SOP"):
                    sop_list.append({
                        'name': sop_name,
                        'version': sop_version,
                        'owner': sop_owner,
                        'date': str(sop_date),
                        'description': sop_description,
                        'location': sop_location
                    })
                    self.db.save_dmaic_control(project_id, {'sop_documents': json.dumps(sop_list)})
                    st.success("✅ Đã thêm SOP!")
                    st.rerun()
            
            # Display SOPs
            if sop_list:
                st.write("**Danh sách SOPs:**")
                for idx, sop in enumerate(sop_list):
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**{sop['name']}** (v{sop['version']})")
                            st.write(sop['description'])
                            st.write(f"📁 {sop['location']}")
                        with col2:
                            st.write(f"👤 {sop['owner']}")
                            st.write(f"📅 {sop['date']}")
                        st.divider()
            
            sop_training = st.text_area(
                "Trạng thái đào tạo SOP",
                value=control_data.get('sop_training_status', ''),
                placeholder="Mô tả tiến độ đào tạo nhân viên về các SOP mới",
                height=100
            )
            
            if st.button("💾 Lưu SOP Training Status", key="save_sop_training"):
                self.db.save_dmaic_control(project_id, {'sop_training_status': sop_training})
                st.success("✅ Đã lưu!")
                st.rerun()
        
        # Sustainability Plan
        with st.expander("♻️ Sustainability & Monitoring", expanded=False):
            st.write("**Kế hoạch duy trì cải tiến lâu dài**")
            
            sustainability_plan = st.text_area(
                "Kế hoạch Sustainability",
                value=control_data.get('sustainability_plan', ''),
                placeholder="Mô tả cách duy trì cải tiến: communication plan, audit schedule, continuous improvement, etc.",
                height=200
            )
            
            if st.button("💾 Lưu Sustainability Plan", key="save_sustainability"):
                self.db.save_dmaic_control(project_id, {'sustainability_plan': sustainability_plan})
                st.success("✅ Đã lưu!")
                st.rerun()
            
            st.info("💡 Đừng quên cập nhật monitoring metrics thường xuyên để đảm bảo cải tiến được duy trì!")

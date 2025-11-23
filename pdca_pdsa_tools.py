"""
PDCA/PDSA Tools - Ultra Clean Version
ZERO database dependencies - Uses ONLY session state
"""

import streamlit as st
from datetime import datetime


class PDCATools:
    """
    Ultra-simplified PDCA/PDSA tracking tools
    NO database calls - uses ONLY session state
    """
    
    def __init__(self, db):
        """Initialize - db parameter ignored, kept for compatibility"""
        self.db = db  # Stored but not used
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state for PDCA data"""
        if 'pdca_simple_data' not in st.session_state:
            st.session_state.pdca_simple_data = {}
    
    def _make_key(self, project_id, methodology, phase):
        """Generate unique key for session state"""
        return f"pdca_{project_id}_{methodology}_{phase}"
    
    def _get_phase_data(self, project_id, methodology, phase):
        """Get data from session state - NO database calls"""
        key = self._make_key(project_id, methodology, phase)
        return st.session_state.pdca_simple_data.get(key, {})
    
    def _save_phase_data(self, project_id, methodology, phase, data):
        """Save data to session state - NO database calls"""
        key = self._make_key(project_id, methodology, phase)
        st.session_state.pdca_simple_data[key] = data
        return True
    
    def render_pdca_interface(self, project_id, methodology):
        """Main PDCA/PDSA interface"""
        st.write(f"## 🔄 {methodology} Tracking")
        
        # Phase info
        if methodology == 'PDCA':
            phases = ['Plan', 'Do', 'Check', 'Act']
            st.info("📋 PDCA: Plan → Do → Check → Act (Deming Cycle)")
        else:  # PDSA
            phases = ['Plan', 'Do', 'Study', 'Act']
            st.info("📋 PDSA: Plan → Do → Study → Act (Quality Improvement)")
        
        # Create tabs
        tabs = st.tabs([f"📌 {phase}" for phase in phases])
        
        # Render each phase
        for idx, phase in enumerate(phases):
            with tabs[idx]:
                self._render_phase_form(project_id, methodology, phase)
    
    def _render_phase_form(self, project_id, methodology, phase):
        """Render form for a specific phase"""
        st.write(f"### {phase} Phase")
        
        # Get existing data
        data = self._get_phase_data(project_id, methodology, phase)
        
        # Create form
        with st.form(f"pdca_form_{project_id}_{phase}"):
            # Main content
            st.write("#### 📝 Nội dung chính")
            content = st.text_area(
                "Mô tả chi tiết",
                value=data.get('content', ''),
                height=150,
                placeholder=f"Nhập nội dung cho {phase} phase..."
            )
            
            # Status and progress
            col1, col2 = st.columns(2)
            with col1:
                status = st.selectbox(
                    "Trạng thái",
                    ['Chưa bắt đầu', 'Đang thực hiện', 'Hoàn thành'],
                    index=['Chưa bắt đầu', 'Đang thực hiện', 'Hoàn thành'].index(
                        data.get('status', 'Chưa bắt đầu')
                    )
                )
            with col2:
                progress = st.slider(
                    "Tiến độ (%)",
                    0, 100,
                    value=data.get('progress', 0)
                )
            
            # Phase-specific fields
            st.write(f"#### 📋 Thông tin {phase}")
            
            if phase == 'Plan':
                problem = st.text_area(
                    "Vấn đề cần giải quyết",
                    value=data.get('problem', ''),
                    height=100
                )
                goal = st.text_area(
                    "Mục tiêu",
                    value=data.get('goal', ''),
                    height=100
                )
                actions = st.text_area(
                    "Kế hoạch hành động",
                    value=data.get('actions', ''),
                    height=100
                )
            
            elif phase == 'Do':
                implementation = st.text_area(
                    "Hoạt động đã thực hiện",
                    value=data.get('implementation', ''),
                    height=100
                )
                observations = st.text_area(
                    "Quan sát và phát hiện",
                    value=data.get('observations', ''),
                    height=100
                )
            
            elif phase in ['Check', 'Study']:
                results = st.text_area(
                    "Kết quả đạt được",
                    value=data.get('results', ''),
                    height=100
                )
                analysis = st.text_area(
                    "Phân tích và đánh giá",
                    value=data.get('analysis', ''),
                    height=100
                )
                lessons = st.text_area(
                    "Bài học kinh nghiệm",
                    value=data.get('lessons', ''),
                    height=100
                )
            
            elif phase == 'Act':
                next_actions = st.text_area(
                    "Hành động tiếp theo",
                    value=data.get('next_actions', ''),
                    height=100
                )
                standardization = st.text_area(
                    "Tiêu chuẩn hóa",
                    value=data.get('standardization', ''),
                    height=100
                )
            
            # Notes
            st.write("#### 📎 Ghi chú & Tài liệu")
            notes = st.text_area(
                "Ghi chú thêm",
                value=data.get('notes', ''),
                height=80,
                placeholder="Ghi chú, link tài liệu, v.v..."
            )
            
            # Submit button
            submitted = st.form_submit_button("💾 Lưu", type="primary")
            
            if submitted:
                # Prepare data
                save_data = {
                    'content': content,
                    'status': status,
                    'progress': progress,
                    'notes': notes,
                    'updated_at': datetime.now().isoformat()
                }
                
                # Add phase-specific data
                if phase == 'Plan':
                    save_data.update({
                        'problem': problem,
                        'goal': goal,
                        'actions': actions
                    })
                elif phase == 'Do':
                    save_data.update({
                        'implementation': implementation,
                        'observations': observations
                    })
                elif phase in ['Check', 'Study']:
                    save_data.update({
                        'results': results,
                        'analysis': analysis,
                        'lessons': lessons
                    })
                elif phase == 'Act':
                    save_data.update({
                        'next_actions': next_actions,
                        'standardization': standardization
                    })
                
                # Save to session state
                if self._save_phase_data(project_id, methodology, phase, save_data):
                    st.success(f"✅ Đã lưu {phase} phase!")
                    st.rerun()
                else:
                    st.error("❌ Lỗi khi lưu dữ liệu")
        
        # Display current status
        if data:
            st.markdown("---")
            st.write("#### 📊 Trạng thái hiện tại")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Trạng thái", data.get('status', 'N/A'))
            with col2:
                st.metric("Tiến độ", f"{data.get('progress', 0)}%")
            with col3:
                updated = data.get('updated_at', 'Chưa cập nhật')
                if updated != 'Chưa cập nhật':
                    try:
                        dt = datetime.fromisoformat(updated)
                        updated = dt.strftime('%d/%m/%Y %H:%M')
                    except:
                        pass
                st.metric("Cập nhật", updated)


# ==================== NOTES ====================
"""
ULTRA CLEAN VERSION:
- ZERO database calls
- Uses ONLY session state
- NO external dependencies
- Guaranteed to work

Data Storage:
- st.session_state.pdca_simple_data
- Key format: pdca_{project_id}_{methodology}_{phase}
- Data persists during session only

Limitations:
- Data lost on refresh
- No permanent storage
- Basic features only

Perfect for:
- Quick fix
- Testing
- Temporary solution
"""

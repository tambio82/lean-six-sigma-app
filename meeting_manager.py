"""
Meeting Manager Module
Handles meeting minutes, action items, and decision log
"""

from datetime import datetime
from typing import List, Dict, Optional
import json
import streamlit as st

class MeetingManager:
    """
    Manage meeting minutes, action items, and decisions
    """
    
    def __init__(self, database, activity_tracker=None):
        """
        Initialize meeting manager
        
        Args:
            database: ProjectDatabase instance
            activity_tracker: ActivityTracker instance (optional)
        """
        self.db = database
        self.activity_tracker = activity_tracker
    
    def add_meeting(self, project_id: int, meeting_data: Dict) -> bool:
        """
        Add meeting minutes
        
        Args:
            project_id: Project ID
            meeting_data: Dict with meeting details
        
        Returns:
            bool: Success status
        """
        try:
            # Add project_id and timestamp
            meeting_data['project_id'] = project_id
            meeting_data['created_at'] = datetime.now().isoformat()
            
            success = self.db.add_meeting_minutes(meeting_data)
            
            if success and self.activity_tracker:
                meeting_date = meeting_data.get('meeting_date', '')
                self.activity_tracker.log_meeting_added(
                    project_id,
                    meeting_data.get('created_by', 'Unknown'),
                    meeting_date
                )
                
                # Log decisions
                decisions = meeting_data.get('decisions', [])
                for decision in decisions:
                    if isinstance(decision, dict):
                        dec_text = decision.get('description', '')
                    else:
                        dec_text = str(decision)
                    
                    if dec_text:
                        self.activity_tracker.log_decision_made(
                            project_id,
                            meeting_data.get('created_by', 'Unknown'),
                            dec_text
                        )
            
            return success
        
        except Exception as e:
            print(f"Error adding meeting: {e}")
            return False
    
    def get_meetings(self, project_id: int) -> List[Dict]:
        """
        Get all meetings for a project
        
        Args:
            project_id: Project ID
        
        Returns:
            List of meeting dicts
        """
        try:
            meetings = self.db.get_meeting_minutes(project_id)
            return meetings if meetings else []
        except Exception as e:
            print(f"Error getting meetings: {e}")
            return []
    
    def get_meeting_by_id(self, meeting_id: int) -> Optional[Dict]:
        """Get a specific meeting by ID"""
        try:
            return self.db.get_meeting_by_id(meeting_id)
        except Exception as e:
            print(f"Error getting meeting: {e}")
            return None
    
    def update_meeting(self, meeting_id: int, meeting_data: Dict) -> bool:
        """Update meeting minutes"""
        try:
            return self.db.update_meeting_minutes(meeting_id, meeting_data)
        except Exception as e:
            print(f"Error updating meeting: {e}")
            return False
    
    def delete_meeting(self, meeting_id: int) -> bool:
        """Delete meeting minutes"""
        try:
            return self.db.delete_meeting_minutes(meeting_id)
        except Exception as e:
            print(f"Error deleting meeting: {e}")
            return False
    
    def get_action_items(self, project_id: int, status: str = None) -> List[Dict]:
        """
        Get action items from all meetings
        
        Args:
            project_id: Project ID
            status: Filter by status (optional)
        
        Returns:
            List of action item dicts
        """
        try:
            meetings = self.get_meetings(project_id)
            all_action_items = []
            
            for meeting in meetings:
                meeting_date = meeting.get('meeting_date', '')
                action_items_json = meeting.get('action_items', '[]')
                
                # Parse JSON
                try:
                    if isinstance(action_items_json, str):
                        action_items = json.loads(action_items_json)
                    else:
                        action_items = action_items_json
                except:
                    action_items = []
                
                # Add meeting context to each action item
                for item in action_items:
                    if isinstance(item, dict):
                        item['meeting_id'] = meeting.get('id')
                        item['meeting_date'] = meeting_date
                        
                        # Filter by status if specified
                        if status is None or item.get('status') == status:
                            all_action_items.append(item)
            
            return all_action_items
        
        except Exception as e:
            print(f"Error getting action items: {e}")
            return []
    
    def get_decisions(self, project_id: int) -> List[Dict]:
        """
        Get all decisions from meetings
        
        Args:
            project_id: Project ID
        
        Returns:
            List of decision dicts
        """
        try:
            meetings = self.get_meetings(project_id)
            all_decisions = []
            
            for meeting in meetings:
                meeting_date = meeting.get('meeting_date', '')
                decisions_json = meeting.get('decisions', '[]')
                
                # Parse JSON
                try:
                    if isinstance(decisions_json, str):
                        decisions = json.loads(decisions_json)
                    else:
                        decisions = decisions_json
                except:
                    decisions = []
                
                # Add meeting context
                for decision in decisions:
                    if isinstance(decision, dict):
                        decision['meeting_id'] = meeting.get('id')
                        decision['meeting_date'] = meeting_date
                        all_decisions.append(decision)
            
            return all_decisions
        
        except Exception as e:
            print(f"Error getting decisions: {e}")
            return []


# ==================== UI COMPONENTS ====================

def render_meeting_minutes_section(project_id: int, current_user: str,
                                   meeting_manager: MeetingManager):
    """
    Render meeting minutes section UI
    
    Args:
        project_id: Project ID
        current_user: Current user name
        meeting_manager: MeetingManager instance
    """
    st.subheader("🗓️ Biên bản Họp")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs([
        "📋 Tất cả biên bản",
        "📌 Action Items",
        "✅ Decision Log"
    ])
    
    with tab1:
        render_meetings_list(project_id, current_user, meeting_manager)
    
    with tab2:
        render_action_items_dashboard(project_id, meeting_manager)
    
    with tab3:
        render_decision_log(project_id, meeting_manager)


def render_meetings_list(project_id: int, current_user: str,
                         meeting_manager: MeetingManager):
    """Render list of meetings with add button"""
    
    # Add new meeting button
    if st.button("➕ Thêm biên bản họp mới", type="primary"):
        st.session_state['show_meeting_form'] = True
    
    # Show form if requested
    if st.session_state.get('show_meeting_form', False):
        render_meeting_form(project_id, current_user, meeting_manager)
    
    # Display meetings
    st.markdown("---")
    meetings = meeting_manager.get_meetings(project_id)
    
    if not meetings:
        st.info("Chưa có biên bản họp nào.")
    else:
        # Sort by date
        meetings_sorted = sorted(
            meetings,
            key=lambda x: x.get('meeting_date', ''),
            reverse=True
        )
        
        for meeting in meetings_sorted:
            render_meeting_card(meeting, meeting_manager)


def render_meeting_form(project_id: int, current_user: str,
                       meeting_manager: MeetingManager):
    """Render form to add/edit meeting"""
    
    with st.form("meeting_form", clear_on_submit=True):
        st.write("### Thêm Biên bản Họp")
        
        col1, col2 = st.columns(2)
        
        with col1:
            meeting_title = st.text_input("Chủ đề cuộc họp *")
            meeting_date = st.date_input("Ngày họp *")
            meeting_time = st.time_input("Thời gian")
        
        with col2:
            location = st.text_input("Địa điểm", placeholder="Phòng họp 301 / Zoom")
            duration = st.number_input("Thời lượng (phút)", min_value=15, value=60)
        
        # Attendees
        st.write("**Người tham dự**")
        attendees = st.text_area(
            "Danh sách người tham dự",
            placeholder="Nhập tên, cách nhau bởi dấu phẩy\nVD: Nguyen Van A, Tran Thi B, Le Van C",
            height=80
        )
        
        # Agenda
        st.write("**Nội dung họp**")
        agenda = st.text_area(
            "Chương trình nghị sự",
            placeholder="1. Review tiến độ dự án\n2. Thảo luận vấn đề X\n3. Quyết định Y",
            height=100
        )
        
        # Notes
        notes = st.text_area(
            "Ghi chú & thảo luận",
            placeholder="Tóm tắt các điểm thảo luận chính...",
            height=150
        )
        
        # Action Items
        st.write("**Action Items**")
        num_actions = st.number_input("Số lượng action items", min_value=0, max_value=10, value=0)
        
        action_items = []
        for i in range(num_actions):
            with st.expander(f"Action Item #{i+1}"):
                action_desc = st.text_input(f"Mô tả #{i+1}", key=f"action_desc_{i}")
                action_owner = st.text_input(f"Người phụ trách #{i+1}", key=f"action_owner_{i}")
                action_due = st.date_input(f"Deadline #{i+1}", key=f"action_due_{i}")
                action_status = st.selectbox(
                    f"Trạng thái #{i+1}",
                    ["Not Started", "In Progress", "Completed"],
                    key=f"action_status_{i}"
                )
                
                if action_desc:
                    action_items.append({
                        'description': action_desc,
                        'owner': action_owner,
                        'due_date': action_due.isoformat(),
                        'status': action_status
                    })
        
        # Decisions
        st.write("**Quyết định**")
        num_decisions = st.number_input("Số lượng quyết định", min_value=0, max_value=10, value=0)
        
        decisions = []
        for i in range(num_decisions):
            with st.expander(f"Quyết định #{i+1}"):
                dec_desc = st.text_area(f"Nội dung quyết định #{i+1}", key=f"dec_desc_{i}")
                dec_maker = st.text_input(f"Người quyết định #{i+1}", key=f"dec_maker_{i}")
                dec_rationale = st.text_area(f"Lý do #{i+1}", key=f"dec_rationale_{i}")
                
                if dec_desc:
                    decisions.append({
                        'description': dec_desc,
                        'decision_maker': dec_maker,
                        'rationale': dec_rationale
                    })
        
        # Submit buttons
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("💾 Lưu biên bản", type="primary")
        with col2:
            cancel = st.form_submit_button("❌ Hủy")
        
        if cancel:
            st.session_state['show_meeting_form'] = False
            st.rerun()
        
        if submit:
            if not meeting_title or not meeting_date:
                st.error("⚠️ Vui lòng nhập chủ đề và ngày họp!")
            else:
                meeting_data = {
                    'meeting_title': meeting_title,
                    'meeting_date': meeting_date.isoformat(),
                    'meeting_time': str(meeting_time),
                    'location': location,
                    'duration_minutes': duration,
                    'attendees': attendees,
                    'agenda': agenda,
                    'notes': notes,
                    'action_items': json.dumps(action_items),
                    'decisions': json.dumps(decisions),
                    'created_by': current_user
                }
                
                success = meeting_manager.add_meeting(project_id, meeting_data)
                
                if success:
                    st.success("✅ Đã lưu biên bản họp!")
                    st.session_state['show_meeting_form'] = False
                    st.rerun()
                else:
                    st.error("❌ Lỗi khi lưu biên bản")


def render_meeting_card(meeting: Dict, meeting_manager: MeetingManager):
    """Render a single meeting card"""
    
    meeting_id = meeting.get('id')
    title = meeting.get('meeting_title', 'Untitled Meeting')
    date = meeting.get('meeting_date', '')
    location = meeting.get('location', 'N/A')
    
    with st.expander(f"📅 {title} - {date}"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**Ngày:** {date}")
            st.write(f"**Thời gian:** {meeting.get('meeting_time', 'N/A')}")
            st.write(f"**Địa điểm:** {location}")
            st.write(f"**Thời lượng:** {meeting.get('duration_minutes', 0)} phút")
        
        with col2:
            if st.button("🗑️ Xóa", key=f"del_meeting_{meeting_id}"):
                if meeting_manager.delete_meeting(meeting_id):
                    st.success("✅ Đã xóa!")
                    st.rerun()
        
        # Attendees
        st.write("**Người tham dự:**")
        st.write(meeting.get('attendees', 'N/A'))
        
        # Agenda
        st.write("**Nội dung:**")
        st.write(meeting.get('agenda', 'N/A'))
        
        # Notes
        st.write("**Ghi chú:**")
        st.write(meeting.get('notes', 'N/A'))
        
        # Action Items
        action_items_json = meeting.get('action_items', '[]')
        try:
            action_items = json.loads(action_items_json) if isinstance(action_items_json, str) else action_items_json
        except:
            action_items = []
        
        if action_items:
            st.write(f"**Action Items:** ({len(action_items)})")
            for item in action_items:
                if isinstance(item, dict):
                    status_icon = "✅" if item.get('status') == 'Completed' else "📌"
                    st.write(f"{status_icon} {item.get('description')} (Owner: {item.get('owner')})")
        
        # Decisions
        decisions_json = meeting.get('decisions', '[]')
        try:
            decisions = json.loads(decisions_json) if isinstance(decisions_json, str) else decisions_json
        except:
            decisions = []
        
        if decisions:
            st.write(f"**Quyết định:** ({len(decisions)})")
            for decision in decisions:
                if isinstance(decision, dict):
                    st.write(f"✅ {decision.get('description')}")


def render_action_items_dashboard(project_id: int, meeting_manager: MeetingManager):
    """Render action items dashboard"""
    
    st.write("### 📌 Action Items Dashboard")
    
    # Get all action items
    action_items = meeting_manager.get_action_items(project_id)
    
    if not action_items:
        st.info("Chưa có action items nào.")
        return
    
    # Filter options
    status_filter = st.selectbox(
        "Lọc theo trạng thái",
        ["All", "Not Started", "In Progress", "Completed"]
    )
    
    # Filter items
    if status_filter != "All":
        filtered_items = [item for item in action_items if item.get('status') == status_filter]
    else:
        filtered_items = action_items
    
    # Display count
    st.metric("Tổng số Action Items", len(filtered_items))
    
    # Display items in table
    if filtered_items:
        for item in filtered_items:
            status_icon = {"Not Started": "⏸️", "In Progress": "🔄", "Completed": "✅"}.get(item.get('status'), "📌")
            
            st.write(f"{status_icon} **{item.get('description')}**")
            st.caption(f"Owner: {item.get('owner')} | Due: {item.get('due_date')} | Meeting: {item.get('meeting_date')}")
            st.markdown("---")


def render_decision_log(project_id: int, meeting_manager: MeetingManager):
    """Render decision log"""
    
    st.write("### ✅ Decision Log")
    
    # Get all decisions
    decisions = meeting_manager.get_decisions(project_id)
    
    if not decisions:
        st.info("Chưa có quyết định nào được ghi nhận.")
        return
    
    st.metric("Tổng số Quyết định", len(decisions))
    
    # Display decisions
    for i, decision in enumerate(decisions, 1):
        with st.expander(f"Quyết định #{i} - {decision.get('meeting_date')}"):
            st.write(f"**Nội dung:** {decision.get('description')}")
            st.write(f"**Người quyết định:** {decision.get('decision_maker', 'N/A')}")
            st.write(f"**Lý do:** {decision.get('rationale', 'N/A')}")
            st.write(f"**Ngày họp:** {decision.get('meeting_date')}")

"""
Module Meeting Minutes Management
Quản lý meeting notes, action items, và decision log
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

class MeetingManager:
    """
    Quản lý meetings, meeting minutes, và action items
    """
    
    def __init__(self, db, collaboration_manager=None):
        """
        Initialize meeting manager
        
        Args:
            db: ProjectDatabase instance
            collaboration_manager: CollaborationManager instance (optional)
        """
        self.db = db
        self.collaboration_manager = collaboration_manager
    
    # ===== MEETINGS =====
    
    def create_meeting(self, project_id, meeting_title, meeting_date, duration,
                      location, attendees, agenda, created_by):
        """
        Create a new meeting
        
        Args:
            project_id: Project ID
            meeting_title: Meeting title
            meeting_date: Meeting date (datetime or string)
            duration: Duration in minutes
            location: Meeting location
            attendees: List of attendee names or comma-separated string
            agenda: Meeting agenda
            created_by: Creator name
        
        Returns:
            int: Meeting ID
        """
        # Convert attendees to string if list
        if isinstance(attendees, list):
            attendees = ','.join(attendees)
        
        meeting_data = {
            'project_id': project_id,
            'meeting_title': meeting_title,
            'meeting_date': meeting_date if isinstance(meeting_date, str) else meeting_date.isoformat(),
            'duration': duration,
            'location': location,
            'attendees': attendees,
            'agenda': agenda,
            'minutes': None,  # Will be filled later
            'decisions': None,  # Will be filled later
            'created_by': created_by
        }
        
        meeting_id = self.db.add_meeting(meeting_data)
        
        # Log activity
        if self.collaboration_manager:
            self.collaboration_manager.log_activity(
                project_id=project_id,
                user_name=created_by,
                user_email='',
                activity_type='meeting_created',
                activity_description=f"Đã tạo meeting: {meeting_title}",
                entity_type='meeting',
                entity_id=meeting_id
            )
        
        return meeting_id
    
    def update_meeting_minutes(self, meeting_id, minutes, decisions, updated_by):
        """
        Update meeting minutes and decisions
        
        Args:
            meeting_id: Meeting ID
            minutes: Meeting minutes text
            decisions: Decisions made (text or JSON)
            updated_by: Updater name
        """
        meeting_data = {
            'minutes': minutes,
            'decisions': decisions
        }
        
        self.db.update_meeting(meeting_id, meeting_data)
        
        # Get meeting info for logging
        meeting = self.db.get_meeting(meeting_id)
        if not meeting.empty and self.collaboration_manager:
            project_id = meeting.iloc[0]['project_id']
            self.collaboration_manager.log_activity(
                project_id=project_id,
                user_name=updated_by,
                user_email='',
                activity_type='meeting_updated',
                activity_description=f"Đã cập nhật meeting minutes",
                entity_type='meeting',
                entity_id=meeting_id
            )
    
    def get_meetings(self, project_id):
        """
        Get all meetings for a project
        
        Args:
            project_id: Project ID
        
        Returns:
            DataFrame: Meetings data
        """
        return self.db.get_meetings(project_id)
    
    def get_meeting(self, meeting_id):
        """
        Get a specific meeting
        
        Args:
            meeting_id: Meeting ID
        
        Returns:
            DataFrame: Meeting data
        """
        return self.db.get_meeting(meeting_id)
    
    def delete_meeting(self, meeting_id, deleted_by):
        """
        Delete a meeting
        """
        # Get meeting info before deleting
        meeting = self.db.get_meeting(meeting_id)
        
        if not meeting.empty:
            project_id = meeting.iloc[0]['project_id']
            meeting_title = meeting.iloc[0]['meeting_title']
            
            self.db.delete_meeting(meeting_id)
            
            # Log activity
            if self.collaboration_manager:
                self.collaboration_manager.log_activity(
                    project_id=project_id,
                    user_name=deleted_by,
                    user_email='',
                    activity_type='meeting_deleted',
                    activity_description=f"Đã xóa meeting: {meeting_title}",
                    entity_type='meeting',
                    entity_id=meeting_id
                )
    
    # ===== ACTION ITEMS =====
    
    def create_action_item(self, meeting_id, project_id, item_description, 
                          assigned_to, due_date, priority='Medium', notes=None):
        """
        Create a new action item
        
        Args:
            meeting_id: Meeting ID
            project_id: Project ID
            item_description: Action item description
            assigned_to: Person assigned to
            due_date: Due date
            priority: Priority (High/Medium/Low)
            notes: Additional notes
        
        Returns:
            int: Action item ID
        """
        action_data = {
            'meeting_id': meeting_id,
            'project_id': project_id,
            'item_description': item_description,
            'assigned_to': assigned_to,
            'due_date': due_date if isinstance(due_date, str) else due_date.isoformat(),
            'status': 'Open',
            'priority': priority,
            'notes': notes
        }
        
        action_id = self.db.add_action_item(action_data)
        
        # Log activity
        if self.collaboration_manager:
            self.collaboration_manager.log_activity(
                project_id=project_id,
                user_name='System',
                user_email='',
                activity_type='action_item_created',
                activity_description=f"Đã tạo action item cho {assigned_to}: {item_description[:50]}...",
                entity_type='action_item',
                entity_id=action_id
            )
        
        return action_id
    
    def update_action_item_status(self, action_id, status, notes=None, updated_by=None):
        """
        Update action item status
        
        Args:
            action_id: Action item ID
            status: New status (Open/In Progress/Completed/Cancelled)
            notes: Update notes
            updated_by: Person who updated
        """
        update_data = {'status': status}
        
        if notes:
            update_data['notes'] = notes
        
        self.db.update_action_item(action_id, update_data)
        
        # Log activity
        if self.collaboration_manager and updated_by:
            # Get action item info
            all_items = self.db.get_action_items()
            item = all_items[all_items['id'] == action_id]
            
            if not item.empty:
                project_id = item.iloc[0]['project_id']
                self.collaboration_manager.log_activity(
                    project_id=project_id,
                    user_name=updated_by,
                    user_email='',
                    activity_type='action_item_updated',
                    activity_description=f"Đã cập nhật action item: {status}",
                    entity_type='action_item',
                    entity_id=action_id
                )
    
    def get_action_items(self, meeting_id=None, project_id=None, status=None):
        """
        Get action items
        
        Args:
            meeting_id: Filter by meeting ID
            project_id: Filter by project ID
            status: Filter by status
        
        Returns:
            DataFrame: Action items
        """
        return self.db.get_action_items(meeting_id, project_id, status)
    
    def get_overdue_action_items(self, project_id=None):
        """
        Get overdue action items
        
        Args:
            project_id: Filter by project ID
        
        Returns:
            DataFrame: Overdue action items
        """
        all_items = self.get_action_items(project_id=project_id, status='Open')
        
        if all_items.empty:
            return all_items
        
        today = datetime.now().date()
        all_items['due_date_dt'] = pd.to_datetime(all_items['due_date']).dt.date
        
        overdue = all_items[all_items['due_date_dt'] < today]
        
        return overdue
    
    def delete_action_item(self, action_id, deleted_by):
        """
        Delete an action item
        """
        # Get info before deleting
        all_items = self.db.get_action_items()
        item = all_items[all_items['id'] == action_id]
        
        if not item.empty:
            project_id = item.iloc[0]['project_id']
            
            self.db.delete_action_item(action_id)
            
            # Log activity
            if self.collaboration_manager:
                self.collaboration_manager.log_activity(
                    project_id=project_id,
                    user_name=deleted_by,
                    user_email='',
                    activity_type='action_item_deleted',
                    activity_description=f"Đã xóa action item",
                    entity_type='action_item',
                    entity_id=action_id
                )
    
    # ===== UI RENDERING =====
    
    def render_meetings_page(self, project_id, current_user='User'):
        """
        Render complete meetings page for a project
        
        Args:
            project_id: Project ID
            current_user: Current user name
        """
        st.header("📅 Quản lý Meetings")
        
        # Tabs
        tab1, tab2, tab3 = st.tabs(["📋 Danh sách Meetings", "➕ Tạo Meeting Mới", "✅ Action Items"])
        
        with tab1:
            self._render_meetings_list(project_id, current_user)
        
        with tab2:
            self._render_create_meeting_form(project_id, current_user)
        
        with tab3:
            self._render_action_items(project_id, current_user)
    
    def _render_meetings_list(self, project_id, current_user):
        """Render list of meetings"""
        st.subheader("Danh sách Meetings")
        
        meetings = self.get_meetings(project_id)
        
        if meetings.empty:
            st.info("Chưa có meeting nào. Tạo meeting đầu tiên!")
            return
        
        # Sort by date
        meetings['meeting_date_dt'] = pd.to_datetime(meetings['meeting_date'])
        meetings = meetings.sort_values('meeting_date_dt', ascending=False)
        
        for _, meeting in meetings.iterrows():
            with st.expander(f"📅 {meeting['meeting_title']} - {pd.to_datetime(meeting['meeting_date']).strftime('%d/%m/%Y')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Ngày:** {pd.to_datetime(meeting['meeting_date']).strftime('%d/%m/%Y %H:%M')}")
                    st.write(f"**Thời lượng:** {meeting['duration']} phút")
                    st.write(f"**Địa điểm:** {meeting['location']}")
                
                with col2:
                    st.write(f"**Người tạo:** {meeting['created_by']}")
                    st.write(f"**Tạo lúc:** {pd.to_datetime(meeting['created_at']).strftime('%d/%m/%Y %H:%M')}")
                
                st.markdown("---")
                
                # Attendees
                st.write("**👥 Người tham dự:**")
                if meeting['attendees']:
                    attendees_list = meeting['attendees'].split(',')
                    st.write(", ".join(attendees_list))
                
                # Agenda
                st.write("**📋 Chương trình:**")
                st.write(meeting['agenda'])
                
                st.markdown("---")
                
                # Minutes
                st.write("**📝 Biên bản:**")
                if pd.notna(meeting['minutes']) and meeting['minutes']:
                    st.write(meeting['minutes'])
                    
                    # Edit minutes button
                    if st.button("✏️ Sửa biên bản", key=f"edit_minutes_{meeting['id']}"):
                        st.session_state[f'editing_minutes_{meeting["id"]}'] = True
                else:
                    st.info("Chưa có biên bản meeting")
                    if st.button("📝 Thêm biên bản", key=f"add_minutes_{meeting['id']}"):
                        st.session_state[f'editing_minutes_{meeting["id"]}'] = True
                
                # Edit form
                if st.session_state.get(f'editing_minutes_{meeting["id"]}', False):
                    minutes_text = st.text_area(
                        "Biên bản meeting",
                        value=meeting['minutes'] if pd.notna(meeting['minutes']) else '',
                        height=150,
                        key=f"minutes_text_{meeting['id']}"
                    )
                    
                    decisions_text = st.text_area(
                        "Quyết định",
                        value=meeting['decisions'] if pd.notna(meeting['decisions']) else '',
                        height=100,
                        key=f"decisions_text_{meeting['id']}"
                    )
                    
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.button("💾 Lưu", key=f"save_minutes_{meeting['id']}"):
                            self.update_meeting_minutes(
                                meeting['id'],
                                minutes_text,
                                decisions_text,
                                current_user
                            )
                            del st.session_state[f'editing_minutes_{meeting["id"]}']
                            st.success("✅ Đã lưu biên bản!")
                            st.rerun()
                    
                    with col_cancel:
                        if st.button("❌ Hủy", key=f"cancel_minutes_{meeting['id']}"):
                            del st.session_state[f'editing_minutes_{meeting["id"]}']
                            st.rerun()
                
                st.markdown("---")
                
                # Decisions
                if pd.notna(meeting['decisions']) and meeting['decisions']:
                    st.write("**📌 Quyết định:**")
                    st.write(meeting['decisions'])
                
                # Action items for this meeting
                st.markdown("---")
                st.write("**✅ Action Items:**")
                action_items = self.get_action_items(meeting_id=meeting['id'])
                
                if not action_items.empty:
                    self._render_action_items_table(action_items, show_meeting=False)
                else:
                    st.info("Chưa có action item nào")
                
                # Add action item button
                if st.button("➕ Thêm Action Item", key=f"add_action_{meeting['id']}"):
                    st.session_state[f'adding_action_{meeting["id"]}'] = True
                
                # Add action item form
                if st.session_state.get(f'adding_action_{meeting["id"]}', False):
                    self._render_add_action_item_form(meeting['id'], project_id, current_user)
                
                # Delete meeting
                st.markdown("---")
                if st.button("🗑️ Xóa Meeting", key=f"delete_meeting_{meeting['id']}", type="secondary"):
                    self.delete_meeting(meeting['id'], current_user)
                    st.success("✅ Đã xóa meeting!")
                    st.rerun()
    
    def _render_create_meeting_form(self, project_id, current_user):
        """Render create meeting form"""
        st.subheader("Tạo Meeting Mới")
        
        with st.form("create_meeting_form"):
            meeting_title = st.text_input("Tiêu đề Meeting *")
            
            col1, col2 = st.columns(2)
            with col1:
                meeting_date = st.date_input("Ngày Meeting *")
                meeting_time = st.time_input("Giờ Meeting *")
            
            with col2:
                duration = st.number_input("Thời lượng (phút) *", min_value=15, value=60, step=15)
                location = st.text_input("Địa điểm *")
            
            # Get team members for attendees
            team_members = self.db.get_team_members(project_id)
            attendee_options = team_members['name'].tolist() if not team_members.empty else []
            
            attendees = st.multiselect("Người tham dự *", options=attendee_options)
            
            agenda = st.text_area("Chương trình Meeting *", height=150)
            
            submitted = st.form_submit_button("📅 Tạo Meeting", type="primary")
            
            if submitted:
                if not all([meeting_title, meeting_date, meeting_time, location, attendees, agenda]):
                    st.error("Vui lòng điền đầy đủ thông tin!")
                else:
                    # Combine date and time
                    meeting_datetime = datetime.combine(meeting_date, meeting_time)
                    
                    meeting_id = self.create_meeting(
                        project_id=project_id,
                        meeting_title=meeting_title,
                        meeting_date=meeting_datetime,
                        duration=duration,
                        location=location,
                        attendees=attendees,
                        agenda=agenda,
                        created_by=current_user
                    )
                    
                    st.success(f"✅ Đã tạo meeting thành công! (ID: {meeting_id})")
                    st.balloons()
                    st.rerun()
    
    def _render_action_items(self, project_id, current_user):
        """Render action items tab"""
        st.subheader("Action Items")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.selectbox(
                "Lọc theo trạng thái",
                options=['Tất cả', 'Open', 'In Progress', 'Completed', 'Cancelled']
            )
        
        with col2:
            meeting_filter = st.selectbox(
                "Lọc theo Meeting",
                options=['Tất cả'] + self.get_meetings(project_id)['meeting_title'].tolist()
            )
        
        # Get action items
        action_items = self.get_action_items(project_id=project_id)
        
        # Apply filters
        if status_filter != 'Tất cả':
            action_items = action_items[action_items['status'] == status_filter]
        
        if meeting_filter != 'Tất cả':
            meetings = self.get_meetings(project_id)
            meeting_id = meetings[meetings['meeting_title'] == meeting_filter].iloc[0]['id']
            action_items = action_items[action_items['meeting_id'] == meeting_id]
        
        # Show overdue items
        overdue_items = self.get_overdue_action_items(project_id)
        if not overdue_items.empty:
            st.error(f"⚠️ Có {len(overdue_items)} action items quá hạn!")
            with st.expander("Xem action items quá hạn"):
                self._render_action_items_table(overdue_items)
        
        st.markdown("---")
        
        # Show all action items
        if action_items.empty:
            st.info("Không có action item nào")
        else:
            self._render_action_items_table(action_items)
    
    def _render_action_items_table(self, action_items, show_meeting=True):
        """Render action items table"""
        for _, item in action_items.iterrows():
            # Priority color
            priority_colors = {
                'High': '#dc3545',
                'Medium': '#ffc107',
                'Low': '#28a745'
            }
            color = priority_colors.get(item['priority'], '#6c757d')
            
            # Status icon
            status_icons = {
                'Open': '⭕',
                'In Progress': '🔄',
                'Completed': '✅',
                'Cancelled': '❌'
            }
            icon = status_icons.get(item['status'], '❓')
            
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style="border-left: 4px solid {color}; padding-left: 10px;">
                        <strong>{icon} {item['item_description']}</strong><br>
                        <small>Assigned to: {item['assigned_to']}</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    due_date = pd.to_datetime(item['due_date']).date()
                    today = datetime.now().date()
                    days_diff = (due_date - today).days
                    
                    if days_diff < 0 and item['status'] != 'Completed':
                        st.error(f"Quá hạn {abs(days_diff)} ngày")
                    elif days_diff == 0:
                        st.warning("Đến hạn hôm nay!")
                    else:
                        st.write(f"Đến hạn: {due_date.strftime('%d/%m/%Y')}")
                
                with col3:
                    st.write(f"**{item['priority']}** priority")
                    st.write(f"Status: {item['status']}")
                
                with col4:
                    if st.button("✏️", key=f"edit_action_{item['id']}"):
                        st.session_state[f'editing_action_{item["id"]}'] = True
                
                # Edit form
                if st.session_state.get(f'editing_action_{item["id"]}', False):
                    with st.expander("Cập nhật Action Item", expanded=True):
                        new_status = st.selectbox(
                            "Trạng thái",
                            options=['Open', 'In Progress', 'Completed', 'Cancelled'],
                            index=['Open', 'In Progress', 'Completed', 'Cancelled'].index(item['status']),
                            key=f"status_{item['id']}"
                        )
                        
                        notes = st.text_area(
                            "Ghi chú",
                            value=item['notes'] if pd.notna(item['notes']) else '',
                            key=f"notes_{item['id']}"
                        )
                        
                        col_save, col_cancel, col_delete = st.columns(3)
                        
                        with col_save:
                            if st.button("💾 Lưu", key=f"save_action_{item['id']}"):
                                self.update_action_item_status(
                                    item['id'],
                                    new_status,
                                    notes,
                                    'User'
                                )
                                del st.session_state[f'editing_action_{item["id"]}']
                                st.success("✅ Đã cập nhật!")
                                st.rerun()
                        
                        with col_cancel:
                            if st.button("❌ Hủy", key=f"cancel_action_{item['id']}"):
                                del st.session_state[f'editing_action_{item["id"]}']
                                st.rerun()
                        
                        with col_delete:
                            if st.button("🗑️ Xóa", key=f"delete_action_{item['id']}"):
                                self.delete_action_item(item['id'], 'User')
                                del st.session_state[f'editing_action_{item["id"]}']
                                st.success("✅ Đã xóa!")
                                st.rerun()
                
                st.markdown("---")
    
    def _render_add_action_item_form(self, meeting_id, project_id, current_user):
        """Render add action item form"""
        with st.form(f"add_action_form_{meeting_id}"):
            description = st.text_area("Mô tả Action Item *")
            
            col1, col2 = st.columns(2)
            with col1:
                # Get team members
                team_members = self.db.get_team_members(project_id)
                member_options = team_members['name'].tolist() if not team_members.empty else []
                
                assigned_to = st.selectbox("Phân công cho *", options=member_options)
                due_date = st.date_input("Deadline *")
            
            with col2:
                priority = st.selectbox("Mức độ ưu tiên", options=['High', 'Medium', 'Low'], index=1)
            
            notes = st.text_area("Ghi chú")
            
            submitted = st.form_submit_button("➕ Thêm Action Item", type="primary")
            
            if submitted:
                if not all([description, assigned_to, due_date]):
                    st.error("Vui lòng điền đầy đủ thông tin!")
                else:
                    action_id = self.create_action_item(
                        meeting_id=meeting_id,
                        project_id=project_id,
                        item_description=description,
                        assigned_to=assigned_to,
                        due_date=due_date,
                        priority=priority,
                        notes=notes
                    )
                    
                    del st.session_state[f'adding_action_{meeting_id}']
                    st.success(f"✅ Đã thêm action item! (ID: {action_id})")
                    st.rerun()
    
    # ===== STATISTICS =====
    
    def get_meeting_stats(self, project_id):
        """
        Get meeting statistics for a project
        
        Returns:
            dict: Statistics
        """
        meetings = self.get_meetings(project_id)
        action_items = self.get_action_items(project_id=project_id)
        
        # Total meetings
        total_meetings = len(meetings)
        
        # Meetings with minutes
        meetings_with_minutes = 0
        if not meetings.empty:
            meetings_with_minutes = len(meetings[meetings['minutes'].notna() & (meetings['minutes'] != '')])
        
        # Action items stats
        total_actions = len(action_items)
        completed_actions = len(action_items[action_items['status'] == 'Completed']) if not action_items.empty else 0
        overdue_actions = len(self.get_overdue_action_items(project_id))
        
        # Completion rate
        completion_rate = (completed_actions / total_actions * 100) if total_actions > 0 else 0
        
        return {
            'total_meetings': total_meetings,
            'meetings_with_minutes': meetings_with_minutes,
            'total_action_items': total_actions,
            'completed_actions': completed_actions,
            'overdue_actions': overdue_actions,
            'completion_rate': completion_rate
        }

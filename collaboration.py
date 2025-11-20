"""
Module Collaboration & Discussion
Quản lý comments, mentions, và activity log
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import re

class CollaborationManager:
    """
    Quản lý collaboration features: comments, mentions, activity log
    """
    
    def __init__(self, db, notification_system=None):
        """
        Initialize collaboration manager
        
        Args:
            db: ProjectDatabase instance
            notification_system: NotificationSystem instance (optional)
        """
        self.db = db
        self.notification_system = notification_system
    
    # ===== COMMENTS & DISCUSSION =====
    
    def add_comment(self, project_id, user_name, user_email, comment_text, parent_comment_id=None):
        """
        Add a new comment to a project
        
        Args:
            project_id: Project ID
            user_name: Name of the commenter
            user_email: Email of the commenter
            comment_text: Comment text
            parent_comment_id: ID of parent comment (for replies)
        
        Returns:
            int: Comment ID
        """
        # Extract mentions from comment
        mentions = self._extract_mentions(comment_text)
        
        comment_data = {
            'project_id': project_id,
            'user_name': user_name,
            'user_email': user_email,
            'comment_text': comment_text,
            'parent_comment_id': parent_comment_id,
            'mentions': ','.join(mentions) if mentions else None
        }
        
        comment_id = self.db.add_comment(comment_data)
        
        # Log activity
        self.log_activity(
            project_id=project_id,
            user_name=user_name,
            user_email=user_email,
            activity_type='comment_added',
            activity_description=f"Đã thêm bình luận: {comment_text[:50]}...",
            entity_type='comment',
            entity_id=comment_id
        )
        
        # Send notifications for mentions
        if mentions and self.notification_system:
            self._notify_mentions(project_id, mentions, comment_text, user_name)
        
        return comment_id
    
    def _extract_mentions(self, text):
        """
        Extract @mentions from text
        
        Args:
            text: Text to extract mentions from
        
        Returns:
            list: List of mentioned usernames/emails
        """
        # Pattern: @username or @email
        pattern = r'@(\w+(?:\.\w+)*(?:@[\w.-]+)?)'
        matches = re.findall(pattern, text)
        return matches
    
    def _notify_mentions(self, project_id, mentions, comment_text, commenter_name):
        """
        Send notifications to mentioned users
        """
        if not self.notification_system:
            return
        
        # Get all team members to find emails
        team_members = self.db.get_team_members(project_id)
        
        for mention in mentions:
            # Try to find the mentioned user in team members
            if '@' in mention:
                # It's an email
                mentioned_email = mention
            else:
                # It's a username, find email
                member = team_members[team_members['name'].str.lower() == mention.lower()]
                if not member.empty and pd.notna(member.iloc[0]['email']):
                    mentioned_email = member.iloc[0]['email']
                else:
                    continue
            
            # Send notification
            self.notification_system.notify_comment_mention(
                project_id,
                comment_text,
                mentioned_email,
                commenter_name
            )
    
    def get_comments(self, project_id, include_replies=True):
        """
        Get all comments for a project
        
        Args:
            project_id: Project ID
            include_replies: Include reply comments
        
        Returns:
            DataFrame: Comments data
        """
        comments = self.db.get_comments(project_id)
        
        if not include_replies:
            comments = comments[comments['parent_comment_id'].isna()]
        
        return comments
    
    def get_comment_thread(self, comment_id):
        """
        Get a comment and all its replies
        
        Args:
            comment_id: Comment ID
        
        Returns:
            DataFrame: Comment thread
        """
        return self.db.get_comment_thread(comment_id)
    
    def update_comment(self, comment_id, comment_text, user_name, user_email):
        """
        Update a comment
        """
        self.db.update_comment(comment_id, comment_text)
        
        # Log activity
        comment = self.db.get_comments(None)  # Get all to find this one
        comment = comment[comment['id'] == comment_id]
        
        if not comment.empty:
            self.log_activity(
                project_id=comment.iloc[0]['project_id'],
                user_name=user_name,
                user_email=user_email,
                activity_type='comment_updated',
                activity_description=f"Đã cập nhật bình luận",
                entity_type='comment',
                entity_id=comment_id
            )
    
    def delete_comment(self, comment_id, user_name, user_email):
        """
        Delete a comment
        """
        # Get comment info before deleting
        all_comments = self.db.get_comments(None)
        comment = all_comments[all_comments['id'] == comment_id]
        
        if not comment.empty:
            project_id = comment.iloc[0]['project_id']
            
            self.db.delete_comment(comment_id)
            
            # Log activity
            self.log_activity(
                project_id=project_id,
                user_name=user_name,
                user_email=user_email,
                activity_type='comment_deleted',
                activity_description=f"Đã xóa bình luận",
                entity_type='comment',
                entity_id=comment_id
            )
    
    def render_comment(self, comment, show_replies=True):
        """
        Render a single comment in Streamlit
        
        Args:
            comment: Comment data (Series or dict)
            show_replies: Show reply button
        """
        with st.container():
            col1, col2 = st.columns([1, 5])
            
            with col1:
                # User avatar (using first letter of name)
                st.markdown(f"""
                <div style="width: 50px; height: 50px; border-radius: 50%; background-color: #1f4788; 
                            color: white; display: flex; align-items: center; justify-content: center; 
                            font-size: 20px; font-weight: bold;">
                    {comment['user_name'][0].upper()}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 10px;">
                    <div style="margin-bottom: 5px;">
                        <strong>{comment['user_name']}</strong>
                        <span style="color: #6c757d; font-size: 12px; margin-left: 10px;">
                            {self._format_datetime(comment['created_at'])}
                        </span>
                    </div>
                    <div style="color: #212529;">
                        {comment['comment_text']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if show_replies:
                    col_reply, col_edit, col_delete = st.columns([2, 2, 2])
                    with col_reply:
                        if st.button("💬 Reply", key=f"reply_{comment['id']}"):
                            st.session_state[f'replying_to_{comment["id"]}'] = True
                    
                    # TODO: Add edit and delete buttons with permissions check
    
    def _format_datetime(self, dt_string):
        """
        Format datetime string for display
        """
        try:
            dt = datetime.fromisoformat(dt_string)
            now = datetime.now()
            diff = now - dt
            
            if diff.days == 0:
                if diff.seconds < 3600:
                    minutes = diff.seconds // 60
                    return f"{minutes} phút trước"
                else:
                    hours = diff.seconds // 3600
                    return f"{hours} giờ trước"
            elif diff.days == 1:
                return "Hôm qua"
            elif diff.days < 7:
                return f"{diff.days} ngày trước"
            else:
                return dt.strftime("%d/%m/%Y %H:%M")
        except:
            return dt_string
    
    def render_comment_section(self, project_id, user_name, user_email):
        """
        Render complete comment section for a project
        
        Args:
            project_id: Project ID
            user_name: Current user name
            user_email: Current user email
        """
        st.subheader("💬 Thảo luận & Bình luận")
        
        # Add new comment
        with st.expander("✍️ Thêm bình luận mới", expanded=False):
            comment_text = st.text_area(
                "Nội dung bình luận",
                placeholder="Nhập bình luận của bạn... (Dùng @tên để mention team members)",
                height=100
            )
            
            st.info("💡 **Tip**: Sử dụng @tên để nhắc đến team members")
            
            if st.button("📤 Đăng bình luận", type="primary"):
                if comment_text.strip():
                    self.add_comment(
                        project_id=project_id,
                        user_name=user_name,
                        user_email=user_email,
                        comment_text=comment_text
                    )
                    st.success("✅ Đã đăng bình luận!")
                    st.rerun()
                else:
                    st.error("Vui lòng nhập nội dung bình luận")
        
        st.markdown("---")
        
        # Display comments
        comments = self.get_comments(project_id, include_replies=False)
        
        if comments.empty:
            st.info("Chưa có bình luận nào. Hãy là người đầu tiên bình luận!")
        else:
            st.write(f"**{len(comments)} bình luận**")
            
            for _, comment in comments.iterrows():
                self.render_comment(comment)
                
                # Show replies
                replies = self.get_comment_thread(comment['id'])
                replies = replies[replies['id'] != comment['id']]  # Exclude parent
                
                if not replies.empty:
                    with st.container():
                        st.markdown('<div style="margin-left: 60px;">', unsafe_allow_html=True)
                        for _, reply in replies.iterrows():
                            self.render_comment(reply, show_replies=False)
                        st.markdown('</div>', unsafe_allow_html=True)
                
                # Reply form
                if st.session_state.get(f'replying_to_{comment["id"]}', False):
                    with st.container():
                        st.markdown('<div style="margin-left: 60px;">', unsafe_allow_html=True)
                        reply_text = st.text_area(
                            f"Trả lời {comment['user_name']}",
                            key=f"reply_text_{comment['id']}"
                        )
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Gửi trả lời", key=f"send_reply_{comment['id']}"):
                                if reply_text.strip():
                                    self.add_comment(
                                        project_id=project_id,
                                        user_name=user_name,
                                        user_email=user_email,
                                        comment_text=reply_text,
                                        parent_comment_id=comment['id']
                                    )
                                    del st.session_state[f'replying_to_{comment["id"]}']
                                    st.success("✅ Đã gửi trả lời!")
                                    st.rerun()
                        with col2:
                            if st.button("Hủy", key=f"cancel_reply_{comment['id']}"):
                                del st.session_state[f'replying_to_{comment["id"]}']
                                st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== ACTIVITY LOG =====
    
    def log_activity(self, project_id, user_name, user_email, activity_type, 
                     activity_description, entity_type=None, entity_id=None):
        """
        Log an activity
        
        Args:
            project_id: Project ID
            user_name: User name
            user_email: User email
            activity_type: Type of activity (e.g., 'comment_added', 'task_completed')
            activity_description: Description of activity
            entity_type: Type of entity (e.g., 'comment', 'task')
            entity_id: ID of entity
        
        Returns:
            int: Activity ID
        """
        activity_data = {
            'project_id': project_id,
            'user_name': user_name,
            'user_email': user_email,
            'activity_type': activity_type,
            'activity_description': activity_description,
            'entity_type': entity_type,
            'entity_id': entity_id
        }
        
        return self.db.log_activity(activity_data)
    
    def get_activity_log(self, project_id=None, limit=50):
        """
        Get activity log
        
        Args:
            project_id: Project ID (None for all projects)
            limit: Number of activities to return
        
        Returns:
            DataFrame: Activity log
        """
        return self.db.get_activity_log(project_id, limit)
    
    def render_activity_timeline(self, project_id, limit=20):
        """
        Render activity timeline for a project
        
        Args:
            project_id: Project ID
            limit: Number of activities to display
        """
        st.subheader("📊 Lịch sử hoạt động")
        
        activities = self.get_activity_log(project_id, limit)
        
        if activities.empty:
            st.info("Chưa có hoạt động nào được ghi nhận")
            return
        
        # Group by date
        activities['date'] = pd.to_datetime(activities['created_at']).dt.date
        
        for date in activities['date'].unique():
            st.markdown(f"**📅 {date.strftime('%d/%m/%Y')}**")
            
            day_activities = activities[activities['date'] == date]
            
            for _, activity in day_activities.iterrows():
                # Activity icon based on type
                icon = self._get_activity_icon(activity['activity_type'])
                
                time_str = datetime.fromisoformat(activity['created_at']).strftime('%H:%M')
                
                st.markdown(f"""
                <div style="margin-left: 20px; padding: 10px; border-left: 3px solid #1f4788; margin-bottom: 10px;">
                    <div style="color: #6c757d; font-size: 12px;">{time_str}</div>
                    <div>{icon} <strong>{activity['user_name']}</strong> {activity['activity_description']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
    
    def _get_activity_icon(self, activity_type):
        """Get icon for activity type"""
        icons = {
            'comment_added': '💬',
            'comment_updated': '✏️',
            'comment_deleted': '🗑️',
            'task_created': '✅',
            'task_updated': '📝',
            'task_completed': '🎉',
            'project_created': '🚀',
            'project_updated': '📋',
            'member_added': '👤',
            'signoff_completed': '✍️',
            'milestone_achieved': '🎯'
        }
        return icons.get(activity_type, '📌')
    
    # ===== STATISTICS =====
    
    def get_collaboration_stats(self, project_id):
        """
        Get collaboration statistics for a project
        
        Returns:
            dict: Statistics
        """
        comments = self.get_comments(project_id)
        activities = self.get_activity_log(project_id, limit=1000)
        
        # Top commenters
        top_commenters = {}
        if not comments.empty:
            top_commenters = comments['user_name'].value_counts().head(5).to_dict()
        
        # Activity by type
        activity_by_type = {}
        if not activities.empty:
            activity_by_type = activities['activity_type'].value_counts().to_dict()
        
        # Recent activity count (last 7 days)
        recent_count = 0
        if not activities.empty:
            recent_date = datetime.now() - pd.Timedelta(days=7)
            activities['created_at_dt'] = pd.to_datetime(activities['created_at'])
            recent_count = len(activities[activities['created_at_dt'] > recent_date])
        
        return {
            'total_comments': len(comments),
            'total_activities': len(activities),
            'recent_activity_count': recent_count,
            'top_commenters': top_commenters,
            'activity_by_type': activity_by_type
        }

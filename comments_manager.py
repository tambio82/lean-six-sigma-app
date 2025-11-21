"""
Comments Manager Module
Handles comments, @mentions, and discussion threads
"""

from datetime import datetime
from typing import List, Dict, Optional
import re
import streamlit as st

class CommentsManager:
    """
    Manage comments and @mentions for projects
    """
    
    def __init__(self, database, notification_service=None, activity_tracker=None):
        """
        Initialize comments manager
        
        Args:
            database: ProjectDatabase instance
            notification_service: NotificationService instance (optional)
            activity_tracker: ActivityTracker instance (optional)
        """
        self.db = database
        self.notification_service = notification_service
        self.activity_tracker = activity_tracker
    
    def add_comment(self, project_id: int, user_name: str, 
                   comment_text: str, user_email: str = None) -> bool:
        """
        Add a new comment
        
        Args:
            project_id: Project ID
            user_name: Name of commenter
            comment_text: Comment content
            user_email: Email of commenter (optional)
        
        Returns:
            bool: Success status
        """
        try:
            # Parse @mentions
            mentions = self.extract_mentions(comment_text)
            
            # Save comment
            comment_data = {
                'project_id': project_id,
                'user_name': user_name,
                'user_email': user_email,
                'comment_text': comment_text,
                'mentions': ','.join(mentions) if mentions else None,
                'created_at': datetime.now().isoformat()
            }
            
            success = self.db.add_comment(comment_data)
            
            if success:
                # Log activity
                if self.activity_tracker:
                    self.activity_tracker.log_comment_posted(
                        project_id, user_name, comment_text
                    )
                
                # Send notifications for mentions
                if mentions and self.notification_service:
                    self.notify_mentioned_users(
                        project_id, user_name, comment_text, mentions
                    )
            
            return success
        
        except Exception as e:
            print(f"Error adding comment: {e}")
            return False
    
    def get_comments(self, project_id: int) -> List[Dict]:
        """
        Get all comments for a project
        
        Args:
            project_id: Project ID
        
        Returns:
            List of comment dicts
        """
        try:
            comments = self.db.get_comments(project_id)
            return comments if comments is not None else []
        except Exception as e:
            print(f"Error getting comments: {e}")
            return []
    
    def delete_comment(self, comment_id: int, user_name: str) -> bool:
        """
        Delete a comment (only by comment owner)
        
        Args:
            comment_id: Comment ID
            user_name: Name of user requesting deletion
        
        Returns:
            bool: Success status
        """
        try:
            # Get comment to verify ownership
            comment = self.db.get_comment_by_id(comment_id)
            
            if not comment:
                return False
            
            # Check if user owns the comment
            if comment.get('user_name') != user_name:
                print(f"User {user_name} cannot delete comment by {comment.get('user_name')}")
                return False
            
            return self.db.delete_comment(comment_id)
        
        except Exception as e:
            print(f"Error deleting comment: {e}")
            return False
    
    def extract_mentions(self, text: str) -> List[str]:
        """
        Extract @mentions from text
        
        Args:
            text: Comment text
        
        Returns:
            List of mentioned usernames (without @)
        """
        # Pattern: @username (letters, numbers, spaces, Vietnamese characters)
        pattern = r'@([a-zA-ZÀ-ỹ0-9\s]+?)(?=\s|$|[,.:;!?])'
        mentions = re.findall(pattern, text)
        
        # Clean up: trim spaces and make unique
        mentions = [m.strip() for m in mentions]
        mentions = list(set(mentions))  # Remove duplicates
        
        return mentions
    
    def highlight_mentions(self, text: str) -> str:
        """
        Highlight @mentions in text for display
        
        Args:
            text: Comment text
        
        Returns:
            HTML with highlighted mentions
        """
        # Replace @mentions with styled spans
        pattern = r'@([a-zA-ZÀ-ỹ0-9\s]+?)(?=\s|$|[,.:;!?])'
        
        def replace_mention(match):
            username = match.group(1).strip()
            return f'<span style="color: #7C4DFF; font-weight: bold;">@{username}</span>'
        
        highlighted = re.sub(pattern, replace_mention, text)
        return highlighted
    
    def notify_mentioned_users(self, project_id: int, mentioned_by: str,
                               comment_text: str, mentioned_users: List[str]):
        """
        Send email notifications to mentioned users
        
        Args:
            project_id: Project ID
            mentioned_by: Name of user who mentioned
            comment_text: The comment text
            mentioned_users: List of mentioned usernames
        """
        if not self.notification_service:
            return
        
        try:
            # Get project info
            project = self.db.get_project(project_id)
            if not project:
                return
            
            project_name = project.get('project_name', 'Unknown Project')
            project_url = f"https://your-app-url.com/project/{project_id}"  # Update with actual URL
            
            # Get team members to find emails
            team_members = self.db.get_team_members(project_id)
            
            # Create name -> email mapping
            email_map = {}
            for member in team_members:
                name = member.get('name', '')
                email = member.get('email', '')
                if name and email:
                    email_map[name.strip().lower()] = email
            
            # Send notification to each mentioned user
            for username in mentioned_users:
                user_email = email_map.get(username.strip().lower())
                
                if user_email:
                    # Import here to avoid circular import
                    from notification_service import send_notification
                    
                    send_notification(
                        'mention',
                        user_email,
                        {
                            'mentioned_by': mentioned_by,
                            'comment': comment_text,
                            'project_name': project_name,
                            'url': project_url
                        }
                    )
                    
                    # Log mention activity
                    if self.activity_tracker:
                        self.activity_tracker.log_mention(
                            project_id, mentioned_by, username
                        )
        
        except Exception as e:
            print(f"Error notifying mentioned users: {e}")
    
    def get_autocomplete_users(self, project_id: int) -> List[str]:
        """
        Get list of team member names for autocomplete
        
        Args:
            project_id: Project ID
        
        Returns:
            List of user names
        """
        try:
            team_members = self.db.get_team_members(project_id)
            names = [m.get('name', '') for m in team_members if m.get('name')]
            return sorted(names)
        except Exception as e:
            print(f"Error getting autocomplete users: {e}")
            return []


# ==================== UI COMPONENTS ====================

def render_comment_section(project_id: int, current_user: str, 
                          comments_manager: CommentsManager):
    """
    Render comment section UI
    
    Args:
        project_id: Project ID
        current_user: Current user name
        comments_manager: CommentsManager instance
    """
    st.subheader("💬 Bình luận & Thảo luận")
    
    # Get all comments
    comments = comments_manager.get_comments(project_id)
    comment_count = len(comments) if comments else 0
    
    st.caption(f"{comment_count} bình luận")
    
    # New comment form
    with st.form(f"new_comment_{project_id}", clear_on_submit=True):
        st.write("**Viết bình luận mới**")
        
        # Get team members for mention suggestions
        team_members = comments_manager.get_autocomplete_users(project_id)
        if team_members:
            st.caption(f"💡 Tip: Gõ @ để mention team members: {', '.join(team_members[:5])}")
        
        comment_text = st.text_area(
            "Bình luận",
            placeholder="Viết bình luận của bạn... (Gõ @tên để mention người khác)",
            height=100,
            label_visibility="collapsed"
        )
        
        submit = st.form_submit_button("📤 Đăng bình luận", type="primary")
        
        if submit:
            if not comment_text.strip():
                st.error("⚠️ Vui lòng nhập nội dung bình luận!")
            else:
                success = comments_manager.add_comment(
                    project_id, current_user, comment_text
                )
                
                if success:
                    st.success("✅ Đã đăng bình luận!")
                    st.rerun()
                else:
                    st.error("❌ Lỗi khi đăng bình luận")
    
    # Display existing comments
    st.markdown("---")
    
    if not comments:
        st.info("Chưa có bình luận nào. Hãy là người đầu tiên!")
    else:
        # Sort by newest first
        comments_sorted = sorted(
            comments, 
            key=lambda x: x.get('created_at', ''), 
            reverse=True
        )
        
        for comment in comments_sorted:
            render_single_comment(comment, current_user, comments_manager)


def render_single_comment(comment: Dict, current_user: str, 
                         comments_manager: CommentsManager):
    """
    Render a single comment
    
    Args:
        comment: Comment dict
        current_user: Current user name
        comments_manager: CommentsManager instance
    """
    comment_id = comment.get('id')
    author = comment.get('user_name', 'Unknown')
    text = comment.get('comment_text', '')
    timestamp = comment.get('created_at', '')
    
    # Parse timestamp
    try:
        dt = datetime.fromisoformat(timestamp)
        time_str = dt.strftime("%d/%m/%Y %H:%M")
    except:
        time_str = timestamp
    
    # Container for comment
    with st.container():
        col1, col2 = st.columns([6, 1])
        
        with col1:
            st.markdown(f"**👤 {author}** · {time_str}")
            
            # Highlight mentions
            highlighted_text = comments_manager.highlight_mentions(text)
            st.markdown(highlighted_text, unsafe_allow_html=True)
        
        with col2:
            # Delete button (only for comment owner)
            if author == current_user:
                if st.button("🗑️", key=f"del_comment_{comment_id}"):
                    if comments_manager.delete_comment(comment_id, current_user):
                        st.success("✅ Đã xóa!")
                        st.rerun()
        
        st.markdown("---")


# ==================== MENTION AUTOCOMPLETE ====================

def create_mention_suggestions(team_members: List[str]) -> str:
    """
    Create JavaScript for @mention autocomplete
    (For future enhancement with custom components)
    
    Args:
        team_members: List of team member names
    
    Returns:
        JavaScript code for autocomplete
    """
    # This is a placeholder for future enhancement
    # with Streamlit custom components
    suggestions_js = f"""
    const teamMembers = {team_members};
    // Autocomplete logic here
    """
    return suggestions_js

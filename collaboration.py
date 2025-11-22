"""
Collaboration Module - Main Integration
Combines all collaboration features into one cohesive interface
FIXED: Removed limit parameter from get_activities call
"""

import streamlit as st
from datetime import datetime
from typing import Optional

# Import collaboration modules
from notification_service import NotificationService, get_notification_service
from activity_tracker import ActivityTracker
from comments_manager import CommentsManager, render_comment_section
from meeting_manager import MeetingManager, render_meeting_minutes_section


class CollaborationHub:
    """
    Main collaboration hub that integrates all features
    """
    
    def __init__(self, database):
        """
        Initialize collaboration hub
        
        Args:
            database: ProjectDatabase instance
        """
        self.db = database
        
        # Initialize services
        self.notification_service = get_notification_service()
        self.activity_tracker = ActivityTracker(database)
        self.comments_manager = CommentsManager(
            database,
            self.notification_service,
            self.activity_tracker
        )
        self.meeting_manager = MeetingManager(
            database,
            self.activity_tracker
        )
    
    def render(self, project_id: int, project: dict, current_user: str):
        """
        Render complete collaboration interface
        
        Args:
            project_id: Project ID
            project: Project dict
            current_user: Current user name
        """
        st.subheader("💬 Cộng tác & Giao tiếp")
        
        # Create tabs for different collaboration features
        tabs = st.tabs([
            "💭 Bình luận",
            "📋 Nhật ký Hoạt động",
            "🗓️ Biên bản Họp",
            "📧 Thông báo"
        ])
        
        # Tab 1: Comments
        with tabs[0]:
            self.render_comments_tab(project_id, current_user)
        
        # Tab 2: Activity Log
        with tabs[1]:
            self.render_activity_log_tab(project_id)
        
        # Tab 3: Meeting Minutes
        with tabs[2]:
            self.render_meetings_tab(project_id, current_user)
        
        # Tab 4: Notifications (placeholder)
        with tabs[3]:
            self.render_notifications_tab(project_id, current_user)
    
    def render_comments_tab(self, project_id: int, current_user: str):
        """Render comments tab"""
        render_comment_section(project_id, current_user, self.comments_manager)
    
    def render_activity_log_tab(self, project_id: int):
        """Render activity log tab"""
        st.write("### 📋 Nhật ký Hoạt động")
        
        # Get activities - FIXED: Removed limit parameter
        activities = self.db.get_activities(project_id)
        
        # Convert to list if DataFrame
        if hasattr(activities, 'to_dict'):
            activities = activities.to_dict('records')
        
        if not activities:
            st.info("Chưa có hoạt động nào được ghi nhận.")
            return
        
        # Limit to last 50 activities
        activities = activities[-50:] if len(activities) > 50 else activities
        
        # Filter options
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search = st.text_input("🔍 Tìm kiếm", placeholder="Tìm theo người dùng, hành động...")
        
        with col2:
            action_types = ["All"] + list(set([a.get('action_type', '') for a in activities]))
            filter_type = st.selectbox("Lọc theo loại", action_types)
        
        # Filter activities
        filtered = activities
        if search:
            filtered = [a for a in filtered 
                       if search.lower() in str(a).lower()]
        
        if filter_type != "All":
            filtered = [a for a in filtered 
                       if a.get('action_type') == filter_type]
        
        # Display count
        st.metric("Tổng số hoạt động", len(filtered))
        
        # Display activities in timeline
        st.markdown("---")
        
        for activity in filtered:
            formatted = self.activity_tracker.format_activity_for_display(activity)
            
            col1, col2 = st.columns([1, 5])
            
            with col1:
                st.write(formatted['icon'])
            
            with col2:
                st.write(f"**{formatted['user']}** {formatted['action']}")
                
                # Parse timestamp
                try:
                    dt = datetime.fromisoformat(formatted['timestamp'])
                    time_str = dt.strftime("%d/%m/%Y %H:%M")
                except:
                    time_str = formatted['timestamp']
                
                st.caption(time_str)
            
            st.markdown("---")
    
    def render_meetings_tab(self, project_id: int, current_user: str):
        """Render meeting minutes tab"""
        render_meeting_minutes_section(project_id, current_user, self.meeting_manager)
    
    def render_notifications_tab(self, project_id: int, current_user: str):
        """Render notifications tab (placeholder for future)"""
        st.write("### 📧 Thông báo")
        
        st.info("""
        **Thông báo Email**
        
        Hệ thống sẽ tự động gửi email khi:
        - ✅ Task sắp đến deadline (7, 3, 1 ngày trước)
        - 💬 Ai đó @mention bạn trong bình luận
        - ✍️ Có yêu cầu ký tên mới
        - 🎉 Đạt milestone quan trọng
        
        **Cấu hình:**
        - Email service: Đang sử dụng {provider}
        - Trạng thái: {status}
        
        Để thay đổi cài đặt email, vui lòng liên hệ admin.
        """.format(
            provider="SendGrid" if self.notification_service else "Not configured",
            status="✅ Hoạt động" if self.notification_service else "❌ Chưa cấu hình"
        ))
        
        # Test email button
        if st.button("🧪 Test Email Service"):
            test_result = self.test_email_service(current_user)
            if test_result:
                st.success("✅ Email service hoạt động tốt!")
            else:
                st.error("❌ Email service chưa được cấu hình đúng")
    
    def test_email_service(self, user_email: str) -> bool:
        """Test email service"""
        if not self.notification_service:
            return False
        
        try:
            from notification_service import EmailTemplates
            
            subject, html, text = EmailTemplates.task_deadline_reminder(
                task_name="Test Task",
                project_name="Test Project",
                deadline="2025-12-31",
                days_left=7,
                progress=50,
                owner="Test User",
                project_url="https://example.com"
            )
            
            return self.notification_service.send_email(
                user_email,
                subject,
                html,
                text
            )
        except Exception as e:
            print(f"Error testing email: {e}")
            return False


# ==================== HELPER FUNCTIONS ====================

def render_collaboration_tab(project_id: int, project: dict, 
                            database, current_user: str = "Current User"):
    """
    Main function to render collaboration tab in app
    
    Args:
        project_id: Project ID
        project: Project dict
        database: ProjectDatabase instance
        current_user: Current user name
    """
    # Initialize collaboration hub
    hub = CollaborationHub(database)
    
    # Render interface
    hub.render(project_id, project, current_user)


# ==================== AUTO-TRACKING INTEGRATION ====================

def integrate_activity_tracking(database):
    """
    Integrate activity tracking into existing database methods
    
    This wraps existing database methods to auto-log activities
    
    Args:
        database: ProjectDatabase instance
    
    Returns:
        ActivityTracker instance
    """
    tracker = ActivityTracker(database)
    
    # Store original methods
    original_add_project = database.add_project
    original_add_team_member = database.add_team_member
    original_add_task = database.add_task
    original_add_signoff = database.add_signoff
    
    # Wrap methods with tracking
    def add_project_with_tracking(project_data):
        result = original_add_project(project_data)
        if result:
            tracker.log_project_created(
                result,  # project_id
                project_data.get('created_by', 'System'),
                project_data.get('project_name', ''),
                project_data.get('methodology', 'DMAIC')
            )
        return result
    
    def add_team_member_with_tracking(member_data):
        result = original_add_team_member(member_data)
        if result:
            tracker.log_member_added(
                member_data.get('project_id'),
                member_data.get('added_by', 'System'),
                member_data.get('name', ''),
                member_data.get('role', '')
            )
        return result
    
    def add_task_with_tracking(task_data):
        result = original_add_task(task_data)
        if result:
            tracker.log_task_added(
                task_data.get('project_id'),
                task_data.get('created_by', 'System'),
                task_data.get('task_name', ''),
                task_data.get('phase', '')
            )
        return result
    
    def add_signoff_with_tracking(signoff_data):
        result = original_add_signoff(signoff_data)
        if result:
            tracker.log_signoff_completed(
                signoff_data.get('project_id'),
                signoff_data.get('name', ''),
                signoff_data.get('role', '')
            )
        return result
    
    # Replace methods
    database.add_project = add_project_with_tracking
    database.add_team_member = add_team_member_with_tracking
    database.add_task = add_task_with_tracking
    database.add_signoff = add_signoff_with_tracking
    
    return tracker


# ==================== NOTIFICATION SCHEDULER ====================

def setup_notification_scheduler(database):
    """
    Set up background scheduler for automated notifications
    
    Args:
        database: ProjectDatabase instance
    
    Returns:
        APScheduler instance
    """
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger
        
        scheduler = BackgroundScheduler()
        
        # Schedule daily deadline checks at 8 AM
        scheduler.add_job(
            func=check_deadlines_and_notify,
            trigger=CronTrigger(hour=8, minute=0),
            args=[database],
            id='deadline_check',
            name='Check task deadlines',
            replace_existing=True
        )
        
        # Start scheduler
        scheduler.start()
        
        return scheduler
    
    except ImportError:
        print("APScheduler not installed. Run: pip install apscheduler")
        return None
    except Exception as e:
        print(f"Error setting up scheduler: {e}")
        return None


def check_deadlines_and_notify(database):
    """
    Check all tasks for upcoming deadlines and send reminders
    
    Args:
        database: ProjectDatabase instance
    """
    try:
        from datetime import date, timedelta
        from notification_service import send_notification
        
        # Get all projects
        all_projects = database.get_all_projects()
        
        for project in all_projects:
            project_id = project.get('id')
            project_name = project.get('project_name', 'Unknown')
            
            # Get tasks for project
            tasks = database.get_tasks(project_id)
            
            if tasks.empty:
                continue
            
            # Check each task
            for _, task in tasks.iterrows():
                if task.get('status') == 'Hoàn thành':
                    continue  # Skip completed tasks
                
                deadline = task.get('end_date')
                if not deadline:
                    continue
                
                try:
                    deadline_date = datetime.fromisoformat(str(deadline)).date()
                except:
                    continue
                
                today = date.today()
                days_until_deadline = (deadline_date - today).days
                
                # Send reminder for 7, 3, or 1 day before
                if days_until_deadline in [7, 3, 1]:
                    # Get responsible person's email
                    responsible = task.get('responsible', '')
                    
                    # Try to find email from team members
                    team_members = database.get_team_members(project_id)
                    email = None
                    
                    for member in team_members:
                        if member.get('name', '').lower() == responsible.lower():
                            email = member.get('email')
                            break
                    
                    if email:
                        # Send notification
                        send_notification(
                            'task_deadline',
                            email,
                            {
                                'task_name': task.get('task_name', ''),
                                'project_name': project_name,
                                'deadline': deadline_date.strftime('%d/%m/%Y'),
                                'days_left': days_until_deadline,
                                'progress': task.get('progress', 0),
                                'owner': responsible,
                                'url': f"https://your-app-url.com/project/{project_id}"
                            }
                        )
    
    except Exception as e:
        print(f"Error checking deadlines: {e}")


# ==================== CONFIGURATION ====================

def get_collaboration_config():
    """
    Get collaboration configuration from Streamlit secrets
    
    Returns:
        Dict with configuration
    """
    try:
        import streamlit as st
        
        if hasattr(st, 'secrets') and 'collaboration' in st.secrets:
            return dict(st.secrets['collaboration'])
    except:
        pass
    
    # Default configuration
    return {
        'enable_email_notifications': True,
        'enable_activity_log': True,
        'enable_comments': True,
        'enable_meetings': True,
        'deadline_reminders': [7, 3, 1],  # days
        'max_comments_per_project': 1000,
        'max_meetings_per_project': 100
    }


# ==================== INITIALIZATION ====================

def initialize_collaboration(database, enable_scheduler=False):
    """
    Initialize all collaboration features
    
    Args:
        database: ProjectDatabase instance
        enable_scheduler: Enable background scheduler (default: False)
    
    Returns:
        Dict with initialized components
    """
    print("Initializing collaboration features...")
    
    # Get configuration
    config = get_collaboration_config()
    
    # Initialize components
    components = {
        'notification_service': get_notification_service(),
        'activity_tracker': ActivityTracker(database),
        'comments_manager': None,  # Created per-request
        'meeting_manager': None,   # Created per-request
        'scheduler': None,
        'config': config
    }
    
    # Integrate activity tracking
    if config.get('enable_activity_log', True):
        components['activity_tracker'] = integrate_activity_tracking(database)
        print("✓ Activity tracking integrated")
    
    # Set up scheduler
    if enable_scheduler and config.get('enable_email_notifications', True):
        components['scheduler'] = setup_notification_scheduler(database)
        if components['scheduler']:
            print("✓ Notification scheduler started")
    
    print("✓ Collaboration features initialized")
    
    return components

"""
Activity Tracker Module
Auto-logs all activities in the system for audit trail and timeline view
"""

from datetime import datetime
from typing import Optional, Dict, List
import json

class ActivityTracker:
    """
    Automatic activity logging system
    Tracks all user actions for audit trail and activity feed
    """
    
    def __init__(self, database):
        """Initialize activity tracker with database connection"""
        self.db = database
    
    def log_activity(self, project_id: int, user_name: str, 
                    action_type: str, action_details: str) -> bool:
        """
        Log an activity to the database
        
        Args:
            project_id: Project ID
            user_name: Name of user performing action
            action_type: Type of action
            action_details: Human-readable description
        
        Returns:
            bool: Success status
        """
        try:
            activity_data = {
                'project_id': project_id,
                'user_name': user_name,
                'action_type': action_type,
                'action_details': action_details,
                'created_at': datetime.now().isoformat()
            }
            
            return self.db.add_activity_log(activity_data)
        
        except Exception as e:
            print(f"Error logging activity: {e}")
            return False
    
    # Project activities
    def log_project_created(self, project_id, user_name, project_name, methodology):
        details = f"Tạo dự án '{project_name}' với phương pháp {methodology}"
        return self.log_activity(project_id, user_name, 'project_created', details)
    
    def log_project_updated(self, project_id, user_name, field, old_val, new_val):
        details = f"Cập nhật {field}: '{old_val}' → '{new_val}'"
        return self.log_activity(project_id, user_name, 'project_updated', details)
    
    def log_status_changed(self, project_id, user_name, old_status, new_status):
        details = f"Thay đổi trạng thái: {old_status} → {new_status}"
        return self.log_activity(project_id, user_name, 'status_changed', details)
    
    # Team activities
    def log_member_added(self, project_id, user_name, member_name, role):
        details = f"Thêm thành viên {member_name} với vai trò {role}"
        return self.log_activity(project_id, user_name, 'member_added', details)
    
    def log_member_removed(self, project_id, user_name, member_name):
        details = f"Xóa thành viên {member_name}"
        return self.log_activity(project_id, user_name, 'member_removed', details)
    
    # Task activities
    def log_task_added(self, project_id, user_name, task_name, phase):
        details = f"Thêm task '{task_name}' vào phase {phase}"
        return self.log_activity(project_id, user_name, 'task_added', details)
    
    def log_task_completed(self, project_id, user_name, task_name, phase):
        details = f"✅ Hoàn thành task '{task_name}' (Phase: {phase})"
        return self.log_activity(project_id, user_name, 'task_completed', details)
    
    # Sign-off activities
    def log_signoff_completed(self, project_id, signer_name, role):
        details = f"✍️ {signer_name} đã ký tên với vai trò {role}"
        return self.log_activity(project_id, signer_name, 'signoff_completed', details)
    
    # Milestone activities
    def log_phase_completed(self, project_id, user_name, phase_name, methodology):
        details = f"🎉 Hoàn thành phase {phase_name} ({methodology})"
        return self.log_activity(project_id, user_name, 'phase_completed', details)
    
    def log_milestone_achieved(self, project_id, user_name, milestone):
        details = f"🎯 Đạt milestone: {milestone}"
        return self.log_activity(project_id, user_name, 'milestone_achieved', details)
    
    # Comment activities
    def log_comment_posted(self, project_id, user_name, comment_preview):
        preview = comment_preview[:50] + "..." if len(comment_preview) > 50 else comment_preview
        details = f"💬 Đăng bình luận: {preview}"
        return self.log_activity(project_id, user_name, 'comment_posted', details)
    
    def log_mention(self, project_id, user_name, mentioned_user):
        details = f"@mention {mentioned_user} trong bình luận"
        return self.log_activity(project_id, user_name, 'user_mentioned', details)
    
    # Meeting activities
    def log_meeting_added(self, project_id, user_name, meeting_date):
        details = f"📅 Thêm biên bản họp ngày {meeting_date}"
        return self.log_activity(project_id, user_name, 'meeting_added', details)
    
    def log_decision_made(self, project_id, user_name, decision):
        preview = decision[:50] + "..." if len(decision) > 50 else decision
        details = f"✅ Quyết định: {preview}"
        return self.log_activity(project_id, user_name, 'decision_made', details)
    
    # DMAIC activities
    def log_sipoc_saved(self, project_id, user_name):
        details = "Lưu SIPOC diagram (Define phase)"
        return self.log_activity(project_id, user_name, 'dmaic_sipoc', details)
    
    def log_voc_added(self, project_id, user_name, count):
        details = f"Thêm {count} VOC entries (Define phase)"
        return self.log_activity(project_id, user_name, 'dmaic_voc', details)
    
    def log_baseline_saved(self, project_id, user_name, metric_count):
        details = f"Lưu {metric_count} baseline metrics (Measure phase)"
        return self.log_activity(project_id, user_name, 'dmaic_baseline', details)
    
    def log_fishbone_saved(self, project_id, user_name):
        details = "Lưu Fishbone diagram (Analyze phase)"
        return self.log_activity(project_id, user_name, 'dmaic_fishbone', details)
    
    def log_solution_added(self, project_id, user_name, solution):
        details = f"Thêm giải pháp: {solution[:40]}... (Improve phase)"
        return self.log_activity(project_id, user_name, 'dmaic_solution', details)
    
    def log_control_plan_saved(self, project_id, user_name):
        details = "Lưu Control Plan (Control phase)"
        return self.log_activity(project_id, user_name, 'dmaic_control', details)
    
    # Utility methods
    def get_activity_icon(self, action_type: str) -> str:
        """Get icon for activity type"""
        icons = {
            'project_created': '🆕', 'project_updated': '📝', 'status_changed': '🔄',
            'member_added': '👥', 'member_removed': '👤', 'task_added': '📋',
            'task_completed': '✅', 'signoff_completed': '✍️', 'phase_completed': '🎉',
            'milestone_achieved': '🎯', 'comment_posted': '💬', 'user_mentioned': '@',
            'meeting_added': '📅', 'decision_made': '✅', 'dmaic_sipoc': '📊',
            'dmaic_voc': '🗣️', 'dmaic_baseline': '📈', 'dmaic_fishbone': '🐟',
            'dmaic_solution': '💡', 'dmaic_control': '🎯'
        }
        return icons.get(action_type, '📋')
    
    def format_activity_for_display(self, activity: Dict) -> Dict:
        """Format activity for display in UI"""
        return {
            'id': activity.get('id'),
            'icon': self.get_activity_icon(activity.get('action_type', '')),
            'user': activity.get('user_name', 'Unknown'),
            'action': activity.get('action_details', ''),
            'timestamp': activity.get('created_at', ''),
            'type': activity.get('action_type', '')
        }

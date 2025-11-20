"""
Module Notification System
Gửi email notifications cho các sự kiện quan trọng trong dự án
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import pandas as pd

class NotificationSystem:
    """
    Hệ thống thông báo email cho Lean Six Sigma Projects
    """
    
    def __init__(self, db, smtp_config=None):
        """
        Initialize notification system
        
        Args:
            db: ProjectDatabase instance
            smtp_config: Dict with keys: server, port, username, password, from_email
        """
        self.db = db
        self.smtp_config = smtp_config or self._get_default_config()
    
    def _get_default_config(self):
        """
        Default SMTP configuration (sử dụng Gmail)
        Trong production, nên lưu trong environment variables hoặc config file
        """
        return {
            'server': 'smtp.gmail.com',
            'port': 587,
            'username': '',  # Set this in production
            'password': '',  # Set this in production
            'from_email': '',  # Set this in production
            'enabled': False  # Disabled by default until configured
        }
    
    def configure_smtp(self, server, port, username, password, from_email):
        """Configure SMTP settings"""
        self.smtp_config = {
            'server': server,
            'port': port,
            'username': username,
            'password': password,
            'from_email': from_email,
            'enabled': True
        }
    
    def send_email(self, to_email, subject, body_html, body_text=None):
        """
        Send email notification
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body_html: HTML body content
            body_text: Plain text fallback (optional)
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        if not self.smtp_config.get('enabled'):
            print(f"SMTP not configured. Would send email to {to_email}: {subject}")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.smtp_config['from_email']
            msg['To'] = to_email
            
            # Add text and HTML parts
            if body_text:
                part1 = MIMEText(body_text, 'plain')
                msg.attach(part1)
            
            part2 = MIMEText(body_html, 'html')
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port']) as server:
                server.starttls()
                server.login(self.smtp_config['username'], self.smtp_config['password'])
                server.send_message(msg)
            
            return True
        
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def _create_notification_record(self, project_id, recipient_email, notification_type, title, message):
        """Create notification record in database"""
        notification_data = {
            'project_id': project_id,
            'recipient_email': recipient_email,
            'notification_type': notification_type,
            'title': title,
            'message': message,
            'is_read': 0,
            'sent_at': datetime.now().isoformat()
        }
        return self.db.add_notification(notification_data)
    
    # ===== PROJECT ASSIGNMENT NOTIFICATIONS =====
    
    def notify_project_assignment(self, project_id, assigned_to_email, assigned_by_name):
        """
        Notify when a team member is assigned to a project
        """
        project = self.db.get_project(project_id)
        if project.empty:
            return False
        
        project_info = project.iloc[0]
        
        subject = f"🎯 Bạn được phân công vào dự án: {project_info['project_name']}"
        
        body_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #1f4788;">Thông báo phân công dự án</h2>
                <p>Xin chào,</p>
                <p>Bạn đã được <strong>{assigned_by_name}</strong> phân công vào dự án:</p>
                
                <div style="background-color: #f0f2f6; padding: 15px; border-left: 4px solid #1f4788; margin: 20px 0;">
                    <h3 style="margin-top: 0;">{project_info['project_name']}</h3>
                    <p><strong>Mã dự án:</strong> {project_info['project_code']}</p>
                    <p><strong>Phòng ban:</strong> {project_info['department']}</p>
                    <p><strong>Ngày bắt đầu:</strong> {project_info['start_date']}</p>
                    <p><strong>Ngày kết thúc:</strong> {project_info['end_date']}</p>
                    <p><strong>Mô tả:</strong> {project_info['description']}</p>
                </div>
                
                <p>Vui lòng đăng nhập vào hệ thống để xem chi tiết dự án.</p>
                
                <p>Trân trọng,<br>
                Hệ thống quản lý Lean Six Sigma</p>
            </body>
        </html>
        """
        
        # Send email
        email_sent = self.send_email(assigned_to_email, subject, body_html)
        
        # Create notification record
        self._create_notification_record(
            project_id,
            assigned_to_email,
            'project_assignment',
            subject,
            f"Bạn được phân công bởi {assigned_by_name}"
        )
        
        return email_sent
    
    # ===== DEADLINE NOTIFICATIONS =====
    
    def check_approaching_deadlines(self, days_ahead=7):
        """
        Check for tasks with approaching deadlines and send notifications
        
        Args:
            days_ahead: Number of days ahead to check (default 7)
        """
        today = datetime.now().date()
        deadline_date = today + timedelta(days=days_ahead)
        
        # Get all tasks
        all_tasks = self.db.get_all_tasks()
        
        notifications_sent = []
        
        for _, task in all_tasks.iterrows():
            if pd.notna(task['end_date']):
                try:
                    task_end = datetime.fromisoformat(task['end_date']).date()
                    
                    # Check if deadline is approaching
                    if today <= task_end <= deadline_date:
                        days_remaining = (task_end - today).days
                        
                        # Get project info
                        project = self.db.get_project(task['project_id'])
                        if not project.empty:
                            project_info = project.iloc[0]
                            
                            # Get responsible person's email
                            team_members = self.db.get_team_members(task['project_id'])
                            responsible_member = team_members[team_members['name'] == task['responsible']]
                            
                            if not responsible_member.empty and pd.notna(responsible_member.iloc[0]['email']):
                                recipient_email = responsible_member.iloc[0]['email']
                                
                                subject = f"⏰ Nhắc nhở: Task '{task['task_name']}' sắp đến hạn"
                                
                                urgency_color = "#dc3545" if days_remaining <= 3 else "#ffc107"
                                
                                body_html = f"""
                                <html>
                                    <body style="font-family: Arial, sans-serif;">
                                        <h2 style="color: {urgency_color};">⏰ Nhắc nhở deadline</h2>
                                        <p>Xin chào {task['responsible']},</p>
                                        <p>Task của bạn sắp đến hạn trong <strong>{days_remaining} ngày</strong>:</p>
                                        
                                        <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid {urgency_color}; margin: 20px 0;">
                                            <h3 style="margin-top: 0;">{task['task_name']}</h3>
                                            <p><strong>Dự án:</strong> {project_info['project_name']}</p>
                                            <p><strong>Phase:</strong> {task['phase']}</p>
                                            <p><strong>Deadline:</strong> {task['end_date']}</p>
                                            <p><strong>Trạng thái hiện tại:</strong> {task['status']}</p>
                                            <p><strong>Tiến độ:</strong> {task['progress']}%</p>
                                        </div>
                                        
                                        <p>Vui lòng cập nhật tiến độ hoặc hoàn thành task trước deadline.</p>
                                        
                                        <p>Trân trọng,<br>
                                        Hệ thống quản lý Lean Six Sigma</p>
                                    </body>
                                </html>
                                """
                                
                                # Send email
                                if self.send_email(recipient_email, subject, body_html):
                                    notifications_sent.append({
                                        'task': task['task_name'],
                                        'email': recipient_email,
                                        'days_remaining': days_remaining
                                    })
                                
                                # Create notification record
                                self._create_notification_record(
                                    task['project_id'],
                                    recipient_email,
                                    'deadline_reminder',
                                    subject,
                                    f"Task '{task['task_name']}' sắp đến hạn trong {days_remaining} ngày"
                                )
                
                except Exception as e:
                    print(f"Error processing task {task['task_name']}: {e}")
        
        return notifications_sent
    
    # ===== SIGN-OFF NOTIFICATIONS =====
    
    def notify_signoff_request(self, project_id, signoff_role, recipient_email, requested_by):
        """
        Notify when sign-off is requested
        """
        project = self.db.get_project(project_id)
        if project.empty:
            return False
        
        project_info = project.iloc[0]
        
        subject = f"✍️ Yêu cầu ký duyệt: {project_info['project_name']}"
        
        body_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #1f4788;">Yêu cầu ký duyệt dự án</h2>
                <p>Kính gửi {signoff_role},</p>
                <p><strong>{requested_by}</strong> yêu cầu bạn ký duyệt cho dự án:</p>
                
                <div style="background-color: #e7f3ff; padding: 15px; border-left: 4px solid #1f4788; margin: 20px 0;">
                    <h3 style="margin-top: 0;">{project_info['project_name']}</h3>
                    <p><strong>Mã dự án:</strong> {project_info['project_code']}</p>
                    <p><strong>Phòng ban:</strong> {project_info['department']}</p>
                    <p><strong>Trạng thái:</strong> {project_info['status']}</p>
                    <p><strong>Vai trò ký duyệt:</strong> {signoff_role}</p>
                </div>
                
                <p>Vui lòng đăng nhập vào hệ thống để xem xét và ký duyệt.</p>
                
                <p>Trân trọng,<br>
                Hệ thống quản lý Lean Six Sigma</p>
            </body>
        </html>
        """
        
        # Send email
        email_sent = self.send_email(recipient_email, subject, body_html)
        
        # Create notification record
        self._create_notification_record(
            project_id,
            recipient_email,
            'signoff_request',
            subject,
            f"Yêu cầu ký duyệt với vai trò {signoff_role}"
        )
        
        return email_sent
    
    def notify_signoff_completed(self, project_id, signoff_role, signed_by, notify_team=True):
        """
        Notify when sign-off is completed
        """
        project = self.db.get_project(project_id)
        if project.empty:
            return False
        
        project_info = project.iloc[0]
        
        subject = f"✅ Đã ký duyệt: {project_info['project_name']}"
        
        body_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #28a745;">✅ Thông báo ký duyệt</h2>
                <p>Xin chào,</p>
                <p><strong>{signed_by}</strong> đã ký duyệt dự án với vai trò <strong>{signoff_role}</strong>:</p>
                
                <div style="background-color: #d4edda; padding: 15px; border-left: 4px solid #28a745; margin: 20px 0;">
                    <h3 style="margin-top: 0;">{project_info['project_name']}</h3>
                    <p><strong>Mã dự án:</strong> {project_info['project_code']}</p>
                    <p><strong>Vai trò ký duyệt:</strong> {signoff_role}</p>
                    <p><strong>Người ký:</strong> {signed_by}</p>
                    <p><strong>Thời gian:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                </div>
                
                <p>Trân trọng,<br>
                Hệ thống quản lý Lean Six Sigma</p>
            </body>
        </html>
        """
        
        if notify_team:
            # Notify all team members
            team_members = self.db.get_team_members(project_id)
            for _, member in team_members.iterrows():
                if pd.notna(member['email']):
                    self.send_email(member['email'], subject, body_html)
                    
                    self._create_notification_record(
                        project_id,
                        member['email'],
                        'signoff_completed',
                        subject,
                        f"{signed_by} đã ký duyệt với vai trò {signoff_role}"
                    )
        
        return True
    
    # ===== MILESTONE NOTIFICATIONS =====
    
    def notify_milestone_achieved(self, project_id, milestone_name, achieved_by):
        """
        Notify when a milestone is achieved
        """
        project = self.db.get_project(project_id)
        if project.empty:
            return False
        
        project_info = project.iloc[0]
        
        subject = f"🎉 Milestone đạt được: {milestone_name}"
        
        body_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #28a745;">🎉 Chúc mừng!</h2>
                <p>Xin chào,</p>
                <p>Dự án <strong>{project_info['project_name']}</strong> đã đạt được milestone quan trọng:</p>
                
                <div style="background-color: #d4edda; padding: 15px; border-left: 4px solid #28a745; margin: 20px 0;">
                    <h3 style="margin-top: 0;">🎯 {milestone_name}</h3>
                    <p><strong>Dự án:</strong> {project_info['project_name']}</p>
                    <p><strong>Mã dự án:</strong> {project_info['project_code']}</p>
                    <p><strong>Người hoàn thành:</strong> {achieved_by}</p>
                    <p><strong>Thời gian:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                </div>
                
                <p>Chúc mừng toàn bộ team đã làm việc tuyệt vời!</p>
                
                <p>Trân trọng,<br>
                Hệ thống quản lý Lean Six Sigma</p>
            </body>
        </html>
        """
        
        # Notify all team members
        team_members = self.db.get_team_members(project_id)
        for _, member in team_members.iterrows():
            if pd.notna(member['email']):
                self.send_email(member['email'], subject, body_html)
                
                self._create_notification_record(
                    project_id,
                    member['email'],
                    'milestone_achieved',
                    subject,
                    f"Milestone '{milestone_name}' đã đạt được"
                )
        
        return True
    
    # ===== COMMENT NOTIFICATIONS =====
    
    def notify_comment_mention(self, project_id, comment_text, mentioned_user_email, commenter_name):
        """
        Notify when user is mentioned in a comment
        """
        project = self.db.get_project(project_id)
        if project.empty:
            return False
        
        project_info = project.iloc[0]
        
        subject = f"💬 Bạn được nhắc đến trong: {project_info['project_name']}"
        
        # Truncate comment if too long
        preview = comment_text[:200] + "..." if len(comment_text) > 200 else comment_text
        
        body_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #1f4788;">💬 Bạn được nhắc đến</h2>
                <p>Xin chào,</p>
                <p><strong>{commenter_name}</strong> đã nhắc đến bạn trong một bình luận:</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #1f4788; margin: 20px 0;">
                    <p><strong>Dự án:</strong> {project_info['project_name']}</p>
                    <p style="font-style: italic; margin-top: 10px;">"{preview}"</p>
                </div>
                
                <p>Vui lòng đăng nhập vào hệ thống để xem và trả lời bình luận.</p>
                
                <p>Trân trọng,<br>
                Hệ thống quản lý Lean Six Sigma</p>
            </body>
        </html>
        """
        
        # Send email
        email_sent = self.send_email(mentioned_user_email, subject, body_html)
        
        # Create notification record
        self._create_notification_record(
            project_id,
            mentioned_user_email,
            'comment_mention',
            subject,
            f"{commenter_name} đã nhắc đến bạn trong một bình luận"
        )
        
        return email_sent
    
    # ===== UTILITY METHODS =====
    
    def get_unread_notifications(self, user_email):
        """Get all unread notifications for a user"""
        return self.db.get_notifications(recipient_email=user_email, unread_only=True)
    
    def mark_as_read(self, notification_id):
        """Mark a notification as read"""
        self.db.mark_notification_read(notification_id)
    
    def get_notification_summary(self, user_email):
        """Get notification summary for a user"""
        notifications = self.db.get_notifications(recipient_email=user_email)
        
        if notifications.empty:
            return {
                'total': 0,
                'unread': 0,
                'by_type': {}
            }
        
        unread = notifications[notifications['is_read'] == 0]
        by_type = notifications['notification_type'].value_counts().to_dict()
        
        return {
            'total': len(notifications),
            'unread': len(unread),
            'by_type': by_type
        }

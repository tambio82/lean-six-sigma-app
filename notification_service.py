"""
Notification Service Module
Handles email notifications for Lean Six Sigma App
Supports: SendGrid, Gmail SMTP, AWS SES
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

class NotificationService:
    """
    Email notification service supporting multiple providers
    Default: SendGrid API (recommended)
    Fallback: Gmail SMTP
    """
    
    def __init__(self, provider='sendgrid', config=None):
        """
        Initialize notification service
        
        Args:
            provider: 'sendgrid', 'gmail', 'ses'
            config: Dict with email credentials
        """
        self.provider = provider
        self.config = config or {}
        self.from_email = self.config.get('from_email', 'noreply@hospital.com')
        self.from_name = self.config.get('from_name', 'Lean Six Sigma App')
        
    def send_email(self, to_email: str, subject: str, body_html: str, 
                   body_text: str = None) -> bool:
        """
        Send email using configured provider
        
        Args:
            to_email: Recipient email
            subject: Email subject
            body_html: HTML body
            body_text: Plain text body (fallback)
        
        Returns:
            bool: Success status
        """
        try:
            if self.provider == 'sendgrid':
                return self._send_via_sendgrid(to_email, subject, body_html, body_text)
            elif self.provider == 'gmail':
                return self._send_via_gmail(to_email, subject, body_html, body_text)
            elif self.provider == 'ses':
                return self._send_via_ses(to_email, subject, body_html, body_text)
            else:
                print(f"Unknown provider: {self.provider}")
                return False
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def _send_via_sendgrid(self, to_email, subject, body_html, body_text):
        """Send email via SendGrid API"""
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail, Email, To, Content
            
            api_key = self.config.get('api_key')
            if not api_key:
                print("SendGrid API key not found")
                return False
            
            message = Mail(
                from_email=Email(self.from_email, self.from_name),
                to_emails=To(to_email),
                subject=subject,
                html_content=Content("text/html", body_html)
            )
            
            if body_text:
                message.add_content(Content("text/plain", body_text))
            
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)
            
            return response.status_code in [200, 201, 202]
        
        except ImportError:
            print("SendGrid library not installed. Run: pip install sendgrid")
            return False
        except Exception as e:
            print(f"SendGrid error: {e}")
            return False
    
    def _send_via_gmail(self, to_email, subject, body_html, body_text):
        """Send email via Gmail SMTP"""
        try:
            smtp_server = self.config.get('smtp_server', 'smtp.gmail.com')
            smtp_port = self.config.get('smtp_port', 587)
            username = self.config.get('username')
            password = self.config.get('password')
            
            if not username or not password:
                print("Gmail credentials not found")
                return False
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = formataddr((self.from_name, self.from_email))
            msg['To'] = to_email
            
            # Add text and HTML parts
            if body_text:
                part1 = MIMEText(body_text, 'plain', 'utf-8')
                msg.attach(part1)
            
            part2 = MIMEText(body_html, 'html', 'utf-8')
            msg.attach(part2)
            
            # Send
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
            
            return True
        
        except Exception as e:
            print(f"Gmail SMTP error: {e}")
            return False
    
    def _send_via_ses(self, to_email, subject, body_html, body_text):
        """Send email via AWS SES"""
        try:
            import boto3
            from botocore.exceptions import ClientError
            
            aws_region = self.config.get('aws_region', 'us-east-1')
            
            client = boto3.client('ses', region_name=aws_region)
            
            response = client.send_email(
                Source=f"{self.from_name} <{self.from_email}>",
                Destination={'ToAddresses': [to_email]},
                Message={
                    'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                    'Body': {
                        'Html': {'Data': body_html, 'Charset': 'UTF-8'},
                        'Text': {'Data': body_text or '', 'Charset': 'UTF-8'}
                    }
                }
            )
            
            return response['ResponseMetadata']['HTTPStatusCode'] == 200
        
        except ImportError:
            print("boto3 not installed. Run: pip install boto3")
            return False
        except Exception as e:
            print(f"AWS SES error: {e}")
            return False


class EmailTemplates:
    """Email templates for different notification types"""
    
    @staticmethod
    def task_deadline_reminder(task_name, project_name, deadline, days_left, 
                               progress, owner, project_url):
        """Template for task deadline reminder"""
        subject = f"⏰ Task deadline in {days_left} days - {project_name}"
        
        urgency_emoji = "🔴" if days_left <= 1 else "🟡" if days_left <= 3 else "🟢"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: #4A90E2; color: white; padding: 20px; border-radius: 5px;">
                    <h2>⏰ Task Deadline Reminder</h2>
                </div>
                <div style="background: #f9f9f9; padding: 20px; margin: 20px 0;">
                    <p>Xin chào <strong>{owner}</strong>,</p>
                    <p>Task "<strong>{task_name}</strong>" trong dự án "<strong>{project_name}</strong>" sắp đến deadline:</p>
                    <div style="background: white; padding: 15px; margin: 10px 0; border-left: 4px solid #4A90E2;">
                        <p style="font-size: 24px;">{urgency_emoji} <strong>Còn {days_left} ngày</strong></p>
                        <p>📅 Deadline: {deadline}</p>
                        <p>📊 Tiến độ: {progress}%</p>
                    </div>
                    <p><a href="{project_url}" style="display: inline-block; padding: 10px 20px; background: #4A90E2; color: white; text-decoration: none; border-radius: 5px;">👉 Xem chi tiết</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_body = f"Task {task_name} - Deadline in {days_left} days ({deadline}). Progress: {progress}%. View: {project_url}"
        
        return (subject, html_body, text_body)
    
    @staticmethod
    def mention_notification(mentioned_by, comment, project_name, project_url):
        """Template for @mention"""
        subject = f"💬 {mentioned_by} mentioned you"
        
        html_body = f"""
        <div style="max-width: 600px; margin: 0 auto; font-family: Arial;">
            <div style="background: #7C4DFF; color: white; padding: 20px;">
                <h2>💬 You Were Mentioned!</h2>
            </div>
            <div style="padding: 20px;">
                <p><strong>{mentioned_by}</strong> mentioned you in "{project_name}":</p>
                <div style="background: #f0f0f0; padding: 15px; margin: 10px 0; font-style: italic;">
                    "{comment}"
                </div>
                <p><a href="{project_url}" style="display: inline-block; padding: 10px 20px; background: #7C4DFF; color: white; text-decoration: none;">Reply</a></p>
            </div>
        </div>
        """
        
        text_body = f"{mentioned_by} mentioned you: {comment}. Reply: {project_url}"
        return (subject, html_body, text_body)


def get_notification_service(config=None):
    """Factory function to get notification service"""
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and 'email' in st.secrets:
            email_config = dict(st.secrets['email'])
            provider = email_config.get('provider', 'sendgrid')
            return NotificationService(provider=provider, config=email_config)
    except:
        pass
    return NotificationService(config=config or {})


def send_notification(notification_type, recipient_email, data):
    """High-level function to send notifications"""
    service = get_notification_service()
    
    if notification_type == 'task_deadline':
        subject, html, text = EmailTemplates.task_deadline_reminder(
            data['task_name'], data['project_name'], data['deadline'],
            data['days_left'], data['progress'], data['owner'], data['url']
        )
    elif notification_type == 'mention':
        subject, html, text = EmailTemplates.mention_notification(
            data['mentioned_by'], data['comment'], 
            data['project_name'], data['url']
        )
    else:
        return False
    
    return service.send_email(recipient_email, subject, html, text)

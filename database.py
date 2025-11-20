import sqlite3
import pandas as pd
from datetime import datetime
import json

class ProjectDatabase:
    def __init__(self, db_path="lean_projects.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Bảng thông tin dự án
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_code TEXT UNIQUE NOT NULL,
                project_name TEXT NOT NULL,
                department TEXT,
                start_date TEXT,
                end_date TEXT,
                status TEXT,
                category TEXT,
                description TEXT,
                problem_statement TEXT,
                goal TEXT,
                scope TEXT,
                budget REAL,
                actual_cost REAL,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # Bảng thành viên dự án
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                name TEXT NOT NULL,
                role TEXT,
                department TEXT,
                email TEXT,
                phone TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
            )
        ''')
        
        # Bảng stakeholders
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stakeholders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                name TEXT NOT NULL,
                role TEXT,
                department TEXT,
                impact_level TEXT,
                engagement_level TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
            )
        ''')
        
        # Bảng kế hoạch (Gantt)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS project_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                phase TEXT,
                task_name TEXT NOT NULL,
                start_date TEXT,
                end_date TEXT,
                responsible TEXT,
                status TEXT,
                progress INTEGER,
                FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
            )
        ''')
        
        # Bảng ký tên
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signoffs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                role TEXT NOT NULL,
                name TEXT,
                signature TEXT,
                date TEXT,
                notes TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
            )
        ''')
        
        # Bảng comments và discussion
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                user_name TEXT NOT NULL,
                user_email TEXT,
                comment_text TEXT NOT NULL,
                parent_comment_id INTEGER,
                mentions TEXT,
                created_at TEXT,
                updated_at TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
                FOREIGN KEY (parent_comment_id) REFERENCES comments (id) ON DELETE CASCADE
            )
        ''')
        
        # Bảng notifications
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                recipient_email TEXT NOT NULL,
                notification_type TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                is_read INTEGER DEFAULT 0,
                sent_at TEXT,
                created_at TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
            )
        ''')
        
        # Bảng activity log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                user_name TEXT NOT NULL,
                user_email TEXT,
                activity_type TEXT NOT NULL,
                activity_description TEXT NOT NULL,
                entity_type TEXT,
                entity_id INTEGER,
                created_at TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
            )
        ''')
        
        # Bảng meetings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meetings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                meeting_title TEXT NOT NULL,
                meeting_date TEXT,
                duration INTEGER,
                location TEXT,
                attendees TEXT,
                agenda TEXT,
                minutes TEXT,
                decisions TEXT,
                created_by TEXT,
                created_at TEXT,
                updated_at TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
            )
        ''')
        
        # Bảng action items từ meetings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS action_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meeting_id INTEGER,
                project_id INTEGER,
                item_description TEXT NOT NULL,
                assigned_to TEXT,
                due_date TEXT,
                status TEXT DEFAULT 'Open',
                priority TEXT,
                notes TEXT,
                created_at TEXT,
                completed_at TEXT,
                FOREIGN KEY (meeting_id) REFERENCES meetings (id) ON DELETE CASCADE,
                FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
            )
        ''')
        
        # Bảng danh mục phòng ban
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # ===== QUẢN LÝ DỰ ÁN =====
    def add_project(self, project_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        project_data['created_at'] = now
        project_data['updated_at'] = now
        
        columns = ', '.join(project_data.keys())
        placeholders = ', '.join(['?' for _ in project_data])
        
        cursor.execute(f'''
            INSERT INTO projects ({columns})
            VALUES ({placeholders})
        ''', list(project_data.values()))
        
        project_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return project_id
    
    def update_project(self, project_id, project_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        project_data['updated_at'] = datetime.now().isoformat()
        
        set_clause = ', '.join([f"{key} = ?" for key in project_data.keys()])
        values = list(project_data.values()) + [project_id]
        
        cursor.execute(f'''
            UPDATE projects
            SET {set_clause}
            WHERE id = ?
        ''', values)
        
        conn.commit()
        conn.close()
    
    def get_project(self, project_id):
        conn = self.get_connection()
        df = pd.read_sql_query(
            "SELECT * FROM projects WHERE id = ?",
            conn,
            params=(project_id,)
        )
        conn.close()
        
        if len(df) > 0:
            return df.iloc[0].to_dict()
        return None
    
    def get_all_projects(self):
        conn = self.get_connection()
        df = pd.read_sql_query("SELECT * FROM projects ORDER BY created_at DESC", conn)
        conn.close()
        return df
    
    def delete_project(self, project_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        conn.close()
    
    # ===== QUẢN LÝ THÀNH VIÊN =====
    def add_team_member(self, member_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        columns = ', '.join(member_data.keys())
        placeholders = ', '.join(['?' for _ in member_data])
        
        cursor.execute(f'''
            INSERT INTO team_members ({columns})
            VALUES ({placeholders})
        ''', list(member_data.values()))
        
        conn.commit()
        conn.close()
    
    def get_team_members(self, project_id):
        conn = self.get_connection()
        df = pd.read_sql_query(
            "SELECT * FROM team_members WHERE project_id = ?",
            conn,
            params=(project_id,)
        )
        conn.close()
        return df
    
    def delete_team_member(self, member_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM team_members WHERE id = ?", (member_id,))
        conn.commit()
        conn.close()
    
    # ===== QUẢN LÝ STAKEHOLDERS =====
    def add_stakeholder(self, stakeholder_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        columns = ', '.join(stakeholder_data.keys())
        placeholders = ', '.join(['?' for _ in stakeholder_data])
        
        cursor.execute(f'''
            INSERT INTO stakeholders ({columns})
            VALUES ({placeholders})
        ''', list(stakeholder_data.values()))
        
        conn.commit()
        conn.close()
    
    def get_stakeholders(self, project_id):
        conn = self.get_connection()
        df = pd.read_sql_query(
            "SELECT * FROM stakeholders WHERE project_id = ?",
            conn,
            params=(project_id,)
        )
        conn.close()
        return df
    
    def delete_stakeholder(self, stakeholder_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stakeholders WHERE id = ?", (stakeholder_id,))
        conn.commit()
        conn.close()
    
    # ===== QUẢN LÝ TASKS (GANTT) =====
    def add_task(self, task_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        columns = ', '.join(task_data.keys())
        placeholders = ', '.join(['?' for _ in task_data])
        
        cursor.execute(f'''
            INSERT INTO project_tasks ({columns})
            VALUES ({placeholders})
        ''', list(task_data.values()))
        
        conn.commit()
        conn.close()
    
    def get_tasks(self, project_id):
        conn = self.get_connection()
        df = pd.read_sql_query(
            "SELECT * FROM project_tasks WHERE project_id = ? ORDER BY start_date",
            conn,
            params=(project_id,)
        )
        conn.close()
        return df
    
    def update_task(self, task_id, task_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        set_clause = ', '.join([f"{key} = ?" for key in task_data.keys()])
        values = list(task_data.values()) + [task_id]
        
        cursor.execute(f'''
            UPDATE project_tasks
            SET {set_clause}
            WHERE id = ?
        ''', values)
        
        conn.commit()
        conn.close()
    
    def delete_task(self, task_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM project_tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
    
    # ===== QUẢN LÝ KÝ TÊN =====
    def add_signoff(self, signoff_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        columns = ', '.join(signoff_data.keys())
        placeholders = ', '.join(['?' for _ in signoff_data])
        
        cursor.execute(f'''
            INSERT INTO signoffs ({columns})
            VALUES ({placeholders})
        ''', list(signoff_data.values()))
        
        conn.commit()
        conn.close()
    
    def get_signoffs(self, project_id):
        conn = self.get_connection()
        df = pd.read_sql_query(
            "SELECT * FROM signoffs WHERE project_id = ?",
            conn,
            params=(project_id,)
        )
        conn.close()
        return df
    
    def delete_signoff(self, signoff_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM signoffs WHERE id = ?", (signoff_id,))
        conn.commit()
        conn.close()
    
    # ===== QUẢN LÝ PHÒNG BAN =====
    def add_department(self, name, description=""):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO departments (name, description)
                VALUES (?, ?)
            ''', (name, description))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False
    
    def get_departments(self):
        conn = self.get_connection()
        df = pd.read_sql_query("SELECT * FROM departments ORDER BY name", conn)
        conn.close()
        return df
    
    def delete_department(self, dept_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM departments WHERE id = ?", (dept_id,))
        conn.commit()
        conn.close()
    
    # ===== THỐNG KÊ =====
    def get_statistics(self):
        conn = self.get_connection()
        
        # Tổng số dự án
        total_projects = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM projects", conn
        ).iloc[0]['count']
        
        # Dự án theo trạng thái
        by_status = pd.read_sql_query(
            "SELECT status, COUNT(*) as count FROM projects GROUP BY status", conn
        )
        
        # Dự án theo danh mục
        by_category = pd.read_sql_query(
            "SELECT category, COUNT(*) as count FROM projects GROUP BY category", conn
        )
        
        # Dự án theo phòng ban
        by_department = pd.read_sql_query(
            "SELECT department, COUNT(*) as count FROM projects GROUP BY department", conn
        )
        
        # Tổng ngân sách
        budget_stats = pd.read_sql_query(
            "SELECT SUM(budget) as total_budget, SUM(actual_cost) as total_cost FROM projects", conn
        )
        
        conn.close()
        
        return {
            'total_projects': total_projects,
            'by_status': by_status,
            'by_category': by_category,
            'by_department': by_department,
            'budget_stats': budget_stats
        }
    
    # ===== COLLABORATION - COMMENTS =====
    def add_comment(self, comment_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        comment_data['created_at'] = datetime.now().isoformat()
        comment_data['updated_at'] = datetime.now().isoformat()
        
        columns = ', '.join(comment_data.keys())
        placeholders = ', '.join(['?' for _ in comment_data])
        
        cursor.execute(f'''
            INSERT INTO comments ({columns})
            VALUES ({placeholders})
        ''', list(comment_data.values()))
        
        conn.commit()
        comment_id = cursor.lastrowid
        conn.close()
        
        return comment_id
    
    def get_comments(self, project_id):
        conn = self.get_connection()
        df = pd.read_sql_query(
            "SELECT * FROM comments WHERE project_id = ? ORDER BY created_at DESC",
            conn,
            params=(project_id,)
        )
        conn.close()
        return df
    
    def get_comment_thread(self, comment_id):
        """Get comment and all its replies"""
        conn = self.get_connection()
        df = pd.read_sql_query(
            "SELECT * FROM comments WHERE id = ? OR parent_comment_id = ? ORDER BY created_at ASC",
            conn,
            params=(comment_id, comment_id)
        )
        conn.close()
        return df
    
    def update_comment(self, comment_id, comment_text):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE comments 
            SET comment_text = ?, updated_at = ?
            WHERE id = ?
        ''', (comment_text, datetime.now().isoformat(), comment_id))
        
        conn.commit()
        conn.close()
    
    def delete_comment(self, comment_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        conn.commit()
        conn.close()
    
    # ===== NOTIFICATIONS =====
    def add_notification(self, notification_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        notification_data['created_at'] = datetime.now().isoformat()
        
        columns = ', '.join(notification_data.keys())
        placeholders = ', '.join(['?' for _ in notification_data])
        
        cursor.execute(f'''
            INSERT INTO notifications ({columns})
            VALUES ({placeholders})
        ''', list(notification_data.values()))
        
        conn.commit()
        notification_id = cursor.lastrowid
        conn.close()
        
        return notification_id
    
    def get_notifications(self, recipient_email=None, project_id=None, unread_only=False):
        conn = self.get_connection()
        
        query = "SELECT * FROM notifications WHERE 1=1"
        params = []
        
        if recipient_email:
            query += " AND recipient_email = ?"
            params.append(recipient_email)
        
        if project_id:
            query += " AND project_id = ?"
            params.append(project_id)
        
        if unread_only:
            query += " AND is_read = 0"
        
        query += " ORDER BY created_at DESC"
        
        df = pd.read_sql_query(query, conn, params=params if params else None)
        conn.close()
        return df
    
    def mark_notification_read(self, notification_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE notifications 
            SET is_read = 1
            WHERE id = ?
        ''', (notification_id,))
        
        conn.commit()
        conn.close()
    
    def delete_notification(self, notification_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
        conn.commit()
        conn.close()
    
    # ===== ACTIVITY LOG =====
    def log_activity(self, activity_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        activity_data['created_at'] = datetime.now().isoformat()
        
        columns = ', '.join(activity_data.keys())
        placeholders = ', '.join(['?' for _ in activity_data])
        
        cursor.execute(f'''
            INSERT INTO activity_log ({columns})
            VALUES ({placeholders})
        ''', list(activity_data.values()))
        
        conn.commit()
        activity_id = cursor.lastrowid
        conn.close()
        
        return activity_id
    
    def get_activity_log(self, project_id=None, limit=100):
        conn = self.get_connection()
        
        if project_id:
            df = pd.read_sql_query(
                "SELECT * FROM activity_log WHERE project_id = ? ORDER BY created_at DESC LIMIT ?",
                conn,
                params=(project_id, limit)
            )
        else:
            df = pd.read_sql_query(
                "SELECT * FROM activity_log ORDER BY created_at DESC LIMIT ?",
                conn,
                params=(limit,)
            )
        
        conn.close()
        return df
    
    # ===== MEETINGS =====
    def add_meeting(self, meeting_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        meeting_data['created_at'] = datetime.now().isoformat()
        meeting_data['updated_at'] = datetime.now().isoformat()
        
        columns = ', '.join(meeting_data.keys())
        placeholders = ', '.join(['?' for _ in meeting_data])
        
        cursor.execute(f'''
            INSERT INTO meetings ({columns})
            VALUES ({placeholders})
        ''', list(meeting_data.values()))
        
        conn.commit()
        meeting_id = cursor.lastrowid
        conn.close()
        
        return meeting_id
    
    def get_meetings(self, project_id):
        conn = self.get_connection()
        df = pd.read_sql_query(
            "SELECT * FROM meetings WHERE project_id = ? ORDER BY meeting_date DESC",
            conn,
            params=(project_id,)
        )
        conn.close()
        return df
    
    def get_meeting(self, meeting_id):
        conn = self.get_connection()
        df = pd.read_sql_query(
            "SELECT * FROM meetings WHERE id = ?",
            conn,
            params=(meeting_id,)
        )
        conn.close()
        return df
    
    def update_meeting(self, meeting_id, meeting_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        meeting_data['updated_at'] = datetime.now().isoformat()
        
        set_clause = ', '.join([f"{key} = ?" for key in meeting_data.keys()])
        values = list(meeting_data.values())
        values.append(meeting_id)
        
        cursor.execute(f'''
            UPDATE meetings 
            SET {set_clause}
            WHERE id = ?
        ''', values)
        
        conn.commit()
        conn.close()
    
    def delete_meeting(self, meeting_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM meetings WHERE id = ?", (meeting_id,))
        conn.commit()
        conn.close()
    
    # ===== ACTION ITEMS =====
    def add_action_item(self, action_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        action_data['created_at'] = datetime.now().isoformat()
        
        columns = ', '.join(action_data.keys())
        placeholders = ', '.join(['?' for _ in action_data])
        
        cursor.execute(f'''
            INSERT INTO action_items ({columns})
            VALUES ({placeholders})
        ''', list(action_data.values()))
        
        conn.commit()
        action_id = cursor.lastrowid
        conn.close()
        
        return action_id
    
    def get_action_items(self, meeting_id=None, project_id=None, status=None):
        conn = self.get_connection()
        
        query = "SELECT * FROM action_items WHERE 1=1"
        params = []
        
        if meeting_id:
            query += " AND meeting_id = ?"
            params.append(meeting_id)
        
        if project_id:
            query += " AND project_id = ?"
            params.append(project_id)
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " ORDER BY due_date ASC, priority DESC"
        
        df = pd.read_sql_query(query, conn, params=params if params else None)
        conn.close()
        return df
    
    def update_action_item(self, action_id, action_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if action_data.get('status') == 'Completed':
            action_data['completed_at'] = datetime.now().isoformat()
        
        set_clause = ', '.join([f"{key} = ?" for key in action_data.keys()])
        values = list(action_data.values())
        values.append(action_id)
        
        cursor.execute(f'''
            UPDATE action_items 
            SET {set_clause}
            WHERE id = ?
        ''', values)
        
        conn.commit()
        conn.close()
    
    def delete_action_item(self, action_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM action_items WHERE id = ?", (action_id,))
        conn.commit()
        conn.close()

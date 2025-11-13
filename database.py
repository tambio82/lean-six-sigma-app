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

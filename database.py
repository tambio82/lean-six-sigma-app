import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text, Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import streamlit as st

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_code = Column(String(50), unique=True, nullable=False)
    project_name = Column(Text, nullable=False)
    department = Column(String(200))
    start_date = Column(String(20))
    end_date = Column(String(20))
    status = Column(String(50))
    category = Column(String(100))
    description = Column(Text)
    problem_statement = Column(Text)
    goal = Column(Text)
    scope = Column(Text)
    budget = Column(Float)
    actual_cost = Column(Float)
    created_at = Column(String(30))
    updated_at = Column(String(30))
    
    team_members = relationship("TeamMember", back_populates="project", cascade="all, delete-orphan")
    stakeholders = relationship("Stakeholder", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("ProjectTask", back_populates="project", cascade="all, delete-orphan")
    signoffs = relationship("Signoff", back_populates="project", cascade="all, delete-orphan")

class TeamMember(Base):
    __tablename__ = 'team_members'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    name = Column(Text, nullable=False)
    role = Column(String(100))
    department = Column(String(200))
    email = Column(String(200))
    phone = Column(String(50))
    
    project = relationship("Project", back_populates="team_members")

class Stakeholder(Base):
    __tablename__ = 'stakeholders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    name = Column(Text, nullable=False)
    role = Column(String(100))
    department = Column(String(200))
    impact_level = Column(String(50))
    engagement_level = Column(String(50))
    
    project = relationship("Project", back_populates="stakeholders")

class ProjectTask(Base):
    __tablename__ = 'project_tasks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    phase = Column(String(50))
    task_name = Column(Text, nullable=False)
    start_date = Column(String(20))
    end_date = Column(String(20))
    responsible = Column(String(200))
    status = Column(String(50))
    progress = Column(Integer)
    
    project = relationship("Project", back_populates="tasks")

class Signoff(Base):
    __tablename__ = 'signoffs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    role = Column(Text, nullable=False)
    name = Column(String(200))
    signature = Column(Text)
    date = Column(String(20))
    notes = Column(Text)
    
    project = relationship("Project", back_populates="signoffs")

class Department(Base):
    __tablename__ = 'departments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), unique=True, nullable=False)
    description = Column(Text)

class ProjectDatabase:
    def __init__(self, connection_string=None):
        """
        Initialize database connection
        If connection_string is None, try to get from Streamlit secrets
        """
        if connection_string is None:
            try:
                # Try to get from Streamlit secrets
                connection_string = st.secrets["connections"]["postgresql"]["url"]
            except Exception as e:
                st.error(f"Không thể kết nối database. Vui lòng kiểm tra cấu hình secrets!")
                st.error(f"Chi tiết lỗi: {str(e)}")
                raise
        
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self.init_database()
    
    def init_database(self):
        """Create all tables if they don't exist"""
        Base.metadata.create_all(self.engine)
    
    def get_connection(self):
        """Get raw connection for pandas operations"""
        return self.engine.connect()
    
    # ===== QUẢN LÝ DỰ ÁN =====
    def add_project(self, project_data):
        session = self.Session()
        try:
            now = datetime.now().isoformat()
            project_data['created_at'] = now
            project_data['updated_at'] = now
            
            project = Project(**project_data)
            session.add(project)
            session.commit()
            project_id = project.id
            return project_id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def update_project(self, project_id, project_data):
        session = self.Session()
        try:
            project_data['updated_at'] = datetime.now().isoformat()
            
            session.query(Project).filter(Project.id == project_id).update(project_data)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_project(self, project_id):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM projects WHERE id = %(id)s",
                conn,
                params={"id": project_id}
            )
            
            if len(df) > 0:
                return df.iloc[0].to_dict()
            return None
        finally:
            conn.close()
    
    def get_all_projects(self):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query("SELECT * FROM projects ORDER BY created_at DESC", conn)
            return df
        finally:
            conn.close()
    
    def delete_project(self, project_id):
        session = self.Session()
        try:
            session.query(Project).filter(Project.id == project_id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    # ===== QUẢN LÝ THÀNH VIÊN =====
    def add_team_member(self, member_data):
        session = self.Session()
        try:
            member = TeamMember(**member_data)
            session.add(member)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_team_members(self, project_id):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM team_members WHERE project_id = %(id)s",
                conn,
                params={"id": project_id}
            )
            return df
        finally:
            conn.close()
    
    def delete_team_member(self, member_id):
        session = self.Session()
        try:
            session.query(TeamMember).filter(TeamMember.id == member_id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    # ===== QUẢN LÝ STAKEHOLDERS =====
    def add_stakeholder(self, stakeholder_data):
        session = self.Session()
        try:
            stakeholder = Stakeholder(**stakeholder_data)
            session.add(stakeholder)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_stakeholders(self, project_id):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM stakeholders WHERE project_id = %(id)s",
                conn,
                params={"id": project_id}
            )
            return df
        finally:
            conn.close()
    
    def delete_stakeholder(self, stakeholder_id):
        session = self.Session()
        try:
            session.query(Stakeholder).filter(Stakeholder.id == stakeholder_id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    # ===== QUẢN LÝ TASKS (GANTT) =====
    def add_task(self, task_data):
        session = self.Session()
        try:
            task = ProjectTask(**task_data)
            session.add(task)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_tasks(self, project_id):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM project_tasks WHERE project_id = %(id)s ORDER BY start_date",
                conn,
                params={"id": project_id}
            )
            return df
        finally:
            conn.close()
    
    def update_task(self, task_id, task_data):
        session = self.Session()
        try:
            session.query(ProjectTask).filter(ProjectTask.id == task_id).update(task_data)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete_task(self, task_id):
        session = self.Session()
        try:
            session.query(ProjectTask).filter(ProjectTask.id == task_id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    # ===== QUẢN LÝ KÝ TÊN =====
    def add_signoff(self, signoff_data):
        session = self.Session()
        try:
            signoff = Signoff(**signoff_data)
            session.add(signoff)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_signoffs(self, project_id):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM signoffs WHERE project_id = %(id)s",
                conn,
                params={"id": project_id}
            )
            return df
        finally:
            conn.close()
    
    def delete_signoff(self, signoff_id):
        session = self.Session()
        try:
            session.query(Signoff).filter(Signoff.id == signoff_id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    # ===== QUẢN LÝ PHÒNG BAN =====
    def add_department(self, name, description=""):
        session = self.Session()
        try:
            department = Department(name=name, description=description)
            session.add(department)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()
    
    def get_departments(self):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query("SELECT * FROM departments ORDER BY name", conn)
            return df
        finally:
            conn.close()
    
    def delete_department(self, dept_id):
        session = self.Session()
        try:
            session.query(Department).filter(Department.id == dept_id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    # ===== THỐNG KÊ =====
    def get_statistics(self):
        conn = self.get_connection()
        try:
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
            
            return {
                'total_projects': total_projects,
                'by_status': by_status,
                'by_category': by_category,
                'by_department': by_department,
                'budget_stats': budget_stats
            }
        finally:
            conn.close()

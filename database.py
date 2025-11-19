import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text, Column, Integer, String, Float, Text, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import streamlit as st
import json as json_module

Base = declarative_base()

# ==================== EXISTING MODELS ====================

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
    methodology = Column(String(20), default='DMAIC')  # NEW: DMAIC, PDCA, PDSA
    description = Column(Text)
    problem_statement = Column(Text)
    goal = Column(Text)
    scope = Column(Text)
    budget = Column(Float)
    actual_cost = Column(Float)
    created_at = Column(String(30))
    updated_at = Column(String(30))
    
    # Relationships
    team_members = relationship("TeamMember", back_populates="project", cascade="all, delete-orphan")
    stakeholders = relationship("Stakeholder", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("ProjectTask", back_populates="project", cascade="all, delete-orphan")
    signoffs = relationship("Signoff", back_populates="project", cascade="all, delete-orphan")
    documents = relationship("ProjectDocument", back_populates="project", cascade="all, delete-orphan")
    comments = relationship("ProjectComment", back_populates="project", cascade="all, delete-orphan")
    activities = relationship("ActivityLog", back_populates="project", cascade="all, delete-orphan")
    meetings = relationship("MeetingMinute", back_populates="project", cascade="all, delete-orphan")

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

# ==================== NEW MODELS FOR FEATURE 1: DMAIC TRACKING ====================

class DMAICDefine(Base):
    __tablename__ = 'dmaic_define'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    
    # SIPOC
    sipoc_suppliers = Column(Text)  # JSON array
    sipoc_inputs = Column(Text)
    sipoc_process = Column(Text)
    sipoc_outputs = Column(Text)
    sipoc_customers = Column(Text)
    
    # Project Charter
    charter_business_case = Column(Text)
    charter_objectives = Column(Text)
    charter_scope = Column(Text)
    charter_milestones = Column(Text)
    
    # Voice of Customer
    voc_data = Column(Text)  # JSON array of VOC entries
    voc_summary = Column(Text)
    
    created_at = Column(String(30))
    updated_at = Column(String(30))

class DMAICMeasure(Base):
    __tablename__ = 'dmaic_measure'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    
    # Data Collection
    data_collection_plan = Column(Text)
    data_sources = Column(Text)
    
    # Baseline Metrics
    baseline_metrics = Column(Text)  # JSON with metrics
    current_state = Column(Text)
    measurement_system = Column(Text)
    
    # Process Map
    process_map_data = Column(Text)  # JSON for flowchart
    process_map_image = Column(Text)  # Base64 or URL
    
    created_at = Column(String(30))
    updated_at = Column(String(30))

class DMAICAnalyze(Base):
    __tablename__ = 'dmaic_analyze'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    
    # Root Cause Analysis
    fishbone_categories = Column(Text)  # JSON with categories and causes
    five_whys_data = Column(Text)  # JSON array
    
    # Pareto Analysis
    pareto_data = Column(Text)  # JSON with categories and frequencies
    pareto_chart_config = Column(Text)
    
    # Statistical Analysis
    statistical_data = Column(Text)  # JSON with mean, median, std, etc.
    analysis_summary = Column(Text)
    
    created_at = Column(String(30))
    updated_at = Column(String(30))

class DMAICImprove(Base):
    __tablename__ = 'dmaic_improve'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    
    # Solution Brainstorming
    solutions_brainstormed = Column(Text)  # JSON array
    solutions_selected = Column(Text)
    selection_criteria = Column(Text)
    
    # Pilot Testing
    pilot_test_plan = Column(Text)
    pilot_test_results = Column(Text)
    pilot_test_status = Column(String(50))
    
    # Before/After Comparison
    before_data = Column(Text)  # JSON
    after_data = Column(Text)
    comparison_metrics = Column(Text)
    
    created_at = Column(String(30))
    updated_at = Column(String(30))

class DMAICControl(Base):
    __tablename__ = 'dmaic_control'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    
    # Control Plan
    control_plan = Column(Text)  # JSON with control items
    monitoring_frequency = Column(String(50))
    responsible_person = Column(String(200))
    
    # SOPs
    sop_documents = Column(Text)  # JSON array with SOP details
    sop_training_status = Column(Text)
    
    # Monitoring
    monitoring_metrics = Column(Text)  # JSON
    sustainability_plan = Column(Text)
    
    created_at = Column(String(30))
    updated_at = Column(String(30))

# ==================== NEW MODELS FOR FEATURE 2: PDCA/PDSA ====================

class MethodologyPhase(Base):
    __tablename__ = 'methodology_phases'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    methodology = Column(String(20))  # DMAIC, PDCA, PDSA
    phase_name = Column(String(50))  # Define/Plan, Measure/Do, etc.
    phase_order = Column(Integer)
    
    # Generic fields for all methodologies
    phase_description = Column(Text)
    phase_objectives = Column(Text)
    phase_activities = Column(Text)  # JSON array
    phase_deliverables = Column(Text)
    phase_status = Column(String(50))  # Not Started, In Progress, Completed
    phase_completion_date = Column(String(20))
    
    # Data storage
    phase_data = Column(Text)  # JSON for methodology-specific data
    
    created_at = Column(String(30))
    updated_at = Column(String(30))

# ==================== NEW MODELS FOR FEATURE 3: DOCUMENTS ====================

class ProjectDocument(Base):
    __tablename__ = 'project_documents'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    
    document_name = Column(String(500), nullable=False)
    document_type = Column(String(100))  # A3, PDCA, 5S, Risk, FMEA, etc.
    document_category = Column(String(100))  # Template, Report, SOP, etc.
    file_path = Column(Text)  # For cloud storage
    file_content = Column(Text)  # For storing small files as base64
    file_size = Column(Integer)
    mime_type = Column(String(100))
    
    uploaded_by = Column(String(200))
    version = Column(Integer, default=1)
    is_latest = Column(Boolean, default=True)
    
    tags = Column(Text)  # JSON array for search
    description = Column(Text)
    
    created_at = Column(String(30))
    updated_at = Column(String(30))
    
    project = relationship("Project", back_populates="documents")
    versions = relationship("DocumentVersion", back_populates="document", cascade="all, delete-orphan")

class DocumentVersion(Base):
    __tablename__ = 'document_versions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey('project_documents.id', ondelete='CASCADE'))
    
    version_number = Column(Integer, nullable=False)
    file_content = Column(Text)
    change_description = Column(Text)
    modified_by = Column(String(200))
    modified_at = Column(String(30))
    
    document = relationship("ProjectDocument", back_populates="versions")

# ==================== NEW MODELS FOR FEATURE 4: COLLABORATION ====================

class ProjectComment(Base):
    __tablename__ = 'project_comments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    
    comment_text = Column(Text, nullable=False)
    author = Column(String(200), nullable=False)
    author_email = Column(String(200))
    
    # Threading support
    parent_comment_id = Column(Integer, ForeignKey('project_comments.id'))
    
    # Mentions
    mentions = Column(Text)  # JSON array of mentioned users
    
    # Metadata
    is_edited = Column(Boolean, default=False)
    created_at = Column(String(30))
    updated_at = Column(String(30))
    
    project = relationship("Project", back_populates="comments")

class ActivityLog(Base):
    __tablename__ = 'activity_log'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    
    activity_type = Column(String(50))  # created, updated, status_changed, etc.
    activity_description = Column(Text)
    user = Column(String(200))
    user_email = Column(String(200))
    
    # Details
    old_value = Column(Text)
    new_value = Column(Text)
    affected_field = Column(String(100))
    
    timestamp = Column(String(30))
    
    project = relationship("Project", back_populates="activities")

class Notification(Base):
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    
    notification_type = Column(String(50))  # assignment, deadline, signoff, milestone
    title = Column(String(500))
    message = Column(Text)
    
    recipient_email = Column(String(200))
    recipient_name = Column(String(200))
    
    is_read = Column(Boolean, default=False)
    is_sent = Column(Boolean, default=False)
    sent_at = Column(String(30))
    
    created_at = Column(String(30))

class MeetingMinute(Base):
    __tablename__ = 'meeting_minutes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    
    meeting_title = Column(String(500), nullable=False)
    meeting_date = Column(String(20))
    meeting_time = Column(String(20))
    location = Column(String(200))
    
    attendees = Column(Text)  # JSON array
    absent = Column(Text)  # JSON array
    
    agenda = Column(Text)
    discussion_notes = Column(Text)
    
    # Action Items
    action_items = Column(Text)  # JSON array with {item, assignee, due_date, status}
    
    # Decisions
    decisions = Column(Text)  # JSON array
    
    # Next meeting
    next_meeting_date = Column(String(20))
    next_meeting_agenda = Column(Text)
    
    created_by = Column(String(200))
    created_at = Column(String(30))
    updated_at = Column(String(30))
    
    project = relationship("Project", back_populates="meetings")

# ==================== DATABASE CLASS ====================

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
    
    # ===== EXISTING PROJECT MANAGEMENT METHODS =====
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
    
    # ===== TEAM MEMBERS =====
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
    
    # ===== STAKEHOLDERS =====
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
    
    # ===== TASKS =====
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
    
    # ===== SIGNOFFS =====
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
    
    # ===== DEPARTMENTS =====
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
    
    # ===== STATISTICS =====
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
    
    # ==================== NEW METHODS FOR DMAIC TRACKING ====================
    
    # DMAIC Define
    def save_dmaic_define(self, project_id, define_data):
        session = self.Session()
        try:
            now = datetime.now().isoformat()
            define_data['created_at'] = now
            define_data['updated_at'] = now
            define_data['project_id'] = project_id
            
            # Check if exists
            existing = session.query(DMAICDefine).filter(
                DMAICDefine.project_id == project_id
            ).first()
            
            if existing:
                for key, value in define_data.items():
                    setattr(existing, key, value)
            else:
                new_define = DMAICDefine(**define_data)
                session.add(new_define)
            
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_dmaic_define(self, project_id):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM dmaic_define WHERE project_id = %(id)s",
                conn,
                params={"id": project_id}
            )
            if len(df) > 0:
                return df.iloc[0].to_dict()
            return None
        finally:
            conn.close()
    
    # DMAIC Measure
    def save_dmaic_measure(self, project_id, measure_data):
        session = self.Session()
        try:
            now = datetime.now().isoformat()
            measure_data['created_at'] = now
            measure_data['updated_at'] = now
            measure_data['project_id'] = project_id
            
            existing = session.query(DMAICMeasure).filter(
                DMAICMeasure.project_id == project_id
            ).first()
            
            if existing:
                for key, value in measure_data.items():
                    setattr(existing, key, value)
            else:
                new_measure = DMAICMeasure(**measure_data)
                session.add(new_measure)
            
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_dmaic_measure(self, project_id):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM dmaic_measure WHERE project_id = %(id)s",
                conn,
                params={"id": project_id}
            )
            if len(df) > 0:
                return df.iloc[0].to_dict()
            return None
        finally:
            conn.close()
    
    # DMAIC Analyze
    def save_dmaic_analyze(self, project_id, analyze_data):
        session = self.Session()
        try:
            now = datetime.now().isoformat()
            analyze_data['created_at'] = now
            analyze_data['updated_at'] = now
            analyze_data['project_id'] = project_id
            
            existing = session.query(DMAICAnalyze).filter(
                DMAICAnalyze.project_id == project_id
            ).first()
            
            if existing:
                for key, value in analyze_data.items():
                    setattr(existing, key, value)
            else:
                new_analyze = DMAICAnalyze(**analyze_data)
                session.add(new_analyze)
            
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_dmaic_analyze(self, project_id):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM dmaic_analyze WHERE project_id = %(id)s",
                conn,
                params={"id": project_id}
            )
            if len(df) > 0:
                return df.iloc[0].to_dict()
            return None
        finally:
            conn.close()
    
    # DMAIC Improve
    def save_dmaic_improve(self, project_id, improve_data):
        session = self.Session()
        try:
            now = datetime.now().isoformat()
            improve_data['created_at'] = now
            improve_data['updated_at'] = now
            improve_data['project_id'] = project_id
            
            existing = session.query(DMAICImprove).filter(
                DMAICImprove.project_id == project_id
            ).first()
            
            if existing:
                for key, value in improve_data.items():
                    setattr(existing, key, value)
            else:
                new_improve = DMAICImprove(**improve_data)
                session.add(new_improve)
            
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_dmaic_improve(self, project_id):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM dmaic_improve WHERE project_id = %(id)s",
                conn,
                params={"id": project_id}
            )
            if len(df) > 0:
                return df.iloc[0].to_dict()
            return None
        finally:
            conn.close()
    
    # DMAIC Control
    def save_dmaic_control(self, project_id, control_data):
        session = self.Session()
        try:
            now = datetime.now().isoformat()
            control_data['created_at'] = now
            control_data['updated_at'] = now
            control_data['project_id'] = project_id
            
            existing = session.query(DMAICControl).filter(
                DMAICControl.project_id == project_id
            ).first()
            
            if existing:
                for key, value in control_data.items():
                    setattr(existing, key, value)
            else:
                new_control = DMAICControl(**control_data)
                session.add(new_control)
            
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_dmaic_control(self, project_id):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM dmaic_control WHERE project_id = %(id)s",
                conn,
                params={"id": project_id}
            )
            if len(df) > 0:
                return df.iloc[0].to_dict()
            return None
        finally:
            conn.close()
    
    # ==================== NEW METHODS FOR METHODOLOGY PHASES ====================
    
    def save_methodology_phase(self, phase_data):
        session = self.Session()
        try:
            now = datetime.now().isoformat()
            phase_data['created_at'] = now
            phase_data['updated_at'] = now
            
            phase = MethodologyPhase(**phase_data)
            session.add(phase)
            session.commit()
            return phase.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_methodology_phases(self, project_id):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM methodology_phases WHERE project_id = %(id)s ORDER BY phase_order",
                conn,
                params={"id": project_id}
            )
            return df
        finally:
            conn.close()
    
    def update_methodology_phase(self, phase_id, phase_data):
        session = self.Session()
        try:
            phase_data['updated_at'] = datetime.now().isoformat()
            session.query(MethodologyPhase).filter(MethodologyPhase.id == phase_id).update(phase_data)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    # ==================== NEW METHODS FOR DOCUMENTS ====================
    
    def add_document(self, document_data):
        session = self.Session()
        try:
            now = datetime.now().isoformat()
            document_data['created_at'] = now
            document_data['updated_at'] = now
            
            document = ProjectDocument(**document_data)
            session.add(document)
            session.commit()
            return document.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_documents(self, project_id):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM project_documents WHERE project_id = %(id)s AND is_latest = true ORDER BY created_at DESC",
                conn,
                params={"id": project_id}
            )
            return df
        finally:
            conn.close()
    
    def get_document(self, document_id):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM project_documents WHERE id = %(id)s",
                conn,
                params={"id": document_id}
            )
            if len(df) > 0:
                return df.iloc[0].to_dict()
            return None
        finally:
            conn.close()
    
    def add_document_version(self, version_data):
        session = self.Session()
        try:
            version = DocumentVersion(**version_data)
            session.add(version)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete_document(self, document_id):
        session = self.Session()
        try:
            session.query(ProjectDocument).filter(ProjectDocument.id == document_id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    # ==================== NEW METHODS FOR COLLABORATION ====================
    
    # Comments
    def add_comment(self, comment_data):
        session = self.Session()
        try:
            now = datetime.now().isoformat()
            comment_data['created_at'] = now
            comment_data['updated_at'] = now
            
            comment = ProjectComment(**comment_data)
            session.add(comment)
            session.commit()
            return comment.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_comments(self, project_id):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM project_comments WHERE project_id = %(id)s ORDER BY created_at DESC",
                conn,
                params={"id": project_id}
            )
            return df
        finally:
            conn.close()
    
    # Activity Log
    def log_activity(self, activity_data):
        session = self.Session()
        try:
            activity_data['timestamp'] = datetime.now().isoformat()
            activity = ActivityLog(**activity_data)
            session.add(activity)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_activities(self, project_id):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM activity_log WHERE project_id = %(id)s ORDER BY timestamp DESC LIMIT 50",
                conn,
                params={"id": project_id}
            )
            return df
        finally:
            conn.close()
    
    # Notifications
    def create_notification(self, notification_data):
        session = self.Session()
        try:
            notification_data['created_at'] = datetime.now().isoformat()
            notification = Notification(**notification_data)
            session.add(notification)
            session.commit()
            return notification.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_notifications(self, recipient_email):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM notifications WHERE recipient_email = %(email)s AND is_read = false ORDER BY created_at DESC",
                conn,
                params={"email": recipient_email}
            )
            return df
        finally:
            conn.close()
    
    def mark_notification_read(self, notification_id):
        session = self.Session()
        try:
            session.query(Notification).filter(
                Notification.id == notification_id
            ).update({'is_read': True})
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    # Meeting Minutes
    def add_meeting(self, meeting_data):
        session = self.Session()
        try:
            now = datetime.now().isoformat()
            meeting_data['created_at'] = now
            meeting_data['updated_at'] = now
            
            meeting = MeetingMinute(**meeting_data)
            session.add(meeting)
            session.commit()
            return meeting.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_meetings(self, project_id):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM meeting_minutes WHERE project_id = %(id)s ORDER BY meeting_date DESC",
                conn,
                params={"id": project_id}
            )
            return df
        finally:
            conn.close()
    
    def get_meeting(self, meeting_id):
        conn = self.get_connection()
        try:
            df = pd.read_sql_query(
                "SELECT * FROM meeting_minutes WHERE id = %(id)s",
                conn,
                params={"id": meeting_id}
            )
            if len(df) > 0:
                return df.iloc[0].to_dict()
            return None
        finally:
            conn.close()
    
    def update_meeting(self, meeting_id, meeting_data):
        session = self.Session()
        try:
            meeting_data['updated_at'] = datetime.now().isoformat()
            session.query(MeetingMinute).filter(MeetingMinute.id == meeting_id).update(meeting_data)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

# ========================================
# APP.PY UPDATE CODE SNIPPET
# Copy và paste vào app.py của bạn
# ========================================

# ==================== STEP 1: UPDATE IMPORTS ====================
# Tìm dòng 12 trong app.py (sau "from dmaic_tools import DMAICTools")
# THÊM dòng này:

from pdca_pdsa_tools import PDCATools  # ← THÊM DÒNG NÀY

# Sau khi thêm, section import sẽ trông như thế này:
"""
from database import ProjectDatabase
from dmaic_tools import DMAICTools
from pdca_pdsa_tools import PDCATools  # ← MỚI
from collaboration import render_collaboration_tab, initialize_collaboration
from gantt_chart import (
    create_gantt_chart, create_dmaic_gantt, 
    get_project_progress, get_phase_summary, 
    check_overdue_tasks
)
"""


# ==================== STEP 2: REPLACE FUNCTION ====================
# Tìm function render_dmaic_tracking (dòng 308-343)
# XÓA toàn bộ function cũ và THAY BẰNG code sau:

def render_dmaic_tracking(project_id, project):
    """
    Render methodology tracking interface - supports DMAIC, PDCA, PDSA
    
    UPDATED: Now supports all 3 methodologies
    """
    methodology = project.get('methodology', 'DMAIC')
    
    # Hiển thị methodology badge
    methodology_icons = {
        'DMAIC': '🔵',
        'PDCA': '🟢',
        'PDSA': '🟡'
    }
    
    st.write(f"{methodology_icons.get(methodology, '⚪')} **Phương pháp:** {methodology}")
    
    if methodology == 'DMAIC':
        # Render DMAIC tools (existing)
        dmaic_tools = DMAICTools(db)
        dmaic_tools.render_dmaic_tracker(project_id, project)
    
    elif methodology in ['PDCA', 'PDSA']:
        # ← MỚI: Render PDCA/PDSA tools
        pdca_tools = PDCATools(db)
        pdca_tools.render_pdca_interface(project_id, methodology)
    
    else:
        st.warning("Vui lòng chọn phương pháp cải tiến cho dự án trong tab **Thông tin**")


# ==================== THAT'S IT! ====================
# Chỉ cần 2 thay đổi đơn giản:
# 1. Thêm 1 dòng import
# 2. Thay 1 function (35 dòng → 25 dòng)
# 
# Sau đó:
# - Save file
# - Git push
# - Streamlit Cloud sẽ tự động redeploy!
# ========================================


# ==================== VERIFICATION ====================
# Sau khi update, kiểm tra:
# 1. App khởi động không lỗi
# 2. Tạo project với methodology = PDCA
# 3. Vào tab "Tracking" sẽ thấy 4 tabs: Plan, Do, Check, Act
# 4. Tạo project với methodology = PDSA  
# 5. Vào tab "Tracking" sẽ thấy 4 tabs: Plan, Do, Study, Act
# 6. DMAIC projects vẫn hiển thị 5 tabs: Define, Measure, Analyze, Improve, Control
# ========================================


# ==================== OPTIONAL: ADD METHODOLOGY COLUMN ====================
# Nếu database chưa có cột 'methodology', thêm vào Supabase:

"""
ALTER TABLE projects 
ADD COLUMN IF NOT EXISTS methodology VARCHAR(10) DEFAULT 'DMAIC';

-- Có thể set giá trị mặc định:
UPDATE projects 
SET methodology = 'DMAIC' 
WHERE methodology IS NULL;
"""

# ==================== DATABASE METHODS CHECK ====================
# Nếu gặp lỗi "method not found", thêm vào database.py:

"""
# ==================== PDCA/PDSA HELPER METHODS ====================

def get_pdca_data(self, project_id, methodology, phase, data_type):
    '''Get PDCA/PDSA data from methodology_data table'''
    query = '''
        SELECT data_json FROM methodology_data
        WHERE project_id = %s AND methodology = %s 
        AND phase = %s AND data_type = %s
        ORDER BY updated_at DESC LIMIT 1
    '''
    result = self.execute_query(query, (project_id, methodology, phase, data_type))
    if result and not result.empty:
        import json
        return json.loads(result.iloc[0]['data_json'])
    return None

def save_pdca_data(self, project_id, methodology, phase, data_type, data):
    '''Save PDCA/PDSA data to methodology_data table'''
    import json
    query = '''
        INSERT INTO methodology_data 
        (project_id, methodology, phase, data_type, data_json, updated_at)
        VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (project_id, methodology, phase, data_type) 
        DO UPDATE SET 
            data_json = EXCLUDED.data_json, 
            updated_at = CURRENT_TIMESTAMP
    '''
    return self.execute_update(
        query, 
        (project_id, methodology, phase, data_type, json.dumps(data))
    )

def get_pdca_actions(self, project_id, methodology, phase):
    '''Get actions for PDCA/PDSA phase'''
    query = '''
        SELECT * FROM methodology_actions
        WHERE project_id = %s AND methodology = %s AND phase = %s
        ORDER BY start_date
    '''
    return self.execute_query(query, (project_id, methodology, phase))

def add_pdca_action(self, project_id, methodology, phase, action_data):
    '''Add action to methodology_actions table'''
    query = '''
        INSERT INTO methodology_actions 
        (project_id, methodology, phase, action_name, responsible, 
         start_date, end_date, description, resources, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    '''
    params = (
        project_id, methodology, phase,
        action_data['action_name'], action_data['responsible'],
        action_data['start_date'], action_data['end_date'],
        action_data.get('description'), action_data.get('resources'),
        action_data.get('status', 'Planned')
    )
    result = self.execute_query(query, params)
    return result.iloc[0]['id'] if result is not None and not result.empty else None

def update_pdca_action_status(self, action_id, new_status):
    '''Update action status'''
    query = '''
        UPDATE methodology_actions 
        SET status = %s 
        WHERE id = %s
    '''
    return self.execute_update(query, (new_status, action_id))

def update_pdca_action_notes(self, action_id, notes):
    '''Update action notes'''
    query = '''
        UPDATE methodology_actions 
        SET notes = %s 
        WHERE id = %s
    '''
    return self.execute_update(query, (notes, action_id))

def get_pdca_metrics(self, project_id, methodology, phase):
    '''Get metrics for phase'''
    query = '''
        SELECT * FROM methodology_metrics
        WHERE project_id = %s AND methodology = %s AND phase = %s
        ORDER BY created_at
    '''
    return self.execute_query(query, (project_id, methodology, phase))

def add_pdca_metric(self, project_id, methodology, phase, metric_data):
    '''Add metric'''
    query = '''
        INSERT INTO methodology_metrics 
        (project_id, methodology, phase, metric_name, baseline, 
         target, unit, measurement_method, frequency)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    '''
    params = (
        project_id, methodology, phase,
        metric_data['metric_name'], metric_data['baseline'],
        metric_data['target'], metric_data['unit'],
        metric_data['measurement_method'], metric_data['frequency']
    )
    result = self.execute_query(query, params)
    return result.iloc[0]['id'] if result is not None and not result.empty else None

def get_pdca_measurements(self, project_id, methodology, phase):
    '''Get measurements data'''
    query = '''
        SELECT * FROM methodology_measurements
        WHERE project_id = %s AND methodology = %s AND phase = %s
        ORDER BY measurement_date DESC
    '''
    return self.execute_query(query, (project_id, methodology, phase))

def add_pdca_measurement(self, project_id, methodology, phase, measurement_data):
    '''Add measurement'''
    query = '''
        INSERT INTO methodology_measurements 
        (project_id, methodology, phase, metric_name, 
         measured_value, measurement_date, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    '''
    params = (
        project_id, methodology, phase,
        measurement_data['metric_name'], measurement_data['measured_value'],
        measurement_data['measurement_date'], measurement_data.get('notes')
    )
    result = self.execute_query(query, params)
    return result.iloc[0]['id'] if result is not None and not result.empty else None

def get_pdca_issues(self, project_id, methodology, phase):
    '''Get issues log'''
    query = '''
        SELECT * FROM methodology_issues
        WHERE project_id = %s AND methodology = %s AND phase = %s
        ORDER BY reported_date DESC
    '''
    return self.execute_query(query, (project_id, methodology, phase))

def add_pdca_issue(self, project_id, methodology, phase, issue_data):
    '''Add issue to log'''
    query = '''
        INSERT INTO methodology_issues 
        (project_id, methodology, phase, issue_title, severity, 
         description, action_taken, status, reported_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    '''
    params = (
        project_id, methodology, phase,
        issue_data['issue_title'], issue_data['severity'],
        issue_data['description'], issue_data.get('action_taken'),
        issue_data.get('status', 'Open'), issue_data['reported_date']
    )
    result = self.execute_query(query, params)
    return result.iloc[0]['id'] if result is not None and not result.empty else None

def update_pdca_issue_status(self, issue_id, new_status):
    '''Update issue status'''
    query = '''
        UPDATE methodology_issues 
        SET status = %s 
        WHERE id = %s
    '''
    return self.execute_update(query, (new_status, issue_id))

def get_pdca_lessons(self, project_id, methodology, phase):
    '''Get lessons learned'''
    query = '''
        SELECT * FROM methodology_lessons
        WHERE project_id = %s AND methodology = %s AND phase = %s
        ORDER BY created_at DESC
    '''
    return self.execute_query(query, (project_id, methodology, phase))

def add_pdca_lesson(self, project_id, methodology, phase, lesson_data):
    '''Add lesson learned'''
    query = '''
        INSERT INTO methodology_lessons 
        (project_id, methodology, phase, lesson_title, 
         category, description, recommendation)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    '''
    params = (
        project_id, methodology, phase,
        lesson_data['lesson_title'], lesson_data['category'],
        lesson_data['description'], lesson_data.get('recommendation')
    )
    result = self.execute_query(query, params)
    return result.iloc[0]['id'] if result is not None and not result.empty else None

def get_pdca_rollout_plan(self, project_id, methodology):
    '''Get rollout plan'''
    query = '''
        SELECT * FROM methodology_rollout
        WHERE project_id = %s AND methodology = %s
        ORDER BY created_at
    '''
    return self.execute_query(query, (project_id, methodology))

def add_pdca_rollout(self, project_id, methodology, rollout_data):
    '''Add rollout item'''
    query = '''
        INSERT INTO methodology_rollout 
        (project_id, methodology, department, timeline, 
         responsible, resources, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    '''
    params = (
        project_id, methodology,
        rollout_data['department'], rollout_data['timeline'],
        rollout_data['responsible'], rollout_data.get('resources'),
        rollout_data.get('status', 'Planned')
    )
    result = self.execute_query(query, params)
    return result.iloc[0]['id'] if result is not None and not result.empty else None

def mark_pdca_cycle_complete(self, project_id, methodology):
    '''Mark PDCA/PDSA cycle as complete'''
    query = '''
        UPDATE projects 
        SET status = 'Hoàn thành',
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
    '''
    return self.execute_update(query, (project_id,))

# END OF PDCA/PDSA METHODS
"""

# ==================== END OF CODE SNIPPET ====================
# 
# Tổng kết:
# - Thêm 1 import
# - Thay 1 function  
# - (Optional) Thêm database methods nếu chưa có
# 
# Đơn giản vậy thôi! 🎉
# ========================================

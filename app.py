"""
APP.PY UPDATES - COLLABORATION TAB INTEGRATION
==============================================

Follow these steps to add Collaboration tab to your app.py
"""

# ==================== STEP 1: ADD IMPORT (Top of file) ====================

# Find the imports section at the top of app.py (around line 10-20)
# Add this import AFTER the existing imports:

from collaboration import render_collaboration_tab, initialize_collaboration


# ==================== STEP 2: INITIALIZE COLLABORATION (In main()) ====================

# Find the main() function, locate where db is initialized
# Add this code RIGHT AFTER: db = ProjectDatabase()

# Initialize collaboration features
if 'collaboration_initialized' not in st.session_state:
    collaboration_components = initialize_collaboration(db, enable_scheduler=False)
    st.session_state['collaboration_initialized'] = True
    st.session_state['collaboration_components'] = collaboration_components


# ==================== STEP 3: ADD TAB (In render_manage_projects) ====================

# Find the render_manage_projects() function
# Look for where tabs are defined, it should look like:
#
# tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([...])
#
# CHANGE IT TO ADD 7th TAB:

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📄 Thông tin",
    "👥 Thành viên",
    "🤝 Stakeholders",
    "📅 Kế hoạch (Gantt)",
    "🔄 DMAIC Tracking",
    "💬 Cộng tác",  # ← NEW TAB
    "✍️ Ký tên",
    "📤 Xuất báo cáo"
])


# ==================== STEP 4: ADD TAB HANDLER ====================

# After the existing tab handlers (tab1, tab2, tab3, etc.)
# Add this NEW handler for tab6 (before the original tab6 becomes tab7):

# Find where the tabs are handled, should be:
# with tab1:
#     render_project_info(...)
# with tab2:
#     render_team_members(...)
# ...
# with tab5:
#     render_dmaic_tracking(...)
#
# ADD THIS NEW ONE:

with tab6:
    # Get current user (adjust this based on your user management)
    current_user = st.session_state.get('user_name', 'Current User')
    
    # Render collaboration tab
    render_collaboration_tab(
        project_id=project_id,
        project=project,
        database=db,
        current_user=current_user
    )

# THEN the existing tab6 becomes tab7:
with tab7:
    render_signoffs(project_id)

# And tab7 becomes tab8:
with tab8:
    render_export_report(project_id, project)


# ==================== COMPLETE CODE BLOCK ====================

"""
Here's the complete integration in context:

def render_manage_projects():
    st.header("📝 Quản lý Dự án")
    
    projects_df = db.get_projects_df()
    
    if projects_df.empty:
        st.info("Chưa có dự án nào.")
        return
    
    project_list = projects_df['project_code'].tolist()
    selected_project = st.selectbox("Chọn dự án:", project_list)
    
    if selected_project:
        project_id = projects_df[projects_df['project_code'] == selected_project]['id'].iloc[0]
        project = db.get_project(project_id)
        
        # CREATE 8 TABS (was 7, now 8)
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📄 Thông tin",
            "👥 Thành viên",
            "🤝 Stakeholders",
            "📅 Kế hoạch (Gantt)",
            "🔄 DMAIC Tracking",
            "💬 Cộng tác",  # ← NEW!
            "✍️ Ký tên",
            "📤 Xuất báo cáo"
        ])
        
        with tab1:
            render_project_info(project_id, project)
        
        with tab2:
            render_team_members(project_id)
        
        with tab3:
            render_stakeholders(project_id)
        
        with tab4:
            render_gantt_plan(project_id)
        
        with tab5:
            render_dmaic_tracking(project_id, project)
        
        with tab6:  # ← NEW COLLABORATION TAB
            current_user = st.session_state.get('user_name', 'Current User')
            render_collaboration_tab(
                project_id=project_id,
                project=project,
                database=db,
                current_user=current_user
            )
        
        with tab7:  # Was tab6
            render_signoffs(project_id)
        
        with tab8:  # Was tab7
            render_export_report(project_id, project)
"""


# ==================== SUMMARY OF CHANGES ====================

"""
SUMMARY:
========

Changes to make in app.py:

1. ADD IMPORT (top of file):
   from collaboration import render_collaboration_tab, initialize_collaboration

2. ADD INITIALIZATION (in main(), after db creation):
   if 'collaboration_initialized' not in st.session_state:
       collaboration_components = initialize_collaboration(db, enable_scheduler=False)
       st.session_state['collaboration_initialized'] = True

3. UPDATE TABS (in render_manage_projects):
   - Change from 7 tabs to 8 tabs
   - Add "💬 Cộng tác" as 6th tab
   - Previous tabs 6-7 become 7-8

4. ADD TAB HANDLER (in render_manage_projects):
   - Add new "with tab6:" block
   - Call render_collaboration_tab()
   - Update existing tab6→tab7, tab7→tab8

Total changes: 4 locations, ~15 lines of code
Time: 10 minutes
"""


# ==================== QUICK CHECKLIST ====================

"""
CHECKLIST:
==========

Before making changes:
[ ] Backup current app.py
[ ] Make sure database.py is updated first
[ ] Make sure all 5 collaboration modules are uploaded

After making changes:
[ ] No syntax errors (check with Python)
[ ] Imports work correctly
[ ] App runs without crashing
[ ] Collaboration tab appears
[ ] Features work correctly

TESTING:
========

After updating app.py, test:

1. Run app locally or deploy to Streamlit Cloud
2. Navigate to a project
3. Check if "💬 Cộng tác" tab appears
4. Click on it - should show 4 sub-tabs:
   - 💭 Bình luận
   - 📋 Nhật ký Hoạt động
   - 🗓️ Biên bản Họp
   - 📧 Thông báo
5. Try posting a comment
6. Check activity log

If everything works: ✅ SUCCESS!
"""

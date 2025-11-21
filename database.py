"""
DATABASE.PY UPDATES - COLLABORATION SUPPORT
============================================

Thêm các methods này vào class ProjectDatabase trong file database.py
Tìm vị trí cuối cùng của class (trước dòng cuối cùng) và paste các methods này vào.
"""

# ==================== ACTIVITY LOG METHODS ====================

def add_activity_log(self, activity_data):
    """
    Add activity to log
    
    Args:
        activity_data: Dict with activity details
    
    Returns:
        bool: Success status
    """
    try:
        query = """
        INSERT INTO activity_log 
        (project_id, user_name, action_type, action_details, created_at)
        VALUES (:project_id, :user_name, :action_type, :action_details, :created_at)
        """
        self.execute_query(query, activity_data)
        return True
    except Exception as e:
        print(f"Error adding activity: {e}")
        return False

def get_activities(self, project_id, limit=50):
    """
    Get activity log for a project
    
    Args:
        project_id: Project ID
        limit: Maximum number of activities to return
    
    Returns:
        List of activity dicts
    """
    try:
        query = f"""
        SELECT * FROM activity_log 
        WHERE project_id = :project_id 
        ORDER BY created_at DESC 
        LIMIT {limit}
        """
        result = self.execute_query(query, {'project_id': project_id})
        return result.mappings().all() if result else []
    except Exception as e:
        print(f"Error getting activities: {e}")
        return []


# ==================== COMMENTS METHODS ====================

def add_comment(self, comment_data):
    """
    Add comment to project
    
    Args:
        comment_data: Dict with comment details
    
    Returns:
        bool: Success status
    """
    try:
        query = """
        INSERT INTO project_comments 
        (project_id, user_name, user_email, comment_text, mentions, created_at)
        VALUES (:project_id, :user_name, :user_email, :comment_text, :mentions, :created_at)
        """
        self.execute_query(query, comment_data)
        return True
    except Exception as e:
        print(f"Error adding comment: {e}")
        return False

def get_comments(self, project_id):
    """
    Get all comments for a project
    
    Args:
        project_id: Project ID
    
    Returns:
        List of comment dicts
    """
    try:
        query = """
        SELECT * FROM project_comments 
        WHERE project_id = :project_id 
        ORDER BY created_at DESC
        """
        result = self.execute_query(query, {'project_id': project_id})
        return result.mappings().all() if result else []
    except Exception as e:
        print(f"Error getting comments: {e}")
        return []

def get_comment_by_id(self, comment_id):
    """
    Get a specific comment by ID
    
    Args:
        comment_id: Comment ID
    
    Returns:
        Comment dict or None
    """
    try:
        query = "SELECT * FROM project_comments WHERE id = :id"
        result = self.execute_query(query, {'id': comment_id})
        return result.mappings().first() if result else None
    except Exception as e:
        print(f"Error getting comment: {e}")
        return None

def delete_comment(self, comment_id):
    """
    Delete a comment
    
    Args:
        comment_id: Comment ID
    
    Returns:
        bool: Success status
    """
    try:
        query = "DELETE FROM project_comments WHERE id = :id"
        self.execute_query(query, {'id': comment_id})
        return True
    except Exception as e:
        print(f"Error deleting comment: {e}")
        return False


# ==================== MEETING MINUTES METHODS ====================

def add_meeting_minutes(self, meeting_data):
    """
    Add meeting minutes
    
    Args:
        meeting_data: Dict with meeting details
    
    Returns:
        bool: Success status
    """
    try:
        query = """
        INSERT INTO meeting_minutes 
        (project_id, meeting_title, meeting_date, meeting_time, location, 
         duration_minutes, attendees, agenda, notes, action_items, decisions, 
         created_by, created_at)
        VALUES (:project_id, :meeting_title, :meeting_date, :meeting_time, :location,
                :duration_minutes, :attendees, :agenda, :notes, :action_items, 
                :decisions, :created_by, :created_at)
        """
        self.execute_query(query, meeting_data)
        return True
    except Exception as e:
        print(f"Error adding meeting: {e}")
        return False

def get_meeting_minutes(self, project_id):
    """
    Get all meeting minutes for a project
    
    Args:
        project_id: Project ID
    
    Returns:
        List of meeting dicts
    """
    try:
        query = """
        SELECT * FROM meeting_minutes 
        WHERE project_id = :project_id 
        ORDER BY meeting_date DESC
        """
        result = self.execute_query(query, {'project_id': project_id})
        return result.mappings().all() if result else []
    except Exception as e:
        print(f"Error getting meetings: {e}")
        return []

def get_meeting_by_id(self, meeting_id):
    """
    Get a specific meeting by ID
    
    Args:
        meeting_id: Meeting ID
    
    Returns:
        Meeting dict or None
    """
    try:
        query = "SELECT * FROM meeting_minutes WHERE id = :id"
        result = self.execute_query(query, {'id': meeting_id})
        return result.mappings().first() if result else None
    except Exception as e:
        print(f"Error getting meeting: {e}")
        return None

def update_meeting_minutes(self, meeting_id, meeting_data):
    """
    Update meeting minutes
    
    Args:
        meeting_id: Meeting ID
        meeting_data: Dict with updated meeting details
    
    Returns:
        bool: Success status
    """
    try:
        # Build dynamic update query
        fields = []
        for key in meeting_data.keys():
            fields.append(f"{key} = :{key}")
        
        query = f"""
        UPDATE meeting_minutes 
        SET {', '.join(fields)}
        WHERE id = :meeting_id
        """
        
        meeting_data['meeting_id'] = meeting_id
        self.execute_query(query, meeting_data)
        return True
    except Exception as e:
        print(f"Error updating meeting: {e}")
        return False

def delete_meeting_minutes(self, meeting_id):
    """
    Delete meeting minutes
    
    Args:
        meeting_id: Meeting ID
    
    Returns:
        bool: Success status
    """
    try:
        query = "DELETE FROM meeting_minutes WHERE id = :id"
        self.execute_query(query, {'id': meeting_id})
        return True
    except Exception as e:
        print(f"Error deleting meeting: {e}")
        return False


# ==================== HELPER METHODS ====================

def get_all_projects(self):
    """
    Get all projects (for notification scheduler)
    
    Returns:
        List of all project dicts
    """
    try:
        query = "SELECT * FROM projects ORDER BY created_at DESC"
        result = self.execute_query(query)
        return result.mappings().all() if result else []
    except Exception as e:
        print(f"Error getting all projects: {e}")
        return []


# ==================== END OF METHODS ====================

"""
INSTRUCTIONS:
=============

1. Open your database.py file
2. Find the ProjectDatabase class
3. Scroll to the bottom of the class (before the last line)
4. Copy ALL methods above (from add_activity_log to get_all_projects)
5. Paste them into the class
6. Save the file

LOCATION:
=========
Paste these methods right before the end of the ProjectDatabase class.
For example, if your class ends with:

    class ProjectDatabase:
        def __init__(self):
            ...
        
        def get_projects(self):
            ...
        
        # ← PASTE HERE (before the class ends)

Total: 11 new methods
Lines: ~200 lines of code
Time: 5 minutes to copy/paste

TESTING:
========
After adding, test if it works:

from database import ProjectDatabase

db = ProjectDatabase()
# Should not error
print("✅ Database methods added successfully!")
"""

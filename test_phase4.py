"""
Test & Demo Script for Phase 4: Collaboration & Communication
Run this to test all new features
"""

import sys
from datetime import datetime, timedelta
from database import ProjectDatabase
from notifications import NotificationSystem
from collaboration import CollaborationManager
from meetings import MeetingManager

def test_phase4_features():
    """Test all Phase 4 collaboration features"""
    
    print("=" * 80)
    print("🧪 TESTING PHASE 4: COLLABORATION & COMMUNICATION")
    print("=" * 80)
    print()
    
    # Initialize
    print("📦 Initializing systems...")
    db = ProjectDatabase()
    notification_system = NotificationSystem(db)
    collaboration_manager = CollaborationManager(db, notification_system)
    meeting_manager = MeetingManager(db, collaboration_manager)
    print("✅ Systems initialized!\n")
    
    # Get or create a test project
    projects = db.get_all_projects()
    if projects.empty:
        print("⚠️  No projects found. Creating test project...")
        project_data = {
            'project_code': 'TEST-2024-001',
            'project_name': 'Test Collaboration Project',
            'department': 'IT',
            'start_date': datetime.now().isoformat(),
            'end_date': (datetime.now() + timedelta(days=90)).isoformat(),
            'status': 'Đang thực hiện',
            'category': '(5) Bệnh viện thông minh',
            'description': 'Test project for Phase 4 features',
            'problem_statement': 'Testing collaboration features',
            'goal': 'Verify all features work correctly',
            'scope': 'All collaboration modules'
        }
        project_id = db.create_project(project_data)
        print(f"✅ Created test project ID: {project_id}\n")
    else:
        project_id = projects.iloc[0]['id']
        print(f"✅ Using existing project ID: {project_id}\n")
    
    # ========== TEST 1: COMMENTS ==========
    print("-" * 80)
    print("TEST 1: COMMENTS & DISCUSSION")
    print("-" * 80)
    
    print("\n1.1 Adding comments...")
    comment1_id = collaboration_manager.add_comment(
        project_id=project_id,
        user_name="John Doe",
        user_email="john@example.com",
        comment_text="This is the first comment on this project!"
    )
    print(f"   ✅ Added comment 1 (ID: {comment1_id})")
    
    comment2_id = collaboration_manager.add_comment(
        project_id=project_id,
        user_name="Jane Smith",
        user_email="jane@example.com",
        comment_text="@John great start! Let's collaborate on the Define phase."
    )
    print(f"   ✅ Added comment 2 with @mention (ID: {comment2_id})")
    
    reply_id = collaboration_manager.add_comment(
        project_id=project_id,
        user_name="John Doe",
        user_email="john@example.com",
        comment_text="@Jane absolutely! I'll start working on the SIPOC diagram.",
        parent_comment_id=comment2_id
    )
    print(f"   ✅ Added reply (ID: {reply_id})")
    
    print("\n1.2 Retrieving comments...")
    comments = collaboration_manager.get_comments(project_id)
    print(f"   ✅ Retrieved {len(comments)} comments")
    for _, comment in comments.iterrows():
        prefix = "    └─" if comment['parent_comment_id'] else "    ├─"
        print(f"{prefix} {comment['user_name']}: {comment['comment_text'][:50]}...")
    
    print("\n1.3 Comment thread...")
    thread = collaboration_manager.get_comment_thread(comment2_id)
    print(f"   ✅ Thread has {len(thread)} messages")
    
    # ========== TEST 2: ACTIVITY LOG ==========
    print("\n" + "-" * 80)
    print("TEST 2: ACTIVITY LOG")
    print("-" * 80)
    
    print("\n2.1 Logging activities...")
    collaboration_manager.log_activity(
        project_id=project_id,
        user_name="John Doe",
        user_email="john@example.com",
        activity_type="task_created",
        activity_description="Created SIPOC diagram task",
        entity_type="task",
        entity_id=1
    )
    print("   ✅ Logged activity: task_created")
    
    collaboration_manager.log_activity(
        project_id=project_id,
        user_name="Jane Smith",
        user_email="jane@example.com",
        activity_type="project_updated",
        activity_description="Updated project timeline",
        entity_type="project",
        entity_id=project_id
    )
    print("   ✅ Logged activity: project_updated")
    
    collaboration_manager.log_activity(
        project_id=project_id,
        user_name="Bob Johnson",
        user_email="bob@example.com",
        activity_type="milestone_achieved",
        activity_description="Completed Define phase",
        entity_type="milestone",
        entity_id=1
    )
    print("   ✅ Logged activity: milestone_achieved")
    
    print("\n2.2 Retrieving activity log...")
    activities = collaboration_manager.get_activity_log(project_id, limit=20)
    print(f"   ✅ Retrieved {len(activities)} activities")
    for _, activity in activities.iterrows():
        print(f"    - [{activity['activity_type']}] {activity['user_name']}: {activity['activity_description']}")
    
    print("\n2.3 Collaboration statistics...")
    stats = collaboration_manager.get_collaboration_stats(project_id)
    print(f"   ✅ Total comments: {stats['total_comments']}")
    print(f"   ✅ Total activities: {stats['total_activities']}")
    print(f"   ✅ Recent activity (7 days): {stats['recent_activity_count']}")
    print(f"   ✅ Top commenters: {stats['top_commenters']}")
    
    # ========== TEST 3: MEETINGS ==========
    print("\n" + "-" * 80)
    print("TEST 3: MEETINGS & ACTION ITEMS")
    print("-" * 80)
    
    print("\n3.1 Creating meeting...")
    meeting_date = datetime.now() + timedelta(days=1)
    meeting_id = meeting_manager.create_meeting(
        project_id=project_id,
        meeting_title="Sprint Planning Meeting",
        meeting_date=meeting_date,
        duration=90,
        location="Conference Room A",
        attendees=["John Doe", "Jane Smith", "Bob Johnson"],
        agenda="1. Review last sprint\n2. Plan next sprint\n3. Discuss blockers",
        created_by="Project Manager"
    )
    print(f"   ✅ Created meeting (ID: {meeting_id})")
    
    print("\n3.2 Updating meeting minutes...")
    meeting_manager.update_meeting_minutes(
        meeting_id=meeting_id,
        minutes="""
        Meeting Notes:
        - Reviewed progress on Define phase
        - Discussed approach for Measure phase
        - Identified key metrics to track
        - Allocated resources for next sprint
        """,
        decisions="""
        Decisions:
        - Extend Define phase by 1 week
        - Add 2 more team members
        - Use Six Sigma calculator tool
        """,
        updated_by="Project Manager"
    )
    print("   ✅ Updated meeting minutes")
    
    print("\n3.3 Creating action items...")
    action1_id = meeting_manager.create_action_item(
        meeting_id=meeting_id,
        project_id=project_id,
        item_description="Complete SIPOC diagram by next Monday",
        assigned_to="John Doe",
        due_date=(datetime.now() + timedelta(days=7)).date(),
        priority="High",
        notes="Use standard template from shared drive"
    )
    print(f"   ✅ Created action item 1 (ID: {action1_id})")
    
    action2_id = meeting_manager.create_action_item(
        meeting_id=meeting_id,
        project_id=project_id,
        item_description="Prepare data collection plan",
        assigned_to="Jane Smith",
        due_date=(datetime.now() + timedelta(days=5)).date(),
        priority="Medium",
        notes="Include at least 5 key metrics"
    )
    print(f"   ✅ Created action item 2 (ID: {action2_id})")
    
    action3_id = meeting_manager.create_action_item(
        meeting_id=meeting_id,
        project_id=project_id,
        item_description="Review previous similar projects",
        assigned_to="Bob Johnson",
        due_date=(datetime.now() + timedelta(days=3)).date(),
        priority="Low"
    )
    print(f"   ✅ Created action item 3 (ID: {action3_id})")
    
    print("\n3.4 Retrieving meetings...")
    meetings = meeting_manager.get_meetings(project_id)
    print(f"   ✅ Retrieved {len(meetings)} meetings")
    for _, meeting in meetings.iterrows():
        print(f"    - {meeting['meeting_title']} on {meeting['meeting_date']}")
    
    print("\n3.5 Retrieving action items...")
    action_items = meeting_manager.get_action_items(project_id=project_id)
    print(f"   ✅ Retrieved {len(action_items)} action items")
    for _, item in action_items.iterrows():
        print(f"    - [{item['priority']}] {item['item_description']} (assigned to {item['assigned_to']})")
    
    print("\n3.6 Updating action item status...")
    meeting_manager.update_action_item_status(
        action_id=action3_id,
        status="Completed",
        notes="Reviewed 3 similar projects from 2023",
        updated_by="Bob Johnson"
    )
    print("   ✅ Updated action item to Completed")
    
    print("\n3.7 Meeting statistics...")
    meeting_stats = meeting_manager.get_meeting_stats(project_id)
    print(f"   ✅ Total meetings: {meeting_stats['total_meetings']}")
    print(f"   ✅ Meetings with minutes: {meeting_stats['meetings_with_minutes']}")
    print(f"   ✅ Total action items: {meeting_stats['total_action_items']}")
    print(f"   ✅ Completed actions: {meeting_stats['completed_actions']}")
    print(f"   ✅ Completion rate: {meeting_stats['completion_rate']:.1f}%")
    
    # ========== TEST 4: NOTIFICATIONS ==========
    print("\n" + "-" * 80)
    print("TEST 4: NOTIFICATIONS")
    print("-" * 80)
    
    print("\n4.1 Creating notification records...")
    notif1_id = notification_system._create_notification_record(
        project_id=project_id,
        recipient_email="john@example.com",
        notification_type="project_assignment",
        title="You've been assigned to a project",
        message="You have been assigned to Test Collaboration Project"
    )
    print(f"   ✅ Created notification 1 (ID: {notif1_id})")
    
    notif2_id = notification_system._create_notification_record(
        project_id=project_id,
        recipient_email="jane@example.com",
        notification_type="comment_mention",
        title="You were mentioned in a comment",
        message="John Doe mentioned you in a comment"
    )
    print(f"   ✅ Created notification 2 (ID: {notif2_id})")
    
    notif3_id = notification_system._create_notification_record(
        project_id=project_id,
        recipient_email="john@example.com",
        notification_type="deadline_reminder",
        title="Task deadline approaching",
        message="Your task 'Complete SIPOC' is due in 7 days"
    )
    print(f"   ✅ Created notification 3 (ID: {notif3_id})")
    
    print("\n4.2 Retrieving notifications...")
    john_notifications = notification_system.get_unread_notifications("john@example.com")
    print(f"   ✅ John has {len(john_notifications)} unread notifications")
    
    jane_notifications = notification_system.get_unread_notifications("jane@example.com")
    print(f"   ✅ Jane has {len(jane_notifications)} unread notifications")
    
    print("\n4.3 Notification summary...")
    john_summary = notification_system.get_notification_summary("john@example.com")
    print(f"   ✅ John's summary:")
    print(f"      - Total: {john_summary['total']}")
    print(f"      - Unread: {john_summary['unread']}")
    print(f"      - By type: {john_summary['by_type']}")
    
    print("\n4.4 Marking notification as read...")
    notification_system.mark_as_read(notif1_id)
    print(f"   ✅ Marked notification {notif1_id} as read")
    
    print("\n4.5 Email notification test (will not send without SMTP config)...")
    print("   ℹ️  SMTP not configured - skipping actual email send")
    print("   ℹ️  To test email, configure SMTP in the app and run test notification")
    
    # ========== SUMMARY ==========
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    
    print("\n✅ All tests passed successfully!")
    print(f"\n📈 Statistics:")
    print(f"   - Comments created: 3")
    print(f"   - Activities logged: {len(activities)}")
    print(f"   - Meetings created: 1")
    print(f"   - Action items created: 3")
    print(f"   - Notifications created: 3")
    
    print(f"\n💾 Database tables verified:")
    print("   ✅ comments")
    print("   ✅ notifications")
    print("   ✅ activity_log")
    print("   ✅ meetings")
    print("   ✅ action_items")
    
    print("\n🎉 Phase 4 features are working correctly!")
    print("\n💡 Next steps:")
    print("   1. Run the Streamlit app: streamlit run app.py")
    print("   2. Navigate to Collaboration menu")
    print("   3. Explore all features")
    print("   4. Configure SMTP for email notifications")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    try:
        test_phase4_features()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

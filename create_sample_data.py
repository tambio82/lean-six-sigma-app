"""
Script tạo dữ liệu mẫu cho demo hệ thống Lean Six Sigma
Chạy: python create_sample_data.py
"""

from database import ProjectDatabase
from datetime import datetime, timedelta
import random

def create_sample_data():
    db = ProjectDatabase()
    
    print("🔄 Đang tạo dữ liệu mẫu...")
    
    # 1. Tạo Phòng/Ban
    departments = [
        ("Khoa Nội Tổng hợp", "Khám và điều trị các bệnh nội khoa"),
        ("Khoa Ngoại Tổng hợp", "Khám và phẫu thuật ngoại khoa"),
        ("Khoa Sản", "Chăm sóc sức khỏe bà mẹ và trẻ em"),
        ("Khoa Cấp cứu", "Tiếp nhận và xử lý cấp cứu"),
        ("Phòng Kế hoạch Tổng hợp", "Quản lý và điều phối chung"),
        ("Phòng Điều dưỡng", "Quản lý và đào tạo điều dưỡng"),
        ("Khoa Xét nghiệm", "Xét nghiệm chẩn đoán"),
        ("Khoa Chẩn đoán Hình ảnh", "X-quang, CT, MRI...")
    ]
    
    print("  → Tạo Phòng/Ban...")
    for name, desc in departments:
        db.add_department(name, desc)
    
    # 2. Tạo các dự án mẫu
    categories = [
        "(1) An toàn người bệnh",
        "(2) Hướng đến Hài lòng cho người bệnh",
        "(3) Hướng đến hài lòng cho nhân viên",
        "(4) Nâng cao chất lượng chuyên môn",
        "(5) Bệnh viện thông minh"
    ]
    
    statuses = ["Lên kế hoạch", "Đang thực hiện", "Hoàn thành"]
    
    projects_data = [
        {
            "project_code": "LSS-2024-001",
            "project_name": "Giảm thời gian chờ khám tại Khoa Nội",
            "department": "Khoa Nội Tổng hợp",
            "category": "(2) Hướng đến Hài lòng cho người bệnh",
            "status": "Đang thực hiện",
            "description": "Tối ưu hóa quy trình khám bệnh để giảm thời gian chờ",
            "problem_statement": "Thời gian chờ khám trung bình hiện tại là 45 phút, gây bất tiện cho người bệnh",
            "goal": "Giảm thời gian chờ xuống còn 20 phút trong vòng 3 tháng",
            "scope": "Áp dụng cho tất cả bệnh nhân khám ngoại trú tại Khoa Nội",
            "budget": 50000000,
            "actual_cost": 15000000
        },
        {
            "project_code": "LSS-2024-002",
            "project_name": "Cải thiện quy trình vệ sinh tay",
            "department": "Phòng Điều dưỡng",
            "category": "(1) An toàn người bệnh",
            "status": "Hoàn thành",
            "description": "Nâng cao tuân thủ vệ sinh tay của nhân viên y tế",
            "problem_statement": "Tỷ lệ tuân thủ vệ sinh tay chỉ đạt 65%, thấp hơn tiêu chuẩn WHO",
            "goal": "Đạt tỷ lệ tuân thủ 95% trong 6 tháng",
            "scope": "Áp dụng toàn bộ nhân viên y tế tại bệnh viện",
            "budget": 30000000,
            "actual_cost": 28000000
        },
        {
            "project_code": "LSS-2024-003",
            "project_name": "Triển khai Hệ thống HIS mới",
            "department": "Phòng Kế hoạch Tổng hợp",
            "category": "(5) Bệnh viện thông minh",
            "status": "Đang thực hiện",
            "description": "Nâng cấp hệ thống thông tin bệnh viện",
            "problem_statement": "Hệ thống hiện tại lỗi thời, không tích hợp tốt",
            "goal": "Triển khai thành công HIS mới trong 12 tháng",
            "scope": "Toàn bộ bệnh viện",
            "budget": 500000000,
            "actual_cost": 200000000
        },
        {
            "project_code": "LSS-2024-004",
            "project_name": "Tối ưu hóa quy trình xét nghiệm",
            "department": "Khoa Xét nghiệm",
            "category": "(4) Nâng cao chất lượng chuyên môn",
            "status": "Lên kế hoạch",
            "description": "Giảm thời gian trả kết quả xét nghiệm",
            "problem_statement": "Thời gian trả kết quả trung bình 4 giờ, chậm hơn so với yêu cầu",
            "goal": "Giảm thời gian xuống 2 giờ",
            "scope": "Các xét nghiệm thường quy",
            "budget": 80000000,
            "actual_cost": 0
        },
        {
            "project_code": "LSS-2024-005",
            "project_name": "Cải thiện môi trường làm việc",
            "department": "Phòng Kế hoạch Tổng hợp",
            "category": "(3) Hướng đến hài lòng cho nhân viên",
            "status": "Đang thực hiện",
            "description": "Nâng cao sự hài lòng của nhân viên",
            "problem_statement": "Khảo sát cho thấy chỉ 60% nhân viên hài lòng với môi trường làm việc",
            "goal": "Đạt mức hài lòng 85% trong 6 tháng",
            "scope": "Toàn bộ nhân viên",
            "budget": 100000000,
            "actual_cost": 40000000
        }
    ]
    
    print("  → Tạo dự án...")
    project_ids = []
    for i, proj_data in enumerate(projects_data):
        # Tạo ngày tháng
        start_date = datetime.now() - timedelta(days=random.randint(30, 180))
        end_date = start_date + timedelta(days=random.randint(90, 365))
        
        proj_data['start_date'] = start_date.date().isoformat()
        proj_data['end_date'] = end_date.date().isoformat()
        
        project_id = db.add_project(proj_data)
        project_ids.append(project_id)
        print(f"    ✓ Dự án {i+1}: {proj_data['project_name']}")
    
    # 3. Thêm team members
    print("  → Tạo thành viên...")
    members_data = [
        ("Nguyễn Văn A", "Trưởng nhóm", "nva@hospital.com", "0901234567"),
        ("Trần Thị B", "Thành viên", "ttb@hospital.com", "0901234568"),
        ("Lê Văn C", "Thành viên", "lvc@hospital.com", "0901234569"),
        ("Phạm Thị D", "Sponsor", "ptd@hospital.com", "0901234570"),
    ]
    
    for project_id in project_ids[:3]:  # Thêm cho 3 dự án đầu
        for name, role, email, phone in members_data:
            member_data = {
                'project_id': project_id,
                'name': name,
                'role': role,
                'department': random.choice([d[0] for d in departments]),
                'email': email,
                'phone': phone
            }
            db.add_team_member(member_data)
    
    # 4. Thêm stakeholders
    print("  → Tạo stakeholders...")
    stakeholders_data = [
        ("BS. Nguyễn Văn X", "Trưởng khoa", "Cao", "Tích cực"),
        ("ThS. Trần Thị Y", "Phó Giám đốc", "Rất cao", "Rất tích cực"),
        ("CN. Lê Văn Z", "Quản lý điều dưỡng", "Trung bình", "Vừa phải"),
    ]
    
    for project_id in project_ids[:3]:
        for name, role, impact, engagement in stakeholders_data:
            stake_data = {
                'project_id': project_id,
                'name': name,
                'role': role,
                'department': random.choice([d[0] for d in departments]),
                'impact_level': impact,
                'engagement_level': engagement
            }
            db.add_stakeholder(stake_data)
    
    # 5. Thêm tasks (Gantt)
    print("  → Tạo kế hoạch...")
    dmaic_phases = ["Define", "Measure", "Analyze", "Improve", "Control"]
    
    for project_id in project_ids[:3]:
        project = db.get_project(project_id)
        start_date = datetime.fromisoformat(project['start_date'])
        
        for i, phase in enumerate(dmaic_phases):
            phase_start = start_date + timedelta(days=i*30)
            phase_end = phase_start + timedelta(days=29)
            
            tasks = [
                f"Hoàn thành {phase} phase",
                f"Review {phase}",
                f"Document {phase}"
            ]
            
            for j, task_name in enumerate(tasks):
                task_start = phase_start + timedelta(days=j*10)
                task_end = task_start + timedelta(days=9)
                
                task_data = {
                    'project_id': project_id,
                    'phase': phase,
                    'task_name': task_name,
                    'start_date': task_start.date().isoformat(),
                    'end_date': task_end.date().isoformat(),
                    'responsible': random.choice([m[0] for m in members_data]),
                    'status': random.choice(["Đang thực hiện", "Hoàn thành", "Chưa bắt đầu"]),
                    'progress': random.randint(0, 100)
                }
                db.add_task(task_data)
    
    # 6. Thêm signoffs
    print("  → Tạo thông tin ký tên...")
    signoff_roles = [
        "Trưởng nhóm dự án",
        "Trưởng khoa/Phòng",
        "Phó Giám đốc",
        "Giám đốc"
    ]
    
    for project_id in project_ids[:2]:
        for i, role in enumerate(signoff_roles):
            sign_data = {
                'project_id': project_id,
                'role': role,
                'name': random.choice([m[0] for m in members_data]) if i < 2 else "",
                'date': (datetime.now() - timedelta(days=random.randint(1, 30))).date().isoformat() if i < 2 else "",
                'notes': "Đã xem xét và đồng ý" if i < 2 else ""
            }
            db.add_signoff(sign_data)
    
    print("\n✅ Hoàn thành! Đã tạo dữ liệu mẫu:")
    print(f"  • {len(departments)} Phòng/Ban")
    print(f"  • {len(projects_data)} Dự án")
    print(f"  • Thành viên, Stakeholders, Tasks, Signoffs cho các dự án")
    print("\n🚀 Chạy 'streamlit run app.py' để xem kết quả!")

if __name__ == "__main__":
    create_sample_data()

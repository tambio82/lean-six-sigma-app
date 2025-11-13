from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import pandas as pd

def setup_vietnamese_font():
    """
    Thiết lập font hỗ trợ tiếng Việt
    """
    try:
        pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
        return True
    except:
        return False

def create_project_pdf(project_data, team_members, stakeholders, tasks, signoffs, output_path):
    """
    Tạo file PDF báo cáo dự án Lean Six Sigma
    """
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Thiết lập font
    use_vietnamese = setup_vietnamese_font()
    
    # Container cho các elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    if use_vietnamese:
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='DejaVuSans-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2e5c8a'),
            spaceAfter=12,
            fontName='DejaVuSans-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            fontName='DejaVuSans'
        )
    else:
        title_style = styles['Title']
        heading_style = styles['Heading2']
        normal_style = styles['Normal']
    
    # 1. TIÊU ĐỀ
    title = Paragraph(f"BẢNG ĐIỀU LỆ DỰ ÁN<br/>{project_data.get('project_name', 'N/A')}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.5*cm))
    
    # 2. THÔNG TIN CHUNG
    elements.append(Paragraph("1. THÔNG TIN CHUNG", heading_style))
    
    general_info = [
        ["Mã dự án:", project_data.get('project_code', 'N/A')],
        ["Tên dự án:", project_data.get('project_name', 'N/A')],
        ["Phòng/Ban:", project_data.get('department', 'N/A')],
        ["Danh mục:", project_data.get('category', 'N/A')],
        ["Trạng thái:", project_data.get('status', 'N/A')],
        ["Ngày bắt đầu:", project_data.get('start_date', 'N/A')],
        ["Ngày kết thúc:", project_data.get('end_date', 'N/A')],
    ]
    
    general_table = Table(general_info, colWidths=[4*cm, 12*cm])
    general_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'DejaVuSans' if use_vietnamese else 'Helvetica', 9),
        ('FONT', (0, 0), (0, -1), 'DejaVuSans-Bold' if use_vietnamese else 'Helvetica-Bold', 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(general_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Mô tả vấn đề
    if project_data.get('problem_statement'):
        elements.append(Paragraph("Mô tả vấn đề:", heading_style))
        elements.append(Paragraph(project_data.get('problem_statement', ''), normal_style))
        elements.append(Spacer(1, 0.3*cm))
    
    # Mục tiêu
    if project_data.get('goal'):
        elements.append(Paragraph("Mục tiêu:", heading_style))
        elements.append(Paragraph(project_data.get('goal', ''), normal_style))
        elements.append(Spacer(1, 0.3*cm))
    
    # Phạm vi
    if project_data.get('scope'):
        elements.append(Paragraph("Phạm vi dự án:", heading_style))
        elements.append(Paragraph(project_data.get('scope', ''), normal_style))
        elements.append(Spacer(1, 0.5*cm))
    
    # 3. THÀNH VIÊN DỰ ÁN
    elements.append(Paragraph("2. CÁC THÀNH VIÊN TRONG DỰ ÁN", heading_style))
    
    if not team_members.empty:
        team_data = [['STT', 'Họ tên', 'Vai trò', 'Phòng/Ban', 'Email']]
        for idx, member in team_members.iterrows():
            team_data.append([
                str(idx + 1),
                member.get('name', ''),
                member.get('role', ''),
                member.get('department', ''),
                member.get('email', '')
            ])
        
        team_table = Table(team_data, colWidths=[1*cm, 4*cm, 3*cm, 3.5*cm, 4.5*cm])
        team_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'DejaVuSans' if use_vietnamese else 'Helvetica', 8),
            ('FONT', (0, 0), (-1, 0), 'DejaVuSans-Bold' if use_vietnamese else 'Helvetica-Bold', 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(team_table)
    else:
        elements.append(Paragraph("Chưa có thành viên nào.", normal_style))
    
    elements.append(Spacer(1, 0.5*cm))
    
    # 4. STAKEHOLDERS
    elements.append(Paragraph("3. CÁC BÊN LIÊN QUAN", heading_style))
    
    if not stakeholders.empty:
        stake_data = [['STT', 'Họ tên', 'Vai trò', 'Phòng/Ban', 'Mức độ ảnh hưởng']]
        for idx, stake in stakeholders.iterrows():
            stake_data.append([
                str(idx + 1),
                stake.get('name', ''),
                stake.get('role', ''),
                stake.get('department', ''),
                stake.get('impact_level', '')
            ])
        
        stake_table = Table(stake_data, colWidths=[1*cm, 4*cm, 3.5*cm, 3.5*cm, 4*cm])
        stake_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'DejaVuSans' if use_vietnamese else 'Helvetica', 8),
            ('FONT', (0, 0), (-1, 0), 'DejaVuSans-Bold' if use_vietnamese else 'Helvetica-Bold', 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(stake_table)
    else:
        elements.append(Paragraph("Chưa có thông tin bên liên quan.", normal_style))
    
    elements.append(Spacer(1, 0.5*cm))
    
    # 5. NGÂN SÁCH
    elements.append(Paragraph("4. NGÂN SÁCH", heading_style))
    
    budget_info = [
        ["Ngân sách dự kiến:", f"{project_data.get('budget', 0):,.0f} VNĐ"],
        ["Chi phí thực tế:", f"{project_data.get('actual_cost', 0):,.0f} VNĐ"],
    ]
    
    budget_table = Table(budget_info, colWidths=[4*cm, 12*cm])
    budget_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'DejaVuSans' if use_vietnamese else 'Helvetica', 9),
        ('FONT', (0, 0), (0, -1), 'DejaVuSans-Bold' if use_vietnamese else 'Helvetica-Bold', 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(budget_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # 6. KẾ HOẠCH CHI TIẾT
    elements.append(PageBreak())
    elements.append(Paragraph("5. KẾ HOẠCH CHI TIẾT", heading_style))
    
    if not tasks.empty:
        task_data = [['Phase', 'Công việc', 'Bắt đầu', 'Kết thúc', 'Người phụ trách', 'Tiến độ']]
        for _, task in tasks.iterrows():
            task_data.append([
                task.get('phase', ''),
                task.get('task_name', ''),
                task.get('start_date', ''),
                task.get('end_date', ''),
                task.get('responsible', ''),
                f"{task.get('progress', 0)}%"
            ])
        
        task_table = Table(task_data, colWidths=[2*cm, 5*cm, 2*cm, 2*cm, 3*cm, 1.5*cm])
        task_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'DejaVuSans' if use_vietnamese else 'Helvetica', 7),
            ('FONT', (0, 0), (-1, 0), 'DejaVuSans-Bold' if use_vietnamese else 'Helvetica-Bold', 8),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        elements.append(task_table)
    else:
        elements.append(Paragraph("Chưa có kế hoạch chi tiết.", normal_style))
    
    elements.append(Spacer(1, 0.5*cm))
    
    # 7. BẢNG KÝ TÊN
    elements.append(PageBreak())
    elements.append(Paragraph("6. BẢNG KÝ TÊN", heading_style))
    
    if not signoffs.empty:
        sign_data = [['Vai trò', 'Họ tên', 'Ngày ký', 'Chữ ký']]
        for _, sign in signoffs.iterrows():
            sign_data.append([
                sign.get('role', ''),
                sign.get('name', ''),
                sign.get('date', ''),
                ''  # Chỗ để ký tay
            ])
        
        sign_table = Table(sign_data, colWidths=[4*cm, 4*cm, 3*cm, 5*cm])
        sign_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'DejaVuSans' if use_vietnamese else 'Helvetica', 9),
            ('FONT', (0, 0), (-1, 0), 'DejaVuSans-Bold' if use_vietnamese else 'Helvetica-Bold', 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(sign_table)
    else:
        elements.append(Paragraph("Chưa có thông tin ký tên.", normal_style))
    
    # Tạo PDF
    doc.build(elements)
    
    return output_path

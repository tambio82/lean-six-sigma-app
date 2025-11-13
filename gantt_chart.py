import plotly.figure_factory as ff
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

def create_gantt_chart(tasks_df):
    """
    Tạo biểu đồ Gantt từ DataFrame tasks
    """
    if tasks_df.empty:
        return None
    
    # Chuyển đổi định dạng cho Plotly
    gantt_data = []
    
    for _, row in tasks_df.iterrows():
        gantt_data.append(dict(
            Task=row['task_name'],
            Start=row['start_date'],
            Finish=row['end_date'],
            Resource=row.get('phase', 'N/A'),
            Description=f"{row.get('responsible', 'N/A')} - {row.get('progress', 0)}%"
        ))
    
    if not gantt_data:
        return None
    
    # Tạo màu sắc cho các phase khác nhau
    colors = {
        'Define': 'rgb(46, 137, 205)',
        'Measure': 'rgb(114, 44, 121)',
        'Analyze': 'rgb(198, 47, 105)',
        'Improve': 'rgb(58, 149, 136)',
        'Control': 'rgb(107, 127, 135)',
        'N/A': 'rgb(128, 128, 128)'
    }
    
    fig = ff.create_gantt(
        gantt_data,
        colors=colors,
        index_col='Resource',
        show_colorbar=True,
        group_tasks=True,
        showgrid_x=True,
        showgrid_y=True,
        title='Biểu đồ Gantt - Kế hoạch Dự án'
    )
    
    fig.update_layout(
        xaxis_title='Thời gian',
        yaxis_title='Công việc',
        height=max(400, len(gantt_data) * 40),
        font=dict(size=10)
    )
    
    return fig

def create_dmaic_gantt(tasks_df):
    """
    Tạo Gantt chart theo DMAIC phases
    """
    if tasks_df.empty:
        return None
    
    # Định nghĩa các phase DMAIC
    dmaic_phases = ['Define', 'Measure', 'Analyze', 'Improve', 'Control']
    colors = ['#2E89CD', '#722C79', '#C62F69', '#3A9588', '#6B7F87']
    
    fig = go.Figure()
    
    for idx, phase in enumerate(dmaic_phases):
        phase_tasks = tasks_df[tasks_df['phase'] == phase]
        
        for _, task in phase_tasks.iterrows():
            start = pd.to_datetime(task['start_date'])
            end = pd.to_datetime(task['end_date'])
            
            fig.add_trace(go.Scatter(
                x=[start, end],
                y=[task['task_name'], task['task_name']],
                mode='lines',
                line=dict(color=colors[idx], width=20),
                name=phase,
                showlegend=(idx == 0),
                hovertemplate=(
                    f"<b>{task['task_name']}</b><br>"
                    f"Phase: {phase}<br>"
                    f"Người phụ trách: {task.get('responsible', 'N/A')}<br>"
                    f"Tiến độ: {task.get('progress', 0)}%<br>"
                    f"Từ: {start.strftime('%d/%m/%Y')}<br>"
                    f"Đến: {end.strftime('%d/%m/%Y')}<br>"
                    "<extra></extra>"
                )
            ))
    
    fig.update_layout(
        title='Biểu đồ Gantt - DMAIC Phases',
        xaxis_title='Thời gian',
        yaxis_title='Công việc',
        height=max(400, len(tasks_df) * 40),
        showlegend=True,
        hovermode='closest'
    )
    
    return fig

def get_project_progress(tasks_df):
    """
    Tính toán tiến độ tổng thể của dự án
    """
    if tasks_df.empty:
        return 0
    
    total_progress = tasks_df['progress'].mean()
    return round(total_progress, 1)

def get_phase_summary(tasks_df):
    """
    Tóm tắt tiến độ theo từng phase
    """
    if tasks_df.empty:
        return pd.DataFrame()
    
    summary = tasks_df.groupby('phase').agg({
        'task_name': 'count',
        'progress': 'mean'
    }).reset_index()
    
    summary.columns = ['Phase', 'Số công việc', 'Tiến độ trung bình (%)']
    summary['Tiến độ trung bình (%)'] = summary['Tiến độ trung bình (%)'].round(1)
    
    return summary

def check_overdue_tasks(tasks_df):
    """
    Kiểm tra các task quá hạn
    """
    if tasks_df.empty:
        return pd.DataFrame()
    
    today = datetime.now().date()
    
    overdue_tasks = []
    for _, task in tasks_df.iterrows():
        end_date = pd.to_datetime(task['end_date']).date()
        if end_date < today and task.get('progress', 0) < 100:
            overdue_tasks.append({
                'Công việc': task['task_name'],
                'Phase': task['phase'],
                'Hạn chót': end_date.strftime('%d/%m/%Y'),
                'Tiến độ': f"{task.get('progress', 0)}%",
                'Người phụ trách': task.get('responsible', 'N/A')
            })
    
    return pd.DataFrame(overdue_tasks)

def create_timeline_chart(tasks_df):
    """
    Tạo timeline chart đơn giản cho dự án
    """
    if tasks_df.empty:
        return None
    
    fig = go.Figure()
    
    # Sắp xếp tasks theo ngày bắt đầu
    tasks_sorted = tasks_df.sort_values('start_date')
    
    for idx, task in tasks_sorted.iterrows():
        start = pd.to_datetime(task['start_date'])
        end = pd.to_datetime(task['end_date'])
        progress = task.get('progress', 0)
        
        # Tính số ngày
        duration = (end - start).days
        completed_duration = duration * progress / 100
        
        # Vẽ thanh tiến độ
        fig.add_trace(go.Bar(
            y=[task['task_name']],
            x=[completed_duration],
            name='Đã hoàn thành',
            orientation='h',
            marker=dict(color='green'),
            base=start,
            showlegend=(idx == 0)
        ))
        
        fig.add_trace(go.Bar(
            y=[task['task_name']],
            x=[duration - completed_duration],
            name='Chưa hoàn thành',
            orientation='h',
            marker=dict(color='lightgray'),
            base=start + timedelta(days=completed_duration),
            showlegend=(idx == 0)
        ))
    
    fig.update_layout(
        title='Timeline Dự án',
        xaxis_title='Thời gian',
        yaxis_title='Công việc',
        barmode='stack',
        height=max(400, len(tasks_df) * 40)
    )
    
    return fig

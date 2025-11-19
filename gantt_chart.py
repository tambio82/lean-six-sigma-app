import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

def create_gantt_chart(tasks_df):
    """
    Tạo Gantt Chart cơ bản từ DataFrame tasks
    
    Args:
        tasks_df: DataFrame với columns: task_name, start_date, end_date, phase, status, progress
    
    Returns:
        plotly.graph_objects.Figure hoặc None nếu lỗi
    """
    if tasks_df.empty:
        return None
    
    try:
        # Prepare data
        df = tasks_df.copy()
        
        # Convert dates to datetime
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['end_date'] = pd.to_datetime(df['end_date'])
        
        # Add duration
        df['duration'] = (df['end_date'] - df['start_date']).dt.days
        
        # Color mapping by status
        color_map = {
            'Chưa bắt đầu': 'lightgray',
            'Đang thực hiện': 'steelblue',
            'Hoàn thành': 'green',
            'Tạm dừng': 'orange'
        }
        
        df['color'] = df['status'].map(color_map).fillna('lightgray')
        
        # Create figure
        fig = go.Figure()
        
        # Add bars
        for idx, row in df.iterrows():
            fig.add_trace(go.Bar(
                name=row['task_name'],
                x=[row['duration']],
                y=[row['task_name']],
                orientation='h',
                marker=dict(color=row['color']),
                base=row['start_date'],
                text=f"{row['progress']}%",
                textposition='inside',
                hovertemplate=(
                    f"<b>{row['task_name']}</b><br>" +
                    f"Phase: {row['phase']}<br>" +
                    f"Start: {row['start_date'].strftime('%Y-%m-%d')}<br>" +
                    f"End: {row['end_date'].strftime('%Y-%m-%d')}<br>" +
                    f"Status: {row['status']}<br>" +
                    f"Progress: {row['progress']}%<br>" +
                    f"Responsible: {row.get('responsible', 'N/A')}<br>" +
                    "<extra></extra>"
                )
            ))
        
        # Update layout
        fig.update_layout(
            title='Gantt Chart - Project Timeline',
            xaxis_title='Timeline',
            yaxis_title='Tasks',
            height=max(400, len(df) * 40),
            showlegend=False,
            xaxis=dict(type='date'),
            hovermode='closest'
        )
        
        return fig
    
    except Exception as e:
        print(f"Error creating gantt chart: {e}")
        return None


def create_dmaic_gantt(tasks_df):
    """
    Tạo Gantt Chart với group theo DMAIC phases
    
    Args:
        tasks_df: DataFrame với columns: task_name, start_date, end_date, phase, status, progress
    
    Returns:
        plotly.graph_objects.Figure hoặc None nếu lỗi
    """
    if tasks_df.empty:
        return None
    
    try:
        # Prepare data
        df = tasks_df.copy()
        
        # Convert dates
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['end_date'] = pd.to_datetime(df['end_date'])
        
        # DMAIC phase colors
        phase_colors = {
            'Define': '#FF6B6B',
            'Measure': '#4ECDC4',
            'Analyze': '#45B7D1',
            'Improve': '#96CEB4',
            'Control': '#FFEAA7'
        }
        
        df['color'] = df['phase'].map(phase_colors).fillna('lightgray')
        
        # Sort by phase order
        phase_order = ['Define', 'Measure', 'Analyze', 'Improve', 'Control']
        df['phase_order'] = df['phase'].apply(
            lambda x: phase_order.index(x) if x in phase_order else 999
        )
        df = df.sort_values(['phase_order', 'start_date'])
        
        # Create figure
        fig = go.Figure()
        
        # Add bars grouped by phase
        for idx, row in df.iterrows():
            fig.add_trace(go.Bar(
                name=row['task_name'],
                x=[row['end_date'] - row['start_date']],
                y=[f"{row['phase']}: {row['task_name']}"],
                orientation='h',
                marker=dict(color=row['color']),
                base=row['start_date'],
                text=f"{row['progress']}%",
                textposition='inside',
                hovertemplate=(
                    f"<b>{row['task_name']}</b><br>" +
                    f"Phase: {row['phase']}<br>" +
                    f"Start: {row['start_date'].strftime('%Y-%m-%d')}<br>" +
                    f"End: {row['end_date'].strftime('%Y-%m-%d')}<br>" +
                    f"Status: {row['status']}<br>" +
                    f"Progress: {row['progress']}%<br>" +
                    "<extra></extra>"
                )
            ))
        
        # Update layout
        fig.update_layout(
            title='DMAIC Gantt Chart',
            xaxis_title='Timeline',
            yaxis_title='Tasks by Phase',
            height=max(400, len(df) * 40),
            showlegend=False,
            xaxis=dict(type='date'),
            hovermode='closest'
        )
        
        return fig
    
    except Exception as e:
        print(f"Error creating DMAIC gantt: {e}")
        return None


def get_project_progress(tasks_df):
    """
    Tính % tiến độ tổng thể của dự án
    
    Args:
        tasks_df: DataFrame với column 'progress'
    
    Returns:
        int: % progress (0-100)
    """
    if tasks_df.empty:
        return 0
    
    try:
        avg_progress = tasks_df['progress'].mean()
        return int(round(avg_progress))
    except:
        return 0


def get_phase_summary(tasks_df):
    """
    Tạo bảng tóm tắt theo phase
    
    Args:
        tasks_df: DataFrame với columns: phase, status, progress
    
    Returns:
        DataFrame với summary theo phase
    """
    if tasks_df.empty:
        return pd.DataFrame()
    
    try:
        summary = tasks_df.groupby('phase').agg({
            'task_name': 'count',
            'progress': 'mean',
            'status': lambda x: (x == 'Hoàn thành').sum()
        }).reset_index()
        
        summary.columns = ['Phase', 'Tổng số task', 'Tiến độ TB (%)', 'Số task hoàn thành']
        summary['Tiến độ TB (%)'] = summary['Tiến độ TB (%)'].round(1)
        
        return summary
    except Exception as e:
        print(f"Error creating phase summary: {e}")
        return pd.DataFrame()


def check_overdue_tasks(tasks_df):
    """
    Kiểm tra các task quá hạn
    
    Args:
        tasks_df: DataFrame với columns: task_name, end_date, status, progress
    
    Returns:
        DataFrame chứa các task quá hạn
    """
    if tasks_df.empty:
        return pd.DataFrame()
    
    try:
        # Convert end_date to datetime
        df = tasks_df.copy()
        df['end_date'] = pd.to_datetime(df['end_date'])
        
        # Get today
        today = pd.Timestamp.now()
        
        # Filter overdue tasks (past deadline and not completed)
        overdue = df[
            (df['end_date'] < today) & 
            (df['status'] != 'Hoàn thành') &
            (df['progress'] < 100)
        ].copy()
        
        if not overdue.empty:
            overdue['days_overdue'] = (today - overdue['end_date']).dt.days
            overdue = overdue[['task_name', 'phase', 'end_date', 'responsible', 
                               'status', 'progress', 'days_overdue']]
            overdue.columns = ['Công việc', 'Phase', 'Deadline', 'Người phụ trách',
                              'Trạng thái', 'Tiến độ (%)', 'Quá hạn (ngày)']
            
            return overdue.sort_values('Quá hạn (ngày)', ascending=False)
        
        return pd.DataFrame()
    
    except Exception as e:
        print(f"Error checking overdue tasks: {e}")
        return pd.DataFrame()


# ==================== ADDITIONAL HELPER FUNCTIONS ====================

def get_critical_path(tasks_df):
    """
    Xác định critical path (đường găng) của dự án
    (Đơn giản hóa: tasks có thời gian dài nhất)
    """
    if tasks_df.empty:
        return pd.DataFrame()
    
    try:
        df = tasks_df.copy()
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['end_date'] = pd.to_datetime(df['end_date'])
        df['duration'] = (df['end_date'] - df['start_date']).dt.days
        
        # Get tasks with longest duration
        threshold = df['duration'].quantile(0.75)  # Top 25%
        critical = df[df['duration'] >= threshold].sort_values('duration', ascending=False)
        
        return critical[['task_name', 'phase', 'start_date', 'end_date', 'duration', 'status']]
    
    except:
        return pd.DataFrame()


def get_resource_allocation(tasks_df):
    """
    Phân tích phân bổ nguồn lực (người phụ trách)
    """
    if tasks_df.empty:
        return pd.DataFrame()
    
    try:
        if 'responsible' not in tasks_df.columns:
            return pd.DataFrame()
        
        allocation = tasks_df.groupby('responsible').agg({
            'task_name': 'count',
            'progress': 'mean'
        }).reset_index()
        
        allocation.columns = ['Người phụ trách', 'Số task', 'Tiến độ TB (%)']
        allocation['Tiến độ TB (%)'] = allocation['Tiến độ TB (%)'].round(1)
        
        return allocation.sort_values('Số task', ascending=False)
    
    except:
        return pd.DataFrame()


def create_timeline_chart(tasks_df):
    """
    Tạo timeline chart đơn giản với Plotly
    """
    if tasks_df.empty:
        return None
    
    try:
        df = tasks_df.copy()
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['end_date'] = pd.to_datetime(df['end_date'])
        
        fig = px.timeline(
            df,
            x_start='start_date',
            x_end='end_date',
            y='phase',
            color='status',
            hover_data=['task_name', 'responsible', 'progress'],
            title='Project Timeline by Phase'
        )
        
        fig.update_yaxes(categoryorder='total ascending')
        fig.update_layout(height=400)
        
        return fig
    
    except Exception as e:
        print(f"Error creating timeline chart: {e}")
        return None

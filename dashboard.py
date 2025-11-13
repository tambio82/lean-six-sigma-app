import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

def create_status_chart(stats_data, chart_type='pie'):
    """
    Tạo biểu đồ thống kê theo trạng thái dự án
    """
    df = stats_data['by_status']
    
    if df.empty:
        return None
    
    if chart_type == 'pie':
        fig = px.pie(
            df,
            values='count',
            names='status',
            title='Phân bố Dự án theo Trạng thái',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
    elif chart_type == 'bar':
        fig = px.bar(
            df,
            x='status',
            y='count',
            title='Số lượng Dự án theo Trạng thái',
            color='status',
            text='count'
        )
        fig.update_traces(textposition='outside')
    else:  # donut
        fig = go.Figure(data=[go.Pie(
            labels=df['status'],
            values=df['count'],
            hole=.4
        )])
        fig.update_layout(title='Phân bố Dự án theo Trạng thái')
    
    return fig

def create_category_chart(stats_data, chart_type='bar'):
    """
    Tạo biểu đồ thống kê theo danh mục dự án
    """
    df = stats_data['by_category']
    
    if df.empty:
        return None
    
    # Làm ngắn gọn tên danh mục nếu quá dài
    df['category_short'] = df['category'].apply(lambda x: x[:30] + '...' if len(str(x)) > 30 else x)
    
    if chart_type == 'bar':
        fig = px.bar(
            df,
            x='category_short',
            y='count',
            title='Số lượng Dự án theo Danh mục',
            color='count',
            text='count',
            color_continuous_scale='Blues'
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(xaxis_tickangle=-45)
    elif chart_type == 'pie':
        fig = px.pie(
            df,
            values='count',
            names='category',
            title='Phân bố Dự án theo Danh mục'
        )
    else:  # horizontal bar
        fig = px.bar(
            df,
            y='category',
            x='count',
            title='Số lượng Dự án theo Danh mục',
            orientation='h',
            text='count'
        )
        fig.update_traces(textposition='outside')
    
    return fig

def create_department_chart(stats_data, chart_type='bar'):
    """
    Tạo biểu đồ thống kê theo phòng ban
    """
    df = stats_data['by_department']
    
    if df.empty:
        return None
    
    if chart_type == 'bar':
        fig = px.bar(
            df,
            x='department',
            y='count',
            title='Số lượng Dự án theo Phòng/Ban',
            color='count',
            text='count',
            color_continuous_scale='Greens'
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(xaxis_tickangle=-45)
    elif chart_type == 'pie':
        fig = px.pie(
            df,
            values='count',
            names='department',
            title='Phân bố Dự án theo Phòng/Ban'
        )
    else:  # treemap
        fig = px.treemap(
            df,
            path=['department'],
            values='count',
            title='Phân bố Dự án theo Phòng/Ban'
        )
    
    return fig

def create_budget_chart(stats_data):
    """
    Tạo biểu đồ so sánh ngân sách vs chi phí thực tế
    """
    budget_stats = stats_data['budget_stats']
    
    if budget_stats.empty:
        return None
    
    total_budget = budget_stats.iloc[0]['total_budget'] or 0
    total_cost = budget_stats.iloc[0]['total_cost'] or 0
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Ngân sách dự kiến',
        x=['Tổng'],
        y=[total_budget],
        text=[f'{total_budget:,.0f} VNĐ'],
        textposition='outside',
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Bar(
        name='Chi phí thực tế',
        x=['Tổng'],
        y=[total_cost],
        text=[f'{total_cost:,.0f} VNĐ'],
        textposition='outside',
        marker_color='coral'
    ))
    
    fig.update_layout(
        title='So sánh Ngân sách và Chi phí Thực tế',
        yaxis_title='Số tiền (VNĐ)',
        barmode='group'
    )
    
    return fig

def create_overview_dashboard(stats_data):
    """
    Tạo dashboard tổng quan với nhiều biểu đồ
    """
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Dự án theo Trạng thái',
            'Dự án theo Danh mục',
            'Dự án theo Phòng/Ban',
            'Ngân sách vs Chi phí'
        ),
        specs=[
            [{'type': 'pie'}, {'type': 'bar'}],
            [{'type': 'bar'}, {'type': 'bar'}]
        ]
    )
    
    # Status pie chart
    if not stats_data['by_status'].empty:
        df_status = stats_data['by_status']
        fig.add_trace(
            go.Pie(labels=df_status['status'], values=df_status['count']),
            row=1, col=1
        )
    
    # Category bar chart
    if not stats_data['by_category'].empty:
        df_cat = stats_data['by_category']
        fig.add_trace(
            go.Bar(x=df_cat['category'], y=df_cat['count'], name='Danh mục'),
            row=1, col=2
        )
    
    # Department bar chart
    if not stats_data['by_department'].empty:
        df_dept = stats_data['by_department']
        fig.add_trace(
            go.Bar(x=df_dept['department'], y=df_dept['count'], name='Phòng/Ban'),
            row=2, col=1
        )
    
    # Budget comparison
    if not stats_data['budget_stats'].empty:
        budget_stats = stats_data['budget_stats'].iloc[0]
        fig.add_trace(
            go.Bar(
                x=['Ngân sách', 'Chi phí'],
                y=[budget_stats['total_budget'] or 0, budget_stats['total_cost'] or 0],
                name='Tài chính'
            ),
            row=2, col=2
        )
    
    fig.update_layout(
        height=800,
        showlegend=False,
        title_text="Dashboard Tổng quan Dự án Lean Six Sigma"
    )
    
    return fig

def create_timeline_scatter(projects_df):
    """
    Tạo scatter plot timeline của các dự án
    """
    if projects_df.empty:
        return None
    
    # Chuyển đổi ngày tháng
    projects_df['start_date'] = pd.to_datetime(projects_df['start_date'])
    projects_df['end_date'] = pd.to_datetime(projects_df['end_date'])
    
    fig = px.scatter(
        projects_df,
        x='start_date',
        y='project_name',
        size='budget',
        color='status',
        hover_data=['department', 'category'],
        title='Timeline các Dự án'
    )
    
    # Thêm đường kết thúc
    for _, row in projects_df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['start_date'], row['end_date']],
            y=[row['project_name'], row['project_name']],
            mode='lines',
            line=dict(color='gray', width=2),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    return fig

def create_metrics_cards(stats_data):
    """
    Tạo các metrics card cho dashboard
    """
    total_projects = stats_data['total_projects']
    budget_stats = stats_data['budget_stats']
    
    total_budget = budget_stats.iloc[0]['total_budget'] or 0 if not budget_stats.empty else 0
    total_cost = budget_stats.iloc[0]['total_cost'] or 0 if not budget_stats.empty else 0
    
    budget_utilization = (total_cost / total_budget * 100) if total_budget > 0 else 0
    
    return {
        'total_projects': total_projects,
        'total_budget': total_budget,
        'total_cost': total_cost,
        'budget_utilization': round(budget_utilization, 1)
    }

def create_heatmap(projects_df):
    """
    Tạo heatmap số lượng dự án theo tháng và năm
    """
    if projects_df.empty:
        return None
    
    # Chuyển đổi ngày
    projects_df['start_date'] = pd.to_datetime(projects_df['start_date'])
    projects_df['year'] = projects_df['start_date'].dt.year
    projects_df['month'] = projects_df['start_date'].dt.month
    
    # Đếm số dự án theo tháng và năm
    heatmap_data = projects_df.groupby(['year', 'month']).size().reset_index(name='count')
    
    # Pivot để tạo ma trận
    pivot_data = heatmap_data.pivot(index='year', columns='month', values='count').fillna(0)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=['Th1', 'Th2', 'Th3', 'Th4', 'Th5', 'Th6', 
           'Th7', 'Th8', 'Th9', 'Th10', 'Th11', 'Th12'],
        y=pivot_data.index,
        colorscale='Blues',
        text=pivot_data.values,
        texttemplate='%{text}',
        textfont={"size": 10}
    ))
    
    fig.update_layout(
        title='Số lượng Dự án khởi động theo Tháng/Năm',
        xaxis_title='Tháng',
        yaxis_title='Năm'
    )
    
    return fig

def create_funnel_chart(stats_data):
    """
    Tạo funnel chart theo các giai đoạn dự án
    """
    df = stats_data['by_status']
    
    if df.empty:
        return None
    
    fig = go.Figure(go.Funnel(
        y=df['status'],
        x=df['count'],
        textinfo="value+percent initial"
    ))
    
    fig.update_layout(
        title='Funnel Trạng thái Dự án'
    )
    
    return fig

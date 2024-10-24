import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta
from utils import calculate_growth
import plotly.graph_objects as go
def show_overview_report(df):
    st.header('Báo cáo tổng quan')
    
    time_filter = st.selectbox('Chọn khoảng thời gian', 
                               ['7 ngày qua', '30 ngày qua', '6 tháng qua', '1 năm qua', 'Tùy chỉnh'])

    df['day'] = pd.to_datetime(df['day'])
    end_date = df['day'].max()
    if time_filter == '7 ngày qua':
        start_date = end_date - timedelta(days=6)
    elif time_filter == '30 ngày qua':
        start_date = end_date - timedelta(days=29)
    elif time_filter == '6 tháng qua':
        start_date = end_date - timedelta(days=180)
    elif time_filter == '1 năm qua':
        start_date = end_date - timedelta(days=365)
    else:
        # Chuyển đổi day về datetime trước khi lấy min/max
        df['day'] = pd.to_datetime(df['day'])
        start_date = st.date_input('Ngày bắt đầu', min(df['day']).date())
        end_date = st.date_input('Ngày kết thúc', max(df['day']).date())

    # Chuyển đổi start_date và end_date thành Timestamp
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)

    filtered_df = df[(df['day'] >= start_date) & (df['day'] <= end_date)]
    previous_start = start_date - (end_date - start_date)
    previous_df = df[(df['day'] >= previous_start) & (df['day'] < start_date)]

    show_metrics(filtered_df, previous_df)
    show_time_series_chart(filtered_df)
    show_ad_name_chart(filtered_df)

def show_metrics(filtered_df, previous_df):
    col1, col2, col3, col4 = st.columns(4)

    metrics = ['spend', 'revenue', 'profit', 'net_profit']
    labels = ['Tổng chi phí', 'Tổng doanh thu', 'Tổng lợi nhuận', 'Lợi nhuận ròng']
    columns = [col1, col2, col3, col4]

    for metric, label, col in zip(metrics, labels, columns):
        current_value = filtered_df[metric].sum()
        previous_value = previous_df[metric].sum()
        growth = calculate_growth(current_value, previous_value)
        formatted_value = format_number(current_value)
        col.metric(label, f"{formatted_value} đ", f"{growth:+.2f}%", delta_color="inverse" if metric == 'spend' else "normal")

def show_time_series_chart(filtered_df):
    st.subheader('Biểu đồ theo thời gian')
    
    # Kiểm tra khoảng thời gian
    date_range = (filtered_df['day'].max() - filtered_df['day'].min()).days
    
    if date_range > 30:
        # Nhóm dữ liệu theo tháng
        monthly_df = filtered_df.resample('M', on='day').sum().reset_index()
        
        # Tạo biểu đồ đường
        fig1 = px.line(monthly_df, x='day', y=['spend', 'revenue', 'profit', 'net_profit'], 
                      title='Chỉ số theo tháng (Biểu đồ đường)', line_shape='spline')
        fig1.update_xaxes(title_text='Tháng')
        fig1.update_yaxes(title_text='Giá trị')
        st.plotly_chart(fig1, use_container_width=True)
        
        # Tạo biểu đồ cột
        fig2 = px.bar(monthly_df, x='day', y=['spend', 'revenue', 'profit', 'net_profit'],
                      title='Chỉ số theo tháng (Biểu đồ cột)', barmode='group')
        fig2.update_xaxes(title_text='Tháng')
        fig2.update_yaxes(title_text='Giá trị')
        st.plotly_chart(fig2, use_container_width=True)
        
        # Tạo biểu đồ area
        fig3 = px.area(monthly_df, x='day', y=['spend', 'revenue', 'profit', 'net_profit'],
                       title='Chỉ số theo tháng (Biểu đồ area)')
        fig3.update_xaxes(title_text='Tháng')
        fig3.update_yaxes(title_text='Giá trị')
        st.plotly_chart(fig3, use_container_width=True)
    else:
        # Hiển thị dữ liệu hàng ngày với biểu đồ kết hợp
        fig = go.Figure()

        # Thêm đường cho spend và revenue
        fig.add_trace(go.Scatter(x=filtered_df['day'], y=filtered_df['spend'], name='Chi phí', line=dict(color='red', width=2)))
        fig.add_trace(go.Scatter(x=filtered_df['day'], y=filtered_df['revenue'], name='Doanh thu', line=dict(color='green', width=2)))

        # Thêm cột cho profit và net_profit
        fig.add_trace(go.Bar(x=filtered_df['day'], y=filtered_df['profit'], name='Lợi nhuận', marker_color='blue', opacity=0.7))
        fig.add_trace(go.Bar(x=filtered_df['day'], y=filtered_df['net_profit'], name='Lợi nhuận ròng', marker_color='purple', opacity=0.7))

        # Cập nhật layout
        fig.update_layout(
            title='Chỉ số theo thời gian',
            xaxis_title='Ngày',
            yaxis_title='Giá trị',
            barmode='group',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        # Hiển thị biểu đồ
        st.plotly_chart(fig, use_container_width=True)

        # Thêm chú thích
        st.info('Biểu đồ trên kết hợp đường và cột để thể hiện sự thay đổi theo thời gian. '
                'Đường màu đỏ thể hiện chi phí, đường màu xanh lá thể hiện doanh thu. '
                'Cột màu xanh dương thể hiện lợi nhuận, cột màu tím thể hiện lợi nhuận ròng.')

def show_ad_name_chart(filtered_df):
    st.subheader('Biểu đồ theo AD_NAME')
    grouped_df = filtered_df.groupby('ad_name').agg({
        'spend': 'sum',
        'revenue': 'sum',
        'profit': 'sum',
        'net_profit': 'sum'
    }).reset_index()

    fig = px.bar(grouped_df, x='ad_name', y=['spend', 'revenue', 'profit', 'net_profit'], 
                 title='Chỉ số theo AD_NAME', barmode='group')
    st.plotly_chart(fig, use_container_width=True)

def format_number(number):
    if number >= 1000000:
        return f"{number/1000000:.1f}M"
    elif number >= 1000:
        return f"{number/1000:.1f}k"
    else:
        return f"{number:.0f}"

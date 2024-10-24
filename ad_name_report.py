import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta
from utils import calculate_growth, calculate_metrics_with_growth

def show_ad_name_report(df):
    st.header('Báo cáo theo AD_NAME')

    selected_ad_name = st.selectbox('Chọn AD_NAME', df['ad_name'].unique(), key='ad_name_select')
    
    time_filter = st.selectbox('Chọn khoảng thời gian', 
                               ['7 ngày qua', '30 ngày qua', '6 tháng qua', '1 năm qua', 'Tùy chỉnh'],
                               key='time_filter_select')

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
        start_date = st.date_input('Ngày bắt đầu', min(df['day']), key='start_date_input')
        end_date = st.date_input('Ngày kết thúc', max(df['day']), key='end_date_input')

    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)

    ad_df = df[(df['ad_name'] == selected_ad_name) & (df['day'] >= start_date) & (df['day'] <= end_date)]
    previous_start = start_date - (end_date - start_date)
    previous_df = df[(df['ad_name'] == selected_ad_name) & (df['day'] >= previous_start) & (df['day'] < start_date)]

    show_ad_metrics(ad_df, previous_df)
    show_ad_time_series_chart(ad_df, selected_ad_name)
    show_pivot_table(df)

def show_ad_metrics(ad_df, previous_df):
    col1, col2, col3, col4 = st.columns(4)

    metrics = ['spend', 'revenue', 'profit', 'net_profit']
    labels = ['Tổng chi phí', 'Tổng doanh thu', 'Tổng lợi nhuận', 'Lợi nhuận ròng']
    columns = [col1, col2, col3, col4]

    for metric, label, col in zip(metrics, labels, columns):
        current_value = ad_df[metric].sum()
        previous_value = previous_df[metric].sum()
        growth = calculate_growth(current_value, previous_value)
        formatted_value = format_number(current_value)
        col.metric(label, f"{formatted_value} đ", f"{growth:+.2f}%", delta_color="inverse" if metric == 'spend' else "normal")

def show_ad_time_series_chart(ad_df, selected_ad_name):
    st.subheader('Biểu đồ theo thời gian')
    
    date_range = (ad_df['day'].max() - ad_df['day'].min()).days
    
    if date_range > 30:
        monthly_df = ad_df.resample('M', on='day').sum().reset_index()
        
        fig1 = px.line(monthly_df, x='day', y=['spend', 'revenue', 'profit', 'net_profit'], 
                      title=f'Chỉ số theo tháng cho {selected_ad_name} (Biểu đồ đường)', line_shape='spline')
        fig1.update_xaxes(title_text='Tháng')
        fig1.update_yaxes(title_text='Giá trị')
        st.plotly_chart(fig1, use_container_width=True)
        
        fig2 = px.bar(monthly_df, x='day', y=['spend', 'revenue', 'profit', 'net_profit'],
                      title=f'Chỉ số theo tháng cho {selected_ad_name} (Biểu đồ cột)', barmode='group')
        fig2.update_xaxes(title_text='Tháng')
        fig2.update_yaxes(title_text='Giá trị')
        st.plotly_chart(fig2, use_container_width=True)
        
        fig3 = px.area(monthly_df, x='day', y=['spend', 'revenue', 'profit', 'net_profit'],
                       title=f'Chỉ số theo tháng cho {selected_ad_name} (Biểu đồ area)')
        fig3.update_xaxes(title_text='Tháng')
        fig3.update_yaxes(title_text='Giá trị')
        st.plotly_chart(fig3, use_container_width=True)
    else:
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=ad_df['day'], y=ad_df['spend'], name='Chi phí', line=dict(color='red', width=2)))
        fig.add_trace(go.Scatter(x=ad_df['day'], y=ad_df['revenue'], name='Doanh thu', line=dict(color='green', width=2)))
        fig.add_trace(go.Bar(x=ad_df['day'], y=ad_df['profit'], name='Lợi nhuận', marker_color='blue', opacity=0.7))
        fig.add_trace(go.Bar(x=ad_df['day'], y=ad_df['net_profit'], name='Lợi nhuận ròng', marker_color='purple', opacity=0.7))

        fig.update_layout(
            title=f'Chỉ số theo thời gian cho {selected_ad_name}',
            xaxis_title='Ngày',
            yaxis_title='Giá trị',
            barmode='group',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

        st.info('Biểu đồ trên kết hợp đường và cột để thể hiện sự thay đổi theo thời gian. '
                'Đường màu đỏ thể hiện chi phí, đường màu xanh lá thể hiện doanh thu. '
                'Cột màu xanh dương thể hiện lợi nhuận, cột màu tím thể hiện lợi nhuận ròng.')

def show_pivot_table(df):
    st.subheader('Bảng Pivot')
    selected_period = st.selectbox('Chọn khoảng thời gian cho Pivot', [7, 14, 30, 90, 180])

    pivot_data = []
    for ad_name in df['ad_name'].unique():
        ad_df = df[df['ad_name'] == ad_name]
        row = {'ad_name': ad_name}
        row.update(calculate_metrics_with_growth(ad_df, selected_period))
        pivot_data.append(row)

    pivot_df = pd.DataFrame(pivot_data)

    formatted_columns = {}
    for col in pivot_df.columns:
        if col != 'ad_name':
            if 'growth' in col:
                formatted_columns[col] = '{:+.2f}%'
            else:
                formatted_columns[col] = '{:,.0f} đ'

    st.dataframe(pivot_df.style.format(formatted_columns))

def format_number(number):
    if number >= 1000000:
        return f"{number/1000000:.1f}M"
    elif number >= 1000:
        return f"{number/1000:.1f}k"
    else:
        return f"{number:.0f}"

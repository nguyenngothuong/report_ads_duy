import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta
from utils import calculate_growth
import plotly.graph_objects as go
from guides import OVERVIEW_GUIDE, CHART_GUIDE

def show_overview_report(df):
    st.header('Báo cáo tổng quan')
    
    # Thêm checkbox cho hướng dẫn sử dụng
    if st.checkbox('Hiển thị hướng dẫn sử dụng', False, key='overview_guide'):
        st.info(OVERVIEW_GUIDE)
        st.info(CHART_GUIDE)
    
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
    # show_ad_name_chart(filtered_df)

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
        # Thay thế phần chú thích cũ bằng phần chú thích mới này
        st.info("""
        ### 📊 Hướng dẫn đọc biểu đồ và chỉ số

        #### 🎯 Các chỉ số chính:
        1. **Chi phí (🔴 Đường đỏ):**
        - Tổng chi phí quảng cáo đã chi
        - Bao gồm: chi phí chạy quảng cáo, chi phí tối ưu,...
        - Xu hướng tăng cần đi kèm với tăng doanh thu

        2. **Doanh thu (🟢 Đường xanh lá):**
        - Tổng doanh thu từ quảng cáo
        - Chỉ số này cần luôn cao hơn chi phí
        - Tỷ lệ chênh lệch với chi phí càng cao càng tốt

        3. **Lợi nhuận (🔵 Cột xanh dương):**
        - Được tính bằng: Doanh thu - Chi phí
        - Chỉ số dương: quảng cáo có lãi
        - Chỉ số âm: quảng cáo đang lỗ

        4. **Lợi nhuận ròng (🟣 Cột tím):**
        - Lợi nhuận sau khi trừ thuế (7%)
        - Phản ánh lợi nhuận thực tế
        - Dùng để đánh giá hiệu quả cuối cùng

        #### 📈 Cách đọc biểu đồ:
        - **Khoảng cách giữa đường đỏ và xanh:** Càng xa càng có lợi nhuận cao
        - **Chiều cao cột xanh dương:** Thể hiện mức độ sinh lời
        - **Chênh lệch cột tím và xanh:** Phản ánh tác động của thuế

        #### ⚠️ Các dấu hiệu cần chú ý:
        - Chi phí tăng nhưng doanh thu không tăng tương ứng
        - Lợi nhuận giảm liên tục hoặc âm
        - Khoảng cách giữa đường đỏ và xanh bị thu hẹp

        #### 💡 Mẹo phân tích:
        - So sánh các chỉ số theo thời gian để thấy xu hướng
        - Đánh giá tỷ lệ chi phí/doanh thu (không nên vượt quá 70%)
        - Chú ý đến các thời điểm có biến động lớn để tìm nguyên nhân
        """)
                
        
# def show_ad_name_chart(filtered_df):
#     st.subheader('Biểu đồ theo AD_NAME')
    
#     # Tính tổng theo ad_name
#     grouped_df = filtered_df.groupby('ad_name').agg({
#         'spend': 'sum',
#         'revenue': 'sum', 
#         'profit': 'sum',
#         'net_profit': 'sum'
#     }).reset_index()
    
#     # Thêm các filter mẫu
#     filter_options = [
#         "Tùy chỉnh",
#         "Top 10 AD_NAME có lợi nhuận cao nhất",
#         "Top 10 AD_NAME có doanh thu cao nhất", 
#         "Top 10 AD_NAME có chi phí thấp nhất",
#         "Top 10 AD_NAME có ROI tốt nhất",
#         "Top 10 AD_NAME có lợi nhuận âm"
#     ]
    
#     selected_filter = st.selectbox("Chọn bộ lọc:", filter_options)
    
#     if selected_filter == "Tùy chỉnh":
#         # Cho phép user chọn số lượng top AD_NAME muốn xem
#         max_ads = len(grouped_df)
#         default_value = min(20, max_ads)
#         top_n = st.number_input('Số lượng AD_NAME muốn xem:', min_value=1, max_value=max_ads, value=default_value)
        
#         # Thêm thanh kéo để lọc theo revenue
#         min_revenue = float(grouped_df['revenue'].min())
#         max_revenue = float(grouped_df['revenue'].max())
        
#         if min_revenue == max_revenue:
#             min_revenue = 0
#             max_revenue = max(max_revenue, 1000000)
        
#         revenue_range = st.slider(
#             'Lọc theo khoảng Revenue:',
#             min_value=min_revenue,
#             max_value=max_revenue,
#             value=(min_revenue, max_revenue)
#         )
        
#         filtered_by_revenue = grouped_df[
#             (grouped_df['revenue'] >= revenue_range[0]) & 
#             (grouped_df['revenue'] <= revenue_range[1])
#         ]
#         display_df = filtered_by_revenue.nlargest(top_n, 'revenue')
#         title = f'Top {top_n} AD_NAME theo Revenue'
        
#     else:
#         if selected_filter == "Top 10 AD_NAME có lợi nhuận cao nhất":
#             display_df = grouped_df.nlargest(10, 'profit')
#             title = 'Top 10 AD_NAME có lợi nhuận cao nhất'
#         elif selected_filter == "Top 10 AD_NAME có doanh thu cao nhất":
#             display_df = grouped_df.nlargest(10, 'revenue')
#             title = 'Top 10 AD_NAME có doanh thu cao nhất'
#         elif selected_filter == "Top 10 AD_NAME có chi phí thấp nhất":
#             display_df = grouped_df.nsmallest(10, 'spend')
#             title = 'Top 10 AD_NAME có chi phí thấp nhất'
#         elif selected_filter == "Top 10 AD_NAME có ROI tốt nhất":
#             grouped_df['roi'] = (grouped_df['revenue'] - grouped_df['spend']) / grouped_df['spend'] * 100
#             display_df = grouped_df.nlargest(10, 'roi')
#             title = 'Top 10 AD_NAME có ROI tốt nhất'
#         else:  # Top 10 AD_NAME có lợi nhuận âm
#             display_df = grouped_df[grouped_df['profit'] < 0].nlargest(10, 'spend')
#             title = 'Top 10 AD_NAME có lợi nhuận âm'
    
#     # Tạo biểu đồ ngang
#     fig = px.bar(display_df, y='ad_name', x=['spend', 'revenue', 'profit', 'net_profit'],
#                  title=title,
#                  barmode='group',
#                  orientation='h')
    
#     fig.update_layout(
#         yaxis_title="AD_NAME",
#         xaxis_title="Giá trị",
#         legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
#     )
    
#     st.plotly_chart(fig, use_container_width=True)
    
#     # Thêm bộ lọc tìm kiếm
#     search_term = st.text_input("Tìm kiếm AD_NAME:", "")
#     if search_term:
#         filtered_ads = grouped_df[grouped_df['ad_name'].str.contains(search_term, case=False)]
#         if not filtered_ads.empty:
#             fig2 = px.bar(filtered_ads, y='ad_name', x=['spend', 'revenue', 'profit', 'net_profit'],
#                          title=f'Kết quả tìm kiếm cho "{search_term}"',
#                          barmode='group',
#                          orientation='h')
#             fig2.update_layout(
#                 yaxis_title="AD_NAME",
#                 xaxis_title="Giá trị",
#                 legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
#             )
#             st.plotly_chart(fig2, use_container_width=True)
#         else:
#             st.warning("Không tìm thấy AD_NAME phù hợp")

def format_number(number):
    if number >= 1000000:
        return f"{number/1000000:.1f}M"
    elif number >= 1000:
        return f"{number/1000:.1f}k"
    else:
        return f"{number:.0f}"


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta
from utils import calculate_growth, calculate_metrics_with_growth

def show_ad_name_report(df):
    st.header('Báo cáo theo AD_NAME')

    # Thêm checkbox cho hướng dẫn sử dụng
    if st.checkbox('Hiển thị hướng dẫn sử dụng', False):
        st.info("""
        ### 📌 Hướng dẫn sử dụng báo cáo theo AD_NAME
        
        1. **Bộ lọc chung:**
           - Sử dụng bộ lọc SUBID1, SUBID2, SUBID3 để lọc dữ liệu theo từng cấp độ
           - Chọn "Tất cả" để xem toàn bộ dữ liệu
        
        2. **Biểu đồ tổng quan:**
           - Chọn bộ lọc để xem top AD_NAME theo các tiêu chí khác nhau
           - Sử dụng thanh trượt để lọc theo khoảng Revenue
           - Tìm kiếm AD_NAME cụ thể bằng ô tìm kiếm
        
        3. **Báo cáo chi tiết:**
           - Chọn AD_NAME cụ thể để xem chi tiết
           - Chọn khoảng thời gian phân tích
           - Xem biểu đồ theo thời gian và bảng phân tích chi tiết
        
        4. **Đọc hiểu biểu đồ:**
           - 🔴 Đường đỏ: Chi phí
           - 🟢 Đường xanh lá: Doanh thu
           - 🔵 Cột xanh dương: Lợi nhuận
           - 🟣 Cột tím: Lợi nhuận ròng
        
        5. **Bảng phân tích chi tiết:**
           - Xem số liệu và tăng trưởng theo từng khoảng thời gian
           - Các chỉ số tăng trưởng dương (+) thể hiện sự cải thiện
           - Các chỉ số tăng trưởng âm (-) cần được chú ý và có biện pháp cải thiện
        """)

    # Thêm filter theo subid3, subid2, subid1 cho phần tổng quan
    col1, col2, col3 = st.columns(3)
    with col3:
        selected_subid1 = st.selectbox('Chọn SUBID1', ['Tất cả'] + list(df['subid1'].unique()), key='overview_subid1_select')
    with col2:
        selected_subid2 = st.selectbox('Chọn SUBID2', ['Tất cả'] + list(df['subid2'].unique()), key='overview_subid2_select')
    with col1:
        selected_subid3 = st.selectbox('Chọn SUBID3', ['Tất cả'] + list(df['subid3'].unique()), key='overview_subid3_select')

    # Lọc dữ liệu cho phần tổng quan theo các filter đã chọn
    filtered_overview_df = df.copy()
    if selected_subid1 != 'Tất cả':
        filtered_overview_df = filtered_overview_df[filtered_overview_df['subid1'] == selected_subid1]
    if selected_subid2 != 'Tất cả':
        filtered_overview_df = filtered_overview_df[filtered_overview_df['subid2'] == selected_subid2]
    if selected_subid3 != 'Tất cả':
        filtered_overview_df = filtered_overview_df[filtered_overview_df['subid3'] == selected_subid3]

    # Kiểm tra nếu không có dữ liệu
    if filtered_overview_df.empty:
        st.warning("Không có dữ liệu phù hợp với bộ lọc đã chọn")
        return

    # Thêm phần biểu đồ tổng quan theo AD_NAME trước
    show_ad_name_chart(filtered_overview_df)
    st.divider()  # Thêm đường phân cách

    # Tiếp tục với phần chi tiết theo từng AD_NAME

    selected_ad_name = st.selectbox('Chọn AD_NAME để xem chi tiết', df['ad_name'].unique(), key='ad_name_select')

    
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

    # Lọc dữ liệu theo các filter đã chọn
    filtered_df = df[(df['ad_name'] == selected_ad_name) & (df['day'] >= start_date) & (df['day'] <= end_date)]
    
    if selected_subid1 != 'Tất cả':
        filtered_df = filtered_df[filtered_df['subid1'] == selected_subid1]
    if selected_subid2 != 'Tất cả':
        filtered_df = filtered_df[filtered_df['subid2'] == selected_subid2]
    if selected_subid3 != 'Tất cả':
        filtered_df = filtered_df[filtered_df['subid3'] == selected_subid3]

    # Kiểm tra nếu không có dữ liệu sau khi lọc
    if filtered_df.empty:
        st.warning("Không có dữ liệu phù hợp với các bộ lọc đã chọn")
        return

    previous_start = start_date - (end_date - start_date)
    previous_df = df[(df['ad_name'] == selected_ad_name) & (df['day'] >= previous_start) & (df['day'] < start_date)]

    show_ad_metrics(filtered_df, previous_df)
    show_ad_time_series_chart(filtered_df, selected_ad_name)
    show_pivot_table(df)

def show_ad_name_chart(df):
    st.subheader('Tổng quan theo AD_NAME')
    
    # Tính tổng theo ad_name
    grouped_df = df.groupby('ad_name').agg({
        'spend': 'sum',
        'revenue': 'sum', 
        'profit': 'sum',
        'net_profit': 'sum'
    }).reset_index()

    # Kiểm tra nếu không có dữ liệu
    if grouped_df.empty:
        st.warning("Không có dữ liệu để hiển thị")
        return
    
    # Thêm các filter mẫu
    filter_options = [
        "Tùy chỉnh",
        "Top 10 AD_NAME có lợi nhuận cao nhất",
        "Top 10 AD_NAME có doanh thu cao nhất", 
        "Top 10 AD_NAME có chi phí thấp nhất",
        "Top 10 AD_NAME có ROI tốt nhất",
        "Top 10 AD_NAME có lợi nhuận âm"
    ]
    
    selected_filter = st.selectbox("Chọn bộ lọc:", filter_options, key='overview_filter_select')
    
    if selected_filter == "Tùy chỉnh":
        # Cho phép user chọn số lượng top AD_NAME muốn xem
        max_ads = len(grouped_df)
        if max_ads == 0:
            st.warning("Không có dữ liệu để hiển thị")
            return
            
        default_value = min(20, max_ads)
        top_n = st.number_input(
            'Số lượng AD_NAME muốn xem:', 
            min_value=1, 
            max_value=max_ads, 
            value=default_value,
            key='overview_top_n_input'
        )
        
        # Thêm thanh kéo để lọc theo revenue
        min_revenue = int(grouped_df['revenue'].min())
        max_revenue = int(grouped_df['revenue'].max())
        
        if min_revenue == max_revenue:
            min_revenue = 0
            max_revenue = max(max_revenue, 1000000)
            
        # Format giá trị min/max để hiển thị
        min_revenue_display = format_number(min_revenue)
        max_revenue_display = format_number(max_revenue)
        
        revenue_range = st.slider(
            f'Lọc theo khoảng Revenue ({min_revenue_display}đ - {max_revenue_display}đ):',
            min_value=min_revenue,
            max_value=max_revenue,
            value=(min_revenue, max_revenue),
            key='overview_revenue_slider',
            format='%0.0f'
        )
        
        filtered_by_revenue = grouped_df[
            (grouped_df['revenue'] >= revenue_range[0]) & 
            (grouped_df['revenue'] <= revenue_range[1])
        ]

        if filtered_by_revenue.empty:
            st.warning("Không có dữ liệu phù hợp với khoảng Revenue đã chọn")
            return

        display_df = filtered_by_revenue.nlargest(top_n, 'revenue')
        title = f'Top {top_n} AD_NAME theo Revenue'
    else:
        if selected_filter == "Top 10 AD_NAME có lợi nhuận cao nhất":
            display_df = grouped_df.nlargest(10, 'profit')
            title = 'Top 10 AD_NAME có lợi nhuận cao nhất'
        elif selected_filter == "Top 10 AD_NAME có doanh thu cao nhất":
            display_df = grouped_df.nlargest(10, 'revenue')
            title = 'Top 10 AD_NAME có doanh thu cao nhất'
        elif selected_filter == "Top 10 AD_NAME có chi phí thấp nhất":
            display_df = grouped_df.nsmallest(10, 'spend')
            title = 'Top 10 AD_NAME có chi phí thấp nhất'
        elif selected_filter == "Top 10 AD_NAME có ROI tốt nhất":
            grouped_df['roi'] = (grouped_df['revenue'] - grouped_df['spend']) / grouped_df['spend'] * 100
            display_df = grouped_df.nlargest(10, 'roi')
            title = 'Top 10 AD_NAME có ROI tốt nhất'
        else:  # Top 10 AD_NAME có lợi nhuận âm
            negative_profit_df = grouped_df[grouped_df['profit'] < 0]
            if negative_profit_df.empty:
                st.warning("Không có AD_NAME nào có lợi nhuận âm")
                return
            display_df = negative_profit_df.nlargest(10, 'spend')
            title = 'Top 10 AD_NAME có lợi nhuận âm'

    if display_df.empty:
        st.warning("Không có dữ liệu phù hợp với bộ lọc đã chọn")
        return
    
    # Tạo biểu đồ ngang
    fig = px.bar(display_df, y='ad_name', x=['spend', 'revenue', 'profit', 'net_profit'],
                 title=title,
                 barmode='group',
                 orientation='h')
    
    fig.update_layout(
        yaxis_title="AD_NAME",
        xaxis_title="Giá trị",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Thêm bộ lọc tìm kiếm
    search_term = st.text_input("Tìm kiếm AD_NAME:", "", key='overview_search_input')
    if search_term:
        filtered_ads = grouped_df[grouped_df['ad_name'].str.contains(search_term, case=False)]
        if not filtered_ads.empty:
            fig2 = px.bar(filtered_ads, y='ad_name', x=['spend', 'revenue', 'profit', 'net_profit'],
                         title=f'Kết quả tìm kiếm cho "{search_term}"',
                         barmode='group',
                         orientation='h')
            fig2.update_layout(
                yaxis_title="AD_NAME",
                xaxis_title="Giá trị",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("Không tìm thấy AD_NAME phù hợp")

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
    
    if ad_df.empty:
        st.warning("Không có dữ liệu để hiển thị biểu đồ")
        return
        
    date_range = (ad_df['day'].max() - ad_df['day'].min()).days
    
    if date_range > 30:
        monthly_df = ad_df.resample('M', on='day').sum().reset_index()
        
        fig1 = px.line(monthly_df, x='day', y=['spend', 'revenue', 'profit', 'net_profit'], 
                      title=f'Chỉ số theo tháng cho {selected_ad_name} (Biểu đồ đường)', 
                      line_shape='spline',
                      labels={
                          'spend': 'Chi phí',
                          'revenue': 'Doanh thu',
                          'profit': 'Lợi nhuận',
                          'net_profit': 'Lợi nhuận ròng',
                          'day': 'Tháng',
                          'value': 'Giá trị'
                      })
        fig1.update_traces(textposition="top center")
        fig1.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
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

        # Thêm đường cho spend và revenue với label
        fig.add_trace(go.Scatter(
            x=ad_df['day'], 
            y=ad_df['spend'], 
            name='Chi phí', 
            line=dict(color='red', width=2),
            text=ad_df['spend'].apply(lambda x: f'{x:,.0f}đ'),
            textposition='top center'
        ))
        fig.add_trace(go.Scatter(
            x=ad_df['day'], 
            y=ad_df['revenue'], 
            name='Doanh thu', 
            line=dict(color='green', width=2),
            text=ad_df['revenue'].apply(lambda x: f'{x:,.0f}đ'),
            textposition='top center'
        ))

        # Thêm cột cho profit và net_profit với label
        fig.add_trace(go.Bar(
            x=ad_df['day'], 
            y=ad_df['profit'], 
            name='Lợi nhuận', 
            marker_color='blue', 
            opacity=0.7,
            text=ad_df['profit'].apply(lambda x: f'{x:,.0f}đ'),
            textposition='outside'
        ))
        fig.add_trace(go.Bar(
            x=ad_df['day'], 
            y=ad_df['net_profit'], 
            name='Lợi nhuận ròng', 
            marker_color='purple', 
            opacity=0.7,
            text=ad_df['net_profit'].apply(lambda x: f'{x:,.0f}đ'),
            textposition='outside'
        ))

        # Cập nhật layout
        fig.update_layout(
            title=f'Chỉ số theo thời gian cho {selected_ad_name}',
            xaxis_title='Ngày',
            yaxis_title='Giá trị',
            barmode='group',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            # Thêm margin để đảm bảo label không bị cắt
            margin=dict(t=150)
        )

        st.plotly_chart(fig, use_container_width=True)

        # Thêm chú thích với emoji
        st.info("""
        🔍 **Hướng dẫn đọc biểu đồ:**
        - 🔴 Đường đỏ: Chi phí quảng cáo
        - 🟢 Đường xanh lá: Doanh thu
        - 🔵 Cột xanh dương: Lợi nhuận (Doanh thu - Chi phí)
        - 🟣 Cột tím: Lợi nhuận ròng (Lợi nhuận - Thuế)
        """)

def show_pivot_table(df):
    st.subheader('Bảng phân tích chi tiết')
    selected_period = st.selectbox('Chọn khoảng thời gian phân tích', [7, 14, 30, 90, 180], key='pivot_period_select')

    # Chuyển đổi 'day' sang datetime nếu chưa phải
    df['day'] = pd.to_datetime(df['day'])
    
    # Tính toán khoảng thời gian
    end_date = df['day'].max()
    start_date = end_date - pd.Timedelta(days=selected_period)
    previous_start_date = start_date - pd.Timedelta(days=selected_period)

    pivot_data = []
    for ad_name in df['ad_name'].unique():
        ad_df = df[df['ad_name'] == ad_name]
        
        # Lọc dữ liệu cho khoảng thời gian hiện tại và trước đó
        current_period_df = ad_df[(ad_df['day'] > start_date) & (ad_df['day'] <= end_date)]
        previous_period_df = ad_df[(ad_df['day'] > previous_start_date) & (ad_df['day'] <= start_date)]
        
        # Tính toán các chỉ số cho khoảng thời gian hiện tại
        current_metrics = {
            'spend': current_period_df['spend'].sum(),
            'revenue': current_period_df['revenue'].sum(),
            'profit': current_period_df['profit'].sum(),
            'net_profit': current_period_df['net_profit'].sum()
        }
        
        # Tính toán các chỉ số cho khoảng thời gian trước đó
        previous_metrics = {
            'spend': previous_period_df['spend'].sum(),
            'revenue': previous_period_df['revenue'].sum(),
            'profit': previous_period_df['profit'].sum(),
            'net_profit': previous_period_df['net_profit'].sum()
        }
        
        # Tính toán tăng trưởng
        row = {
            'ad_name': ad_name,
            'spend': current_metrics['spend'],
            'spend_growth': calculate_growth(current_metrics['spend'], previous_metrics['spend']),
            'revenue': current_metrics['revenue'],
            'revenue_growth': calculate_growth(current_metrics['revenue'], previous_metrics['revenue']),
            'profit': current_metrics['profit'],
            'profit_growth': calculate_growth(current_metrics['profit'], previous_metrics['profit']),
            'net_profit': current_metrics['net_profit'],
            'net_profit_growth': calculate_growth(current_metrics['net_profit'], previous_metrics['net_profit'])
        }
        
        pivot_data.append(row)

    pivot_df = pd.DataFrame(pivot_data)

    if pivot_df.empty:
        st.warning("Không có dữ liệu để hiển thị bảng phân tích")
        return

    # Đổi tên cột sang tiếng Việt
    column_names = {
        'ad_name': 'Tên quảng cáo',
        'spend': f'Chi phí trong {selected_period} ngày qua',
        'spend_growth': 'Tăng trưởng chi phí (%)',
        'revenue': f'Doanh thu trong {selected_period} ngày qua',
        'revenue_growth': 'Tăng trưởng doanh thu (%)',
        'profit': f'Lợi nhuận trong {selected_period} ngày qua',
        'profit_growth': 'Tăng trưởng lợi nhuận (%)',
        'net_profit': f'Lợi nhuận ròng trong {selected_period} ngày qua',
        'net_profit_growth': 'Tăng trưởng lợi nhuận ròng (%)'
    }
    pivot_df.columns = [column_names.get(col, col) for col in pivot_df.columns]

    # Định dạng các cột
    formatted_columns = {}
    for col in pivot_df.columns:
        if col != 'Tên quảng cáo':
            if 'growth' in col.lower() or 'tăng trưởng' in col.lower():
                formatted_columns[col] = '{:+.2f}%'
            else:
                formatted_columns[col] = '{:,.0f} đ'

    st.dataframe(pivot_df.style.format(formatted_columns))

    # Thêm giải thích
    st.markdown(f"""
    ### Hướng dẫn đọc bảng phân tích:
    
    - **Chi phí trong {selected_period} ngày qua**: Tổng chi phí quảng cáo trong khoảng thời gian đã chọn
    - **Doanh thu trong {selected_period} ngày qua**: Tổng doanh thu từ quảng cáo
    - **Lợi nhuận trong {selected_period} ngày qua**: Doanh thu trừ chi phí
    - **Lợi nhuận ròng trong {selected_period} ngày qua**: Lợi nhuận sau khi trừ thuế và các chi phí khác
    - **Các chỉ số tăng trưởng**: So sánh với {selected_period} ngày trước đó
        - Giá trị dương (+): Tăng trưởng tốt
        - Giá trị âm (-): Cần cải thiện
    """)

    # Thêm biểu đồ tăng trưởng
    growth_columns = [col for col in pivot_df.columns if 'Tăng trưởng' in col]
    if not growth_columns:
        st.warning("Không có dữ liệu tăng trưởng để hiển thị biểu đồ")
        return
        
    growth_data = pivot_df[['Tên quảng cáo'] + growth_columns]

    fig = px.bar(
        growth_data.melt(
            id_vars=['Tên quảng cáo'],
            var_name='Chỉ số',
            value_name='Tăng trưởng (%)'
        ),
        x='Tên quảng cáo',
        y='Tăng trưởng (%)',
        color='Chỉ số',
        title=f'Biểu đồ tăng trưởng trong {selected_period} ngày qua (so với {selected_period} ngày trước đó)',
        barmode='group'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def format_number(number):
    if number >= 1000000:
        return f"{number/1000000:.1f}M"
    elif number >= 1000:
        return f"{number/1000:.1f}k"
    else:
        return f"{number:.0f}"


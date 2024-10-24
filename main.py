import streamlit as st
from database import get_data
from overview_report import show_overview_report
from ad_name_report import show_ad_name_report
from data_entry import show_data_entry

st.title('Báo cáo Quảng cáo')

# Lấy dữ liệu
df = get_data()

# Tạo các tab
tab1, tab2, tab3 = st.tabs(["Báo cáo tổng quan", "Báo cáo theo AD_NAME", "Nhập dữ liệu"])

with tab1:
    show_overview_report(df)

with tab2:
    show_ad_name_report(df)

with tab3:
    show_data_entry()

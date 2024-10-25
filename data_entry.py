import streamlit as st
import pandas as pd
from database import save_spend_data, save_revenue_data, get_data, remove_spend_data, remove_revenue_data
from datetime import datetime
from guides import DATA_ENTRY_GUIDE

def show_data_entry():
    st.header('Nhập dữ liệu')
    
    # Thêm checkbox cho hướng dẫn sử dụng
    if st.checkbox('Hiển thị hướng dẫn sử dụng', False, key='data_entry_guide'):
        st.info(DATA_ENTRY_GUIDE)
    
    table_choice = st.radio("Chọn bảng để nhập dữ liệu", ("Chi phí (Spend)", "Doanh thu (Revenue)"))
    
    if table_choice == "Chi phí (Spend)":
        show_spend_form()
    else:
        show_revenue_form()

    show_current_data()

def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def show_spend_form():
    st.subheader("Nhập dữ liệu chi phí")
    
    st.info("""
    Hướng dẫn nhập liệu:
    - Ngày: Nhập theo định dạng yyyy-mm-dd (ví dụ: 2024-02-01)
    - AD_NAME: Tên quảng cáo
    - Chi phí: Số tiền chi cho quảng cáo
    """)
    
    # Tạo DataFrame ban đầu
    if 'spend_data' not in st.session_state:
        st.session_state.spend_data = pd.DataFrame(
            columns=["day", "ad_name", "spend"],
            data=[["", "", 0.0]]
        )
    
    # Hiển thị data editor
    edited_df = st.data_editor(
        st.session_state.spend_data,
        num_rows="dynamic",
        column_config={
            "day": st.column_config.TextColumn("Ngày (yyyy-mm-dd)"),
            "ad_name": st.column_config.TextColumn("AD_NAME"),
            "spend": st.column_config.NumberColumn("Chi phí", min_value=0.0, format="%.2f")
        }
    )
    
    # Cập nhật DataFrame trong session state
    st.session_state.spend_data = edited_df
    
    if st.button("Lưu dữ liệu chi phí"):
        invalid_dates = []
        empty_fields = []
        for index, row in edited_df.iterrows():
            if not row["day"] or not row["ad_name"] or not row["spend"]:
                empty_fields.append(index + 1)
            elif not is_valid_date(row["day"]):
                invalid_dates.append(index + 1)
        
        if empty_fields:
            st.error(f"Các trường không được để trống ở (các) dòng: {', '.join(map(str, empty_fields))}.")
        elif invalid_dates:
            st.error(f"Ngày không hợp lệ ở (các) dòng: {', '.join(map(str, invalid_dates))}. Vui lòng nhập ngày theo định dạng yyyy-mm-dd.")
        else:
            for _, row in edited_df.iterrows():
                if row["day"] and row["ad_name"] and row["spend"]:
                    date = datetime.strptime(row["day"], '%Y-%m-%d')
                    save_spend_data(date, row["ad_name"], row["spend"])
            st.success("Đã lưu dữ liệu chi phí thành công!")

def show_revenue_form():
    st.subheader("Nhập dữ liệu doanh thu")
    
    st.info("""
    Hướng dẫn nhập liệu:
    - Ngày: Nhập theo định dạng yyyy-mm-dd (ví dụ: 2024-02-01)
    - SUBID1, SUBID2: Thông tin định danh quảng cáo (bắt buộc)
    - SUBID3: Thông tin bổ sung (không bắt buộc)
    - Doanh thu: Số tiền thu được
    - AD_NAME sẽ tự động tạo từ SUBID1 và SUBID2 khi lưu dữ liệu
    """)
    
    # Tạo DataFrame ban đầu
    if 'revenue_data' not in st.session_state:
        st.session_state.revenue_data = pd.DataFrame(
            columns=["day", "subid1", "subid2", "subid3", "revenue", "ad_name"],
            data=[["", "", "", "", 0.0, ""]]
        )
    
    # Hiển thị data editor
    edited_df = st.data_editor(
        st.session_state.revenue_data,
        num_rows="dynamic",
        column_config={
            "day": st.column_config.TextColumn("Ngày (yyyy-mm-dd)"),
            "subid1": st.column_config.TextColumn("SUBID1"),
            "subid2": st.column_config.TextColumn("SUBID2"), 
            "subid3": st.column_config.TextColumn("SUBID3"),
            "revenue": st.column_config.NumberColumn("Doanh thu", min_value=0.0, format="%.2f"),
            "ad_name": st.column_config.TextColumn("AD_NAME", disabled=True)
        }
    )
    
    # Cập nhật DataFrame trong session state
    st.session_state.revenue_data = edited_df
    
    if st.button("Lưu dữ liệu doanh thu"):
        invalid_dates = []
        empty_fields = []
        for index, row in edited_df.iterrows():
            if not all([row["day"], row["subid1"], row["subid2"], row["revenue"]]):
                empty_fields.append(index + 1)
            elif not is_valid_date(row["day"]):
                invalid_dates.append(index + 1)
        
        if empty_fields:
            st.error(f"Các trường bắt buộc (Ngày, SUBID1, SUBID2, Doanh thu) không được để trống ở (các) dòng: {', '.join(map(str, empty_fields))}.")
        elif invalid_dates:
            st.error(f"Ngày không hợp lệ ở (các) dòng: {', '.join(map(str, invalid_dates))}. Vui lòng nhập ngày theo định dạng yyyy-mm-dd.")
        else:
            for _, row in edited_df.iterrows():
                if all([row["day"], row["subid1"], row["subid2"], row["revenue"]]):
                    # Tạo ad_name khi lưu dữ liệu
                    ad_name = f"{row['subid1']}-{row['subid2']}"
                    date = datetime.strptime(row["day"], '%Y-%m-%d')
                    save_revenue_data(date, row["subid1"], row["subid2"], row["subid3"], row["revenue"], ad_name)
            st.success("Đã lưu dữ liệu doanh thu thành công!")

def show_current_data():
    st.subheader("Dữ liệu hiện tại")
    
    days = st.number_input("Số ngày muốn hiển thị", min_value=1, value=30, step=1)
    
    if st.button("Tải lại dữ liệu"):
        st.cache_data.clear()
        st.success(f"Đã tải lại dữ liệu {days} ngày gần nhất thành công!")
    
    df = get_data(days=days)  # Lấy dữ liệu theo số ngày được chọn
    st.dataframe(df)

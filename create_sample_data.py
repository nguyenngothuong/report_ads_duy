import pandas as pd
from datetime import datetime, timedelta
import random
from supabase import create_client, Client
import streamlit as st
from postgrest.exceptions import APIError

supabase_url = st.secrets["supabase"]["url"]
supabase_key = st.secrets["supabase"]["key"]

supabase: Client = create_client(supabase_url, supabase_key)

# Tạo dữ liệu mẫu
start_date = datetime(2024, 1, 1)
end_date = datetime.now()
date_range = pd.date_range(start=start_date, end=end_date)

ad_names = [
    "BeyeuCM-3Dodungchobe2806",
    "BeyeuCM-4Dodungchobe2806",
    "BeyeuCM-5Dodungchobe2806"
]

spend_data = []
revenue_data = []

current_time = datetime.now().isoformat()

for date in date_range:
    for ad_name in ad_names:
        spend = round(random.uniform(20000, 40000), 2)
        revenue = round(random.uniform(50000, 100000), 2)
        subid1, subid2 = ad_name.split('-')[:2]
        subid3 = "T" + str(random.randint(1, 12)) if random.random() > 0.5 else ""
        
        spend_data.append({
            "day": date.strftime("%d/%m/%y"),
            "ad_name": ad_name,
            "spend": spend,
            "created_at": current_time,
            "updated_at": current_time
        })
        
        revenue_data.append({
            "day": date.strftime("%d/%m/%y"),
            "subid1": subid1,
            "subid2": subid2,
            "subid3": subid3,
            "revenue": revenue,
            "ad_name": ad_name,
            "created_at": current_time,
            "updated_at": current_time
        })

try:
    # Xóa dữ liệu cũ
    supabase.table('spend_table').delete().neq('id', 0).execute()
    supabase.table('revenue_table').delete().neq('id', 0).execute()

    # Chèn dữ liệu mới vào bảng
    for data in spend_data:
        supabase.table('spend_table').insert(data).execute()

    for data in revenue_data:
        supabase.table('revenue_table').insert(data).execute()

    print("Đã tạo và cập nhật dữ liệu mẫu thành công!")

except APIError as e:
    print(f"Lỗi API: {e}")
    if "relation" in str(e) and "does not exist" in str(e):
        print("Bảng không tồn tại. Vui lòng tạo bảng trong Supabase trước khi chạy script này.")
    else:
        print("Vui lòng kiểm tra lại cấu hình kết nối Supabase và quyền truy cập của bạn.")
except Exception as e:
    print(f"Lỗi không xác định: {e}")

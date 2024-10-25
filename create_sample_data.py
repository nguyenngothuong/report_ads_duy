import pandas as pd
from datetime import datetime, timedelta
import random
from supabase import create_client, Client
import streamlit as st
from postgrest.exceptions import APIError

supabase_url = st.secrets["supabase"]["url"]
supabase_key = st.secrets["supabase"]["key"]

supabase: Client = create_client(supabase_url, supabase_key)

# Tạo danh sách SUBID1 và SUBID2 mẫu
subid1_list = ["BeyeuCM", "ShopeeVN", "LazadaVN", "TikiVN", "SendoVN", "FptShop", "TheGioiDiDong", 
               "NguyenKim", "Fahasa", "Concung", "Bibomart", "Vinmart", "BachhoaXanh"]

subid2_list = ["DodungChoBe", "DoChoiTreEm", "QuanAoTreEm", "GiayDepTreEm", "BimTa", "SuaBot",
               "VitaminChoBe", "DoGiaDung", "MyPham", "ThucPhamChucNang", "DienThoai", "MayTinhBang",
               "LaptopMayTinh", "TuiXach", "GiayDep", "QuanAo"]

# Tạo danh sách AD_NAME bằng cách kết hợp ngẫu nhiên
ad_names = []
for _ in range(50):  # Tạo 50 AD_NAME khác nhau
    subid1 = random.choice(subid1_list)
    subid2 = random.choice(subid2_list)
    ad_name = f"{subid1}_{subid2}"
    if ad_name not in ad_names:
        ad_names.append(ad_name)

# Tạo dữ liệu mẫu
start_date = datetime(2024, 1, 1)
end_date = datetime.now()
date_range = pd.date_range(start=start_date, end=end_date)

spend_data = []
revenue_data = []

current_time = datetime.now().isoformat()

# Tạo khoảng 10k dòng dữ liệu cho mỗi bảng
target_rows = 10000
daily_entries = target_rows // len(date_range)

for date in date_range:
    # Chọn ngẫu nhiên một số AD_NAME cho mỗi ngày
    daily_ad_names = random.sample(ad_names, min(daily_entries, len(ad_names)))
    
    for ad_name in daily_ad_names:
        # Tạo dữ liệu chi phí với độ biến thiên lớn hơn
        spend = round(random.uniform(50000, 2000000), 2)
        
        # Tạo doanh thu dựa trên chi phí với tỷ lệ ROI ngẫu nhiên
        roi = random.uniform(0.5, 3.0)  # ROI từ 50% đến 300%
        revenue = round(spend * roi, 2)
        
        subid1, subid2 = ad_name.split('_')
        subid3 = f"T{random.randint(1,12)}" if random.random() > 0.5 else ""
        
        spend_data.append({
            "day": date.strftime("%Y-%m-%d"),
            "ad_name": ad_name,
            "spend": spend,
            "created_at": current_time,
            "updated_at": current_time
        })
        
        revenue_data.append({
            "day": date.strftime("%Y-%m-%d"),
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
    batch_size = 500
    for i in range(0, len(spend_data), batch_size):
        batch = spend_data[i:i + batch_size]
        supabase.table('spend_table').insert(batch).execute()

    for i in range(0, len(revenue_data), batch_size):
        batch = revenue_data[i:i + batch_size]
        supabase.table('revenue_table').insert(batch).execute()

    print(f"Đã tạo và cập nhật thành công {len(spend_data)} dòng dữ liệu cho mỗi bảng!")

except APIError as e:
    print(f"Lỗi API: {e}")
    if "relation" in str(e) and "does not exist" in str(e):
        print("Bảng không tồn tại. Vui lòng tạo bảng trong Supabase trước khi chạy script này.")
    else:
        print("Vui lòng kiểm tra lại cấu hình kết nối Supabase và quyền truy cập của bạn.")
except Exception as e:
    print(f"Lỗi không xác định: {e}")

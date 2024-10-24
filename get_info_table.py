import streamlit as st
from supabase import create_client, Client
import pandas as pd

# Đọc thông tin cấu hình từ secret.toml
supabase_url = st.secrets["supabase"]["url"]
supabase_key = st.secrets["supabase"]["key"]

# Kết nối đến Supabase
supabase: Client = create_client(supabase_url, supabase_key)

def get_table_info(table_name):
    # Lấy thông tin về cấu trúc bảng
    response = supabase.table(table_name).select('*').limit(1).execute()
    
    info = f"Các cột và kiểu dữ liệu trong bảng {table_name}:\n"
    if len(response.data) > 0:
        df = pd.DataFrame(response.data)
        for col, dtype in df.dtypes.items():
            info += f"- {col}: {dtype}\n"
    else:
        info += f"Không thể lấy thông tin về bảng {table_name}. Bảng có thể trống hoặc không tồn tại.\n"
    info += "\n"
    return info

# Lấy thông tin về các bảng
spend_info = get_table_info('spend_table')
revenue_info = get_table_info('revenue_table')

# Lấy một số dòng dữ liệu mẫu từ mỗi bảng
def get_sample_data(table_name, limit=5):
    response = supabase.table(table_name).select('*').limit(limit).execute()
    sample_data = f"Dữ liệu mẫu từ bảng {table_name}:\n"
    df = pd.DataFrame(response.data)
    sample_data += df.to_string() + "\n\n"
    return sample_data

spend_sample = get_sample_data('spend_table')
revenue_sample = get_sample_data('revenue_table')

# Hiển thị thông tin chi tiết về cấu trúc bảng
def get_detailed_table_info(table_name):
    response = supabase.table(table_name).select('*').limit(1).execute()
    
    detailed_info = f"Thông tin chi tiết về cấu trúc bảng {table_name}:\n"
    if response.data:
        df = pd.DataFrame(response.data)
        for column, dtype in df.dtypes.items():
            detailed_info += f"- {column}:\n"
            detailed_info += f"  Kiểu dữ liệu: {dtype}\n"
            detailed_info += f"  Cho phép NULL: {'Có' if df[column].isnull().any() else 'Không'}\n"
    else:
        detailed_info += f"Không thể lấy thông tin chi tiết về bảng {table_name}.\n"
    detailed_info += "\n"
    return detailed_info

spend_detailed = get_detailed_table_info('spend_table')
revenue_detailed = get_detailed_table_info('revenue_table')

# Lưu thông tin vào file txt
with open('table_info.txt', 'w', encoding='utf-8') as f:
    f.write(spend_info)
    f.write(revenue_info)
    f.write(spend_sample)
    f.write(revenue_sample)
    f.write(spend_detailed)
    f.write(revenue_detailed)

print("Đã lưu thông tin vào file table_info.txt")

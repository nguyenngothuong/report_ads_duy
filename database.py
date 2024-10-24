import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime

# Đọc thông tin cấu hình từ secret.toml
supabase_url = st.secrets["supabase"]["url"]
supabase_key = st.secrets["supabase"]["key"]

@st.cache_resource
def get_supabase_client() -> Client:
    return create_client(supabase_url, supabase_key)

@st.cache_data
def get_data():
    supabase = get_supabase_client()
    
    spend_response = supabase.table('spend_table').select('*').execute()
    revenue_response = supabase.table('revenue_table').select('*').execute()
    
    spend_df = pd.DataFrame(spend_response.data)
    revenue_df = pd.DataFrame(revenue_response.data)
    
    df = pd.merge(spend_df, revenue_df, on=['day', 'ad_name'], how='outer')
    df['day'] = pd.to_datetime(df['day'], format='%d/%m/%y')
    df['spend'] = pd.to_numeric(df['spend'], errors='coerce')
    df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
    df['profit'] = df['revenue'] - df['spend']
    df['tax'] = df['revenue'] * 0.07
    df['net_profit'] = df['profit'] - df['tax']
    df = df.sort_values('day', ascending=False)
    return df

def save_spend_data(date, ad_name, spend):
    supabase = get_supabase_client()
    supabase.table('spend_table').upsert({
        'day': date,
        'ad_name': ad_name,
        'spend': spend,
        'updated_at': datetime.now().isoformat()
    }).execute()

def save_revenue_data(date, subid1, subid2, subid3, revenue, ad_name):
    supabase = get_supabase_client()
    supabase.table('revenue_table').upsert({
        'day': date,
        'subid1': subid1,
        'subid2': subid2,
        'subid3': subid3,
        'revenue': revenue,
        'ad_name': ad_name,
        'updated_at': datetime.now().isoformat()
    }).execute()

def remove_spend_data(date, ad_name):
    supabase = get_supabase_client()
    supabase.table('spend_table').delete().eq('day', date).eq('ad_name', ad_name).execute()

def remove_revenue_data(date, ad_name):
    supabase = get_supabase_client()
    supabase.table('revenue_table').delete().eq('day', date).eq('ad_name', ad_name).execute()

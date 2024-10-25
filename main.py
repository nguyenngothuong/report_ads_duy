import streamlit as st
from database import get_data
from overview_report import show_overview_report
from ad_name_report import show_ad_name_report
from data_entry import show_data_entry
from guides import UPDATE_INFO, VERSION_HISTORY, FUTURE_PLANS, CONTACT_INFO

st.title('Báo cáo Quảng cáo')

# Tạo các tab
tab1, tab2, tab3, tab4 = st.tabs(["Báo cáo tổng quan", "Báo cáo theo AD_NAME", "Nhập dữ liệu", "Thông báo & Cập nhật"])

# Lấy dữ liệu
df = get_data()

with tab1:
    show_overview_report(df)

with tab2:
    show_ad_name_report(df)

with tab3:
    show_data_entry()

with tab4:
    st.header("Thông báo & Cập nhật")
    
    # Hiển thị phiên bản hiện tại
    st.subheader("📱 Phiên bản hiện tại: v1.0.0")
    
    # Thông báo quan trọng
    st.info(UPDATE_INFO)
    
    # Lịch sử cập nhật
    st.subheader("📝 Lịch sử cập nhật")
    
    for version, info in VERSION_HISTORY.items():
        with st.expander(f"{version} ({info['date']}){' - Phiên bản hiện tại' if version == 'v1.0.0' else ''}"):
            for change in info['changes']:
                st.write(f"- {change}")
    
    # Kế hoạch phát triển
    st.subheader("🚀 Kế hoạch phát triển")
    st.write(FUTURE_PLANS)
    
    # Phản hồi và góp ý
    st.subheader("💡 Góp ý phát triển")
    
    feedback = st.text_area("Nhập góp ý của bạn:", 
                           placeholder="Nhập góp ý hoặc báo lỗi tại đây...")
    
    if st.button("Gửi góp ý"):
        if feedback:
            st.success("Cảm ơn bạn đã gửi góp ý! Chúng tôi sẽ xem xét và phản hồi sớm nhất.")
        else:
            st.warning("Vui lòng nhập nội dung góp ý trước khi gửi.")
    
    # Thông tin liên hệ
    st.markdown(CONTACT_INFO)

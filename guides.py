# Hướng dẫn cho trang Overview
OVERVIEW_GUIDE = """
### 📌 Hướng dẫn sử dụng báo cáo tổng quan

1. **Chọn khoảng thời gian:**
   - Sử dụng dropdown để chọn khoảng thời gian phân tích
   - Có các tùy chọn: 7 ngày, 30 ngày, 6 tháng, 1 năm
   - Chọn "Tùy chỉnh" để tự chọn khoảng thời gian mong muốn

2. **Đọc hiểu các chỉ số tổng quan:**
   - 🔴 Tổng chi phí: Tổng số tiền đã chi cho quảng cáo
   - 🟢 Tổng doanh thu: Tổng số tiền thu được
   - 🔵 Tổng lợi nhuận: Doanh thu trừ chi phí
   - 🟣 Lợi nhuận ròng: Lợi nhuận sau khi trừ thuế (7%)
"""

# Hướng dẫn cho trang AD_NAME
AD_NAME_GUIDE = """
### 📌 Hướng dẫn sử dụng báo cáo theo AD_NAME

1. **Bộ lọc chung:**
   - Sử dụng bộ lọc SUBID1, SUBID2, SUBID3 để lọc dữ liệu theo từng cấp độ
   - Chọn "Tất cả" để xem toàn bộ dữ liệu

2. **Biểu đồ tổng quan:**
   - Chọn bộ lọc để xem top AD_NAME theo các tiêu chí khác nhau
   - Sử dụng thanh trượt để lọc theo khoảng Revenue
   - Tìm kiếm AD_NAME cụ thể bằng ô tìm kiếm
"""

# Hướng dẫn cho trang Data Entry
DATA_ENTRY_GUIDE = """
### 📌 Hướng dẫn nhập liệu

1. **Chọn loại dữ liệu:**
   - Chi phí (Spend): Nhập dữ liệu chi phí quảng cáo
   - Doanh thu (Revenue): Nhập dữ liệu doanh thu

2. **Nhập dữ liệu chi phí:**
   - Ngày (yyyy-mm-dd): Ví dụ 2024-02-01
   - AD_NAME: Tên quảng cáo (phải khớp với định dạng)
   - Chi phí: Số tiền chi cho quảng cáo
"""

# Hướng dẫn đọc biểu đồ và chỉ số
CHART_GUIDE = """
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
"""

# Thông báo và cập nhật
UPDATE_INFO = """
### 📢 Thông báo quan trọng

- **24/10/2024**: Hệ thống đã chuyển sang sử dụng Supabase để lưu trữ dữ liệu
"""

VERSION_HISTORY = {
    "v1.0.1": {
        "date": "25/10/2024",
        "changes": [
            "Sửa lỗi hiển thị dữ liệu trên biểu đồ tăng trưởng",
            "Thay đổi cấu trúc biểu đồ - theo yc của anh Duy",
            "Thêm guides hướng dẫn sử dụng",
            "Bổ sung tính năng lọc dữ liệu theo ngày, AD_NAME và các chỉ số",
        ]
    },
    "v1.0.0": {
        "date": "24/10/2024",
        "changes": [
            "Chuyển đổi cơ sở dữ liệu từ SQLite sang Supabase",
            "Thêm hướng dẫn sử dụng chi tiết cho từng trang",
            "Cải thiện giao diện biểu đồ và hiển thị số liệu",
            "Thêm tính năng lọc theo SUBID1, SUBID2, SUBID3",
            "Tối ưu hóa hiệu suất tải dữ liệu"
        ]
    },
    "v0.9.0": {
        "date": "20/10/2024",
        "changes": [
            "Thêm tính năng phân tích chi tiết theo AD_NAME",
            "Cải thiện giao diện nhập liệu",
            "Thêm biểu đồ tăng trưởng",
            "Sửa lỗi hiển thị ngày tháng"
        ]
    }
}

FUTURE_PLANS = """
### Sắp ra mắt trong v1.1.0:
- Tích hợp đăng nhập và phân quyền người dùng
- Tính năng xuất báo cáo PDF
- Dashboard tùy chỉnh
- Cảnh báo thông minh khi có biến động bất thường
- Tự động đồng bộ dữ liệu từ các nền tảng quảng cáo

### Đang nghiên cứu:
- Tích hợp AI để phân tích và đề xuất tối ưu
- Ứng dụng mobile
- API cho bên thứ ba
"""

CONTACT_INFO = """
---
### 📞 Thông tin hỗ trợ
- **Email**: work@nguyenngothuong.com
- **Hotline**: 0816226086
- **Giờ làm việc**: 9:00 - 17:30 (Thứ 2 - Thứ 6)
"""

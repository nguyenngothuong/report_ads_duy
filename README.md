# Ứng dụng Báo cáo Quảng cáo

Ứng dụng này được xây dựng để theo dõi và phân tích hiệu quả của các chiến dịch quảng cáo, sử dụng Streamlit và Supabase.

## Tính năng

- Báo cáo tổng quan về chi phí, doanh thu, lợi nhuận và lợi nhuận ròng
- Báo cáo chi tiết theo từng AD_NAME
- Biểu đồ trực quan hóa dữ liệu theo thời gian và AD_NAME
- Nhập và quản lý dữ liệu chi phí và doanh thu

## Cài đặt

1. Clone repository này:
   ```
   git clone <url-của-repository>
   ```

2. Cài đặt các thư viện cần thiết:
   ```
   pip install -r requirements.txt
   ```

3. Tạo file `secret.toml` trong thư mục `.streamlit` và thêm thông tin kết nối Supabase:
   ```toml
   [supabase]
   url = "YOUR_SUPABASE_PROJECT_URL"
   key = "YOUR_SUPABASE_API_KEY"
   ```

## Sử dụng

1. Chạy ứng dụng Streamlit:
   ```
   streamlit run main.py
   ```

2. Truy cập ứng dụng qua trình duyệt web theo URL được cung cấp.

## Cấu trúc dự án

- `main.py`: File chính để chạy ứng dụng Streamlit
- `database.py`: Xử lý kết nối và truy vấn cơ sở dữ liệu
- `overview_report.py`: Hiển thị báo cáo tổng quan
- `ad_name_report.py`: Hiển thị báo cáo theo AD_NAME
- `data_entry.py`: Xử lý nhập liệu
- `utils.py`: Chứa các hàm tiện ích
- `create_sample_data.py`: Tạo dữ liệu mẫu cho ứng dụng

## Đóng góp

Mọi đóng góp đều được hoan nghênh. Vui lòng mở một issue hoặc tạo pull request để đóng góp.

## Giấy phép

[MIT License](https://opensource.org/licenses/MIT)

# Hướng dẫn Test API Client

## Cài đặt môi trường

1. Cài đặt các thư viện cần thiết:
```bash
pip install requests
```

2. Đảm bảo có các file sau trong thư mục `src`:
- `api_client.py`
- `test_api_client.py`

## Chạy Test

1. Chạy toàn bộ test:
```bash
# Từ thư mục gốc của project
python -m unittest src/test_api_client.py

# Hoặc từ thư mục src
cd src
python -m unittest test_api_client.py
```

2. Chạy test cụ thể:
```bash
python -m unittest src.test_api_client.TestLangFlowClient.test_call_api_success
```

## Các Test Case

1. **test_call_api_success**
   - Kiểm tra gọi API thành công
   - Xác minh response là dictionary
   - Kiểm tra có key "outputs" trong response

2. **test_get_response_text_success**
   - Kiểm tra lấy text từ response
   - Xác minh response text là string
   - Kiểm tra response text không rỗng

3. **test_invalid_query**
   - Kiểm tra xử lý query rỗng
   - Xác minh trả về dictionary rỗng

4. **test_error_handling**
   - Kiểm tra xử lý lỗi với API key không hợp lệ
   - Xác minh trả về dictionary rỗng

## Debug Test

1. Thêm print statement trong test:
```python
print(f"Response: {response}")
```

2. Chạy test với verbose:
```bash
python -m unittest -v src/test_api_client.py
```

## Lưu ý

1. Test cần kết nối internet
2. API key phải hợp lệ
3. Có thể cần điều chỉnh test query tùy theo nội dung tài liệu
4. Nếu gặp lỗi import, đảm bảo đang chạy từ thư mục gốc của project 
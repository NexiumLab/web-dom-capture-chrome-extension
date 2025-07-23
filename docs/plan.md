# Kế hoạch phát triển Extension "DOM Grabber" (Python Server)

*Mod by Asi on 2024-07-25--17:30-PM*

## 1. Tổng quan

- **Mục tiêu:** Tạo một hệ thống gồm Chrome Extension và một server Python local. Extension sẽ gửi DOM của trang hiện tại đến server, và server sẽ lưu nó vào một thư mục trên máy.
- **Kiến trúc:**
  - **Chrome Extension (Frontend):** Giao diện popup đơn giản, gửi yêu cầu lấy DOM.
  - **Python Server (Backend):** Server Flask nhận dữ liệu DOM và ghi ra file.

## 2. Phân rã công việc

### Đã hoàn thành

1.  **[COMPLETED]** Thiết lập cấu trúc thư mục `py-server` và `captured_doms`.
2.  **[COMPLETED]** Viết server Flask đơn giản (`py-server/main.py`) để nhận và lưu DOM.
3.  **[COMPLETED]** Cập nhật `manifest.json` để cho phép giao tiếp với `http://127.0.0.1:51234/`.
4.  **[COMPLETED]** Viết lại `background.js` để lấy DOM và gửi đến server Python.
5.  **[COMPLETED]** Đơn giản hóa `popup.html` và `popup.js` thành một nút bấm duy nhất.

### Việc cần làm

6.  **[PENDING]** Viết tài liệu hướng dẫn cách chạy server Python và cài đặt extension.
7.  **[PENDING]** Cải thiện server Python (ví dụ: thêm logging, xử lý lỗi tốt hơn).
8.  **[PENDING]** Thêm cơ chế thông báo thành công/thất bại trên giao diện extension. 
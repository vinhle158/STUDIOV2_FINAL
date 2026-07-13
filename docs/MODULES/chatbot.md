# Module Chatbot Quản lý Nội bộ (Rule-based NLP)

## 1. Giới thiệu
Chatbot cung cấp chức năng tra cứu thông tin nhanh cho nhân viên/quản lý thông qua giao tiếp ngôn ngữ tự nhiên. Chức năng này được xây dựng dạng Rule-based (Quy tắc và Mẫu câu), không phụ thuộc vào nền tảng LLM ngoại vi (như ChatGPT/Gemini) nhằm bảo mật dữ liệu tuyệt đối và đạt thời gian phản hồi tức thì.

## 2. Luồng xử lý Pipeline
Mọi truy vấn từ Frontend được xử lý theo trình tự:
1. **Normalizer**: Tiền xử lý, chuẩn hóa tiếng Việt, dấu, viết tắt, con số.
2. **Tokenizer / Entity Extractor**: Trích xuất tham số cụ thể (ví dụ: tên khách hàng, số điện thoại, thời gian "tuần này", "tháng 6").
3. **Fuzzy Matching**: Dùng `fuse.js` ánh xạ tên khách hàng/đơn hàng nhận diện được vào dữ liệu thực trong PostgreSQL (với threshold độ tương đồng).
4. **Intent Classifier / Business Dictionary Lookup**: Phân loại ý định của câu hỏi thông qua NLP.js manager đã được huấn luyện sẵn hoặc fallback regex (VD: tra cứu lịch chụp, cảnh báo vận hành, công việc chưa xong).
5. **Query Builder**: Chuyển Ý định (Intent) và Tham số (Entities) thành truy vấn Prisma Prisma-safe tới CSDL.
6. **Response Templating**: Điền kết quả thực thi vào template ngôn ngữ tự nhiên chuẩn bị sẵn (ví dụ: "Doanh thu tháng X là Y VND") để trả về Client.

## 3. Các Tính năng Tích hợp (Intents)
- `get_business_overview`: Thống kê tổng quan khách hàng, đơn hàng, doanh thu.
- `search_customers`: Tìm khách hàng theo tên/sđt/email.
- `search_orders`: Tra cứu trạng thái đơn hàng.
- `search_tasks`: Quản lý các tác vụ, trạng thái trễ hạn.
- `get_schedule_range`: Tra cứu lịch chụp ảnh trong một khoảng thời gian.
- `get_operational_alerts`: Truy xuất cảnh báo hệ thống (thiếu cọc, đơn trống, nhiệm vụ quá hạn).
- `get_staff_workload`: Xem phân bổ khối lượng công việc của nhân sự.

## 4. Tệp tin cốt lõi
- `src/lib/chatbot/nlp.ts`, `entityExtractor.ts`, `fuzzyMatch.ts`, `queryBuilder.ts`: Cụm module NLP.
- `server.ts`: Tích hợp fallback intent routing và streaming SSE (Server-Sent Events) để trả dữ liệu theo thời gian thực tới Client.

# Module: Chat & Thông báo (Chat & Notifications)

## Tổng quan
Cung cấp khả năng giao tiếp nội bộ giữa các nhân viên trong Studio và nhận các thông báo hệ thống tự động (có Task mới, có tin nhắn mới).

## Luồng hoạt động
1. **Chat Nội bộ**: Người dùng mở `Chat.tsx` để nhắn tin trong nhóm chung hoặc nhắn tin riêng 1-1. Hiện tại sử dụng HTTP Polling và đang có kế hoạch chuyển sang WebSocket.
2. **Trợ lý Ảo (Chatbot)**: Giao diện `ChatWidget.tsx` tích hợp Chatbot NLP dựa trên quy tắc (rule-based) hỗ trợ tư vấn và trả lời nhanh.
3. **Thông báo**: `Notifications.tsx` hiển thị các thông báo được tạo ra từ các action hệ thống (ví dụ: giao task mới).

## Thành phần Frontend
- `src/components/Chat.tsx`: Khung chat nội bộ.
- `src/components/ChatWidget.tsx`: Khung chat mini cho Chatbot/hỗ trợ.
- `src/components/Notifications.tsx`: Menu hiển thị thông báo.

## Cấu trúc Dữ liệu (Database)
- Bảng `Message`: ID, SenderID, ReceiverID/RoomID, Content, Timestamp...
- Bảng `Notification`: ID, UserID, Type, Content, IsRead...

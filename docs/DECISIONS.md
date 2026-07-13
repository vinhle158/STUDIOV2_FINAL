# Quyết định Thiết kế (Design Decisions)

1. **Chuyển đổi Database sang 100% PostgreSQL**: Loại bỏ hoàn toàn cơ chế dual-write (đồng bộ giữa `db.json` và PostgreSQL) sang "PostgreSQL-only Active Cache mode" để giải quyết rủi ro ghi đè dữ liệu và cải thiện hiệu năng (Commit: 5c47e6927...).
2. **Chatbot Nội bộ Không Dùng LLM (Rule-based NLP)**: Chatbot chuyển từ việc sử dụng các API ngoại lai (như MiMo, Gemini) sang cơ chế phân tích NLP nội bộ (NLP.js, fuse.js, regex) để tránh rò rỉ dữ liệu khách hàng và cấu hình API key.
3. **Bảo mật JWT và Bcrypt**: Hủy bỏ việc dùng `user_id` thô làm token và mật khẩu plaintext. Toàn bộ hệ thống hiện sử dụng JWT qua header `Authorization` và mật khẩu băm bằng Bcrypt.
4. **WebSocket cho Real-time Chat**: Đã có kế hoạch chuyển đổi từ HTTP Polling sang WebSocket cho module Chat để giảm tải server và tối ưu hóa thời gian thực (được nêu trong WEBSOCKET_MIGRATION_PLAN.md).
5. **Đóng gói Bundle Duy Nhất**: Backend sử dụng `esbuild` biên dịch `server.ts` thành file `dist/server.cjs` duy nhất chạy Production cho tốc độ load nhanh nhất.


## Nguyên tắc bất biến
- Luôn giao tiếp bằng ngôn ngữ nghiệp vụ sản phẩm (không dùng từ ngữ kỹ thuật/code thuần túy) và luôn gắn mã `[Ref-ID: XXX]` ở cuối câu trả lời.
- Bắt buộc ghi log kỹ thuật ngầm vào `docs/technical_logs/log_YYYY_MM_DD.md` cho mỗi tác vụ sửa đổi.
- Luôn tuân thủ các quy ước được định nghĩa trong `docs/CONVENTIONS.md`.

## Nguyên tắc: Tài liệu KHÔNG mặc định đáng tin
1. Trước khi hành động dựa trên bất kỳ file nào trong /docs, kiểm tra thời gian cập nhật gần nhất của file đó. Nếu quá [X] ngày kể từ lần sửa code liên quan gần nhất, hoặc nếu có dấu hiệu mâu thuẫn với code thực tế, KHÔNG được tin ngay — phải đọc trực tiếp code liên quan để xác minh trước khi tiếp tục.
2. Với bất kỳ thông tin nào trong /docs có thể kiểm chứng trực tiếp từ code (tên hàm, cấu trúc API, schema DB...), coi code là nguồn sự thật cuối cùng. Nếu phát hiện /docs sai lệch so với code, PHẢI sửa lại /docs ngay trong phiên đó, không được để lại "làm sau".
3. Một tác vụ chỉ được coi là HOÀN THÀNH khi:
   - Code đã sửa xong
   - VÀ tài liệu liên quan (BIBLE.md của domain, DECISIONS.md nếu có quyết định mới, CONVENTIONS.md nếu có quy ước mới) đã được cập nhật tương ứng
   Nếu chỉ sửa code mà không cập nhật docs liên quan, coi như tác vụ CHƯA XONG — phải tự cập nhật trước khi báo cáo hoàn thành.
4. Nếu phát hiện mâu thuẫn giữa 2 nguồn tài liệu (vd ARCHITECTURE.md và 1 BIBLE.md nói khác nhau về cùng 1 thứ), KHÔNG tự chọn 1 bên để tin — báo ngay cho người dùng, không tự suy diễn.
5. Cuối mỗi phiên, trong HANDOFF.md, liệt kê rõ: những file /docs nào đã được cập nhật trong phiên này, và những file nào NGHI NGỜ đã lỗi thời nhưng chưa kịp sửa (để cảnh báo cho phiên sau hoặc dashboard giám sát).

## Bảng điều hướng
| Loại việc / Scope | Đọc file nào trước | Ghi chú |
|---|---|---|
| Cấu trúc hệ thống chung | `docs/ARCHITECTURE.md` | Xem cách các thành phần tương tác, tech stack tổng thể. |
| Quy ước Code & Giao tiếp | `docs/CONVENTIONS.md` | Các quy ước về naming, folder, và logging. |
| Logic Cấu trúc Database | `docs/DECISIONS.md` | Đọc để hiểu lý do chọn PostgreSQL, các design pattern áp dụng. |
| Module CRM (Khách hàng) | `docs/MODULES/crm.md` | Khi làm việc với `Customers.tsx`, `Orders.tsx`, `Leads.tsx`. |
| Module Chatbot & Chat | `docs/MODULES/chat.md`, `docs/MODULES/chatbot.md` | Khi làm việc với real-time chat hoặc Rule-based NLP. |
| Module Tasks & OKR | `docs/MODULES/tasks.md`, `docs/MODULES/okr.md` | Khi phân công công việc hoặc xem báo cáo mục tiêu. |

## Khi không chắc phạm vi
- Hãy chủ động hỏi lại người dùng để làm rõ yêu cầu hoặc giới hạn của tác vụ thay vì tự suy đoán.
- Hoặc, hãy đọc lướt `docs/ARCHITECTURE.md` để nắm bắt bối cảnh chung trước khi đưa ra quyết định.

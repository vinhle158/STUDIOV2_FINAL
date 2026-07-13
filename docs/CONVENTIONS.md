# Quy ước Lập trình (Coding Conventions)

## 1. Kiến trúc và Cấu trúc thư mục
- **Thư mục `src/`**: Chứa toàn bộ logic Frontend và các tiện ích dùng chung (như `db_service.ts`).
- **Phân tách Mobile/Desktop**: Các Component Desktop nằm ở `src/components/`, các Component cho điện thoại nằm ở `src/components/mobile/`. Component nào quá lớn (>800 dòng) nên được chia nhỏ thành các sub-components.
- **Luôn import qua `api.ts`**: Frontend gọi API phải sử dụng các phương thức `api.get`, `api.post` từ `src/lib/api.ts` để tự động xử lý token.

## 2. Naming Conventions
- Component và Interfaces: Sử dụng `PascalCase` (VD: `Dashboard`, `User`).
- Biến và hàm: Sử dụng `camelCase` (VD: `totalAmount`, `handleLogin`).
- Không sử dụng `any`: Khai báo Interface tĩnh cho các state, props và payloads API.

## 3. State Management và Dữ liệu
- Quản lý trạng thái cục bộ bằng `useState` và truyền qua các component thông qua `props` hoặc `context` nếu cần thiết (không dùng Redux/Zustand).
- Tránh mutate trực tiếp data, luôn clone mảng/objects khi cập nhật state.

## 4. Bảo mật và API Design
- **Middlewares**: Các route nhạy cảm luôn phải có `authenticate` và `requirePermission('<permission-name>')`.
- **Validation**: Kiểm tra dữ liệu đầu vào (input validation) trước khi thao tác DB.
- **Sanitize**: Sử dụng `sanitizeUser` để bỏ thuộc tính `password_hash` trước khi trả về object User qua API. Không gửi dữ liệu nhạy cảm ra Frontend.

## 5. Xử lý Log và Giao tiếp AI Agent (Communication & Logging)

Mục tiêu: Đảm bảo giao tiếp với người dùng bằng ngôn ngữ tự nhiên, không chứa thuật ngữ kỹ thuật phức tạp, đồng thời lưu trữ chi tiết kỹ thuật vào file log riêng biệt để tra cứu khi cần.

### 5.1. Phản hồi trên Chat (User Interface)
- **Ngôn ngữ:** Sử dụng ngôn ngữ chuyên môn theo góc độ Nghiệp vụ Sản phẩm (Product/Business Logic) hoặc Quản trị Dự án. Tránh sử dụng văn phong quá đời thường hoặc những phép ẩn dụ không cần thiết.
- **Cách diễn đạt:** Tập trung mô tả trực diện vào các thành phần cấu trúc ứng dụng: Giao diện (UI), Cơ sở dữ liệu (Database), và Luồng người dùng (User Flow). 
  - *Ví dụ đúng:* "Phần nút bấm tôi đã chuyển sang tông màu đỏ", "Phần cơ sở dữ liệu tôi đã thêm cột 'Khách hàng'".
- **Tuyệt đối tránh:** Các từ ngữ kỹ thuật chuyên sâu về thuật toán hoặc code thuần túy (ví dụ: "Sử dụng hàm async/await", "Viết vòng lặp for", "INNER JOIN 2 table") trừ khi được yêu cầu.
- **Gắn mã ID:** BẮT BUỘC ở cuối mỗi câu trả lời hoặc sau mỗi phần tính năng vừa hoàn thành, phải sinh ra một mã ID định dạng `[Ref-ID: XXX]` (ví dụ: `[Ref-ID: 001]`).

### 5.2. Ghi Log Kỹ Thuật (Technical Dictionary/Logging)
- **Hành động ngầm:** Đi kèm với việc trả lời trên chat, Agent PHẢI tự động ghi lại toàn bộ chi tiết kỹ thuật thực sự của tác vụ đó vào một file log riêng.
- **Vị trí lưu log:** Lưu vào thư mục `docs/technical_logs/` của dự án. Tên file lưu theo ngày, ví dụ: `docs/technical_logs/log_YYYY_MM_DD.md`.
- **Cấu trúc File Log:** Sử dụng format Markdown. Đây là nơi duy nhất Agent ĐƯỢC PHÉP dùng ngôn ngữ kỹ thuật, code snippets, và phân tích chuyên sâu.
- **Định dạng mỗi Log entry:**
  ```markdown
  ### [Ref-ID: XXX] - [Tên tóm tắt tác vụ]
  - **Thời gian:** HH:MM
  - **Chi tiết thay đổi:** (Giải thích logic code, các hàm đã sửa, logic thuật toán)
  - **File bị tác động:**
    - `path/to/file1.js`: (Làm gì ở đây)
    - `path/to/file2.css`: (Làm gì ở đây)
  ```
  
Khi quy tắc này được áp dụng, Agent đóng vai trò như một bộ lọc: Người dùng chỉ đọc bản dịch đơn giản, còn máy móc tự động sinh ra "Từ điển kỹ thuật" tương ứng thông qua mã ID.

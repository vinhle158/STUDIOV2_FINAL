# Kiến trúc Hệ thống STUDIO V2 (Actual)

## 1. Tổng quan
Dự án STUDIO V2 là ứng dụng web quản lý hoạt động nội bộ của Studio V2.
Hệ thống sử dụng kiến trúc Monolithic kết hợp với React trên Frontend và Express.js trên Backend, được đóng gói để tối ưu hóa hiệu năng.

## 2. Tech Stack Chính
- **Frontend**: React 19.0.1, Vite 6.2.3, Tailwind CSS v4, Motion (Framer Motion), Recharts, Lucide React.
- **Backend**: Node.js & Express.js (v4.21.2) bằng TypeScript.
- **ORM**: Prisma (v6.2.0).
- **Database**: PostgreSQL (Active Cache mode). Hệ thống đã loại bỏ hoàn toàn cơ chế đồng bộ song song với `db.json` cũ.
- **Build Tools**: Vite cho frontend, `esbuild` cho backend.

## 3. Cấu trúc Modules Chính
### 3.1 Backend (`server.ts`)
Toàn bộ logic backend hiện tại tập trung trong file `server.ts` (~3500 dòng), bao gồm:
- **Authentication & Security**: Sử dụng JWT token, rate limiting (`express-rate-limit`), password hashing (`bcryptjs`), phân quyền bằng middleware `requirePermission`.
- **API Endpoints**: Quản lý Customer, Order, Task, Leads, OKR, Staff, Chat.
- **Offline NLP Chatbot**: Logic phân tích cú pháp tĩnh và template ngôn ngữ tự nhiên tích hợp sẵn (không dùng LLM) cho chức năng trợ lý quản trị.
- **Database Access Layer**: `src/db_service.ts` quản lý kết nối PostgreSQL qua Prisma.

### 3.2 Frontend (`src/`)
Frontend được tổ chức dạng SPA (Single Page Application) với kiến trúc component-based:
- `App.tsx`: Điểm vào chính, quản lý routing và state toàn cục.
- `lib/api.ts`: API Client wrapper tự động đính kèm `Authorization: Bearer <token>`.
- `hooks/useIsMobile.ts`: Hook phát hiện thiết bị di động để switch sang Mobile UI.
- `components/`: Chứa các thành phần giao diện desktop.
- `components/mobile/`: Chứa giao diện được thiết kế tối ưu riêng cho màn hình điện thoại (Mobile UI).

### 3.3 Database Schema (PostgreSQL)
Mô hình dữ liệu chính gồm các thực thể: `User`, `Customer`, `Order`, `Task`, `Lead`, `Role`, `Objective` và các thực thể liên kết (Chat, Notifications).

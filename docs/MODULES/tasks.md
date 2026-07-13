# Module: Quản lý Công việc & Nhân sự (Tasks & Staff)

## Tổng quan
Module này chịu trách nhiệm phân công nhiệm vụ (chụp ảnh, chỉnh sửa...) cho nhân viên và quản lý danh sách nhân sự trong Studio.

## Luồng hoạt động
1. **Quản lý Nhân sự**: Admin/Manager thêm tài khoản nhân viên qua `Staff.tsx`, cấp quyền (Photographer, Editor, Staff).
2. **Giao việc (Tasks)**: Từ các đơn hàng hoặc giao việc độc lập, Manager tạo Task tại `Tasks.tsx` và gán cho nhân viên cụ thể.
3. **Cập nhật tiến độ**: Nhân viên đăng nhập, xem danh sách công việc được giao và đánh dấu hoàn thành.

## Thành phần Frontend
- `src/components/Staff.tsx`: Quản lý danh sách nhân viên và quyền hạn (RBAC).
- `src/components/Tasks.tsx`: Kanban/List view cho công việc.

## Cấu trúc Dữ liệu (Database)
- Bảng `User` (Nhân viên): ID, Username, Role, Status...
- Bảng `Task`: ID, AssigneeID, OrderID, Description, Status (Pending, In Progress, Done)...

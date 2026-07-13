# Module: CRM (Khách hàng & Đơn hàng)

## Tổng quan
Module CRM (Customer Relationship Management) chịu trách nhiệm quản lý thông tin khách hàng, khách hàng tiềm năng (Leads) và các đơn hàng dịch vụ (Orders).

## Luồng hoạt động (User Flow)
1. **Tiếp nhận Leads**: Thông tin khách hàng tiềm năng được ghi nhận qua `Leads.tsx`.
2. **Chuyển đổi thành Khách hàng (Customers)**: Khi Leads đồng ý sử dụng dịch vụ, thông tin được chuyển sang bảng Customers (`Customers.tsx`).
3. **Tạo Đơn hàng (Orders)**: Khách hàng được gắn kết với các hợp đồng dịch vụ cụ thể thông qua `Orders.tsx`. Quản lý trạng thái thanh toán (đặt cọc, hoàn tất).

## Thành phần Frontend
- `src/components/Customers.tsx`: Giao diện danh sách và chi tiết khách hàng.
- `src/components/Leads.tsx`: Giao diện theo dõi cơ hội bán hàng.
- `src/components/Orders.tsx`: Giao diện quản lý hợp đồng/đơn hàng.

## Cấu trúc Dữ liệu (Database)
- Bảng `Customer`: ID, Name, Phone, Address...
- Bảng `Order`: ID, CustomerID, ServiceType, TotalAmount, Status...
- Bảng `Lead`: ID, Source, Status, Note...

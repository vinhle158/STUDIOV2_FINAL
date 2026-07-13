# Module: Mục tiêu Doanh số (Objectives / OKR)

## Tổng quan
Module Objectives giúp ban quản lý thiết lập mục tiêu kinh doanh (doanh thu, số lượng hợp đồng) theo từng tháng/quý và theo dõi tiến độ hoàn thành.

## Luồng hoạt động
1. **Thiết lập Mục tiêu**: Admin tạo các mục tiêu (Target) qua `Objectives.tsx` (VD: Đạt 100 triệu doanh thu tháng 7).
2. **Tính toán Tiến độ**: Hệ thống tự động tính toán tổng doanh thu/hợp đồng từ module Orders và đối chiếu với mục tiêu.
3. **Hiển thị trực quan**: Hiển thị phần trăm hoàn thành bằng các thanh tiến trình (Progress Bar) hoặc biểu đồ.

## Thành phần Frontend
- `src/components/Objectives.tsx`: Giao diện danh sách mục tiêu và thanh tiến độ hoàn thành.
- Dashboard: Các mục tiêu này cũng thường được tóm tắt trên `Dashboard.tsx`.

## Cấu trúc Dữ liệu (Database)
- Bảng `Objective`: ID, Title, TargetValue, CurrentValue, Type (Revenue/Quantity), StartDate, EndDate...

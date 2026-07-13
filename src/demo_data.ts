import { DatabaseSchema, defaultRoles, defaultUsersFunc, Customer, Order, OrderStatusHistory, Task, Objective, ObjectiveKeyResult, Lead, ChatMessage } from './db_service';

// Helper functions for random generation
const randomInt = (min: number, max: number) => Math.floor(Math.random() * (max - min + 1)) + min;
const randomChoice = <T>(arr: T[]): T => arr[randomInt(0, arr.length - 1)];

const lastNames = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý"];
const firstNamesM = ["Anh Tuấn", "Quốc Bảo", "Minh Triết", "Hữu Duy", "Anh Đức", "Thế Vinh", "Minh Khang", "Việt Tiến", "Hoàng Nam", "Quốc Hưng", "Tiến Đạt", "Minh Hoàng", "Đức Tài", "Hải Đăng", "Nhật Minh"];
const firstNamesF = ["Thu Hà", "Khánh Vy", "Hồng Hạnh", "Hoàng Yến", "Mai Chi", "Kim Oanh", "Triệu Vy", "Thảo Vân", "Bảo Ngọc", "Mỹ Linh", "Thu Trang", "Phương Trinh", "Lan Anh", "Quỳnh Như", "Thảo Ly"];
const addresses = [
  "Thanh Xuân, Hà Nội", "Quận 9, TP. HCM", "Bình Thạnh, TP. HCM", "Nam Từ Liêm, Hà Nội", "Long Biên, Hà Nội", "Tân Bình, TP. HCM", "Quận 2, TP. HCM", "Cầu Giấy, Hà Nội", "Quận 1, TP. HCM", "Đống Đa, Hà Nội", "Hoàn Kiếm, Hà Nội", "Hà Đông, Hà Nội", "Quận 7, TP. HCM", "Thủ Đức, TP. HCM", "Gò Vấp, TP. HCM"
];
const packages = [
  { name: "Gói Album Phim Trường Premium", price: 18000000 },
  { name: "Trọn gói Pre-wedding Đà Lạt & Ngày Cưới Luxury", price: 45000000 },
  { name: "Trọn gói Album Phim trường L'amour", price: 15000000 },
  { name: "Thuê Váy Cưới Luxury Elie Saab VIP", price: 12000000 },
  { name: "Quay phim Phóng sự cưới Gold & Váy thiết kế", price: 22000000 },
  { name: "Concept Studio Hàn Quốc", price: 10000000 },
  { name: "Combo Wedding Day Diamond Full Service", price: 65000000 },
  { name: "Album ngoại cảnh Ba Vì mùa thu hoa dã quỳ", price: 16000000 },
  { name: "Chụp ảnh gia đình Premium", price: 8000000 },
  { name: "Gói chụp mẹ bầu kỷ niệm", price: 5000000 },
  { name: "Chụp kỷ yếu VIP", price: 6000000 }
];

import bcrypt from 'bcryptjs';

export const getDemoMockData = (): DatabaseSchema => {
  const users = defaultUsersFunc();
  
  // Add a specific user for demo mode
  users.push({
    id: 'user-admin-demo',
    full_name: 'Demo Admin',
    email: 'admin',
    password_hash: bcrypt.hashSync('studio', 10),
    role_id: 'role-admin',
    is_active: true,
    created_at: new Date().toISOString(),
    session_version: 0
  });

  
  const defaultStudioSettings = {
    name: "Studio V2",
    phone: "0901 234 567",
    email: "contact@studiov2.com",
    address: "123 Đường Ba Tháng Hai, Quận 10, TP. Hồ Chí Minh",
    website: "https://studiov2.vn",
    opening_hours: "08:30 - 21:30",
    notes: "Studio váy cưới cao cấp & dịch vụ chụp ảnh trọn gói chuyên nghiệp.",
    backup_schedule: "weekly",
    last_backup_time: "",
    anniversary_reminder_days: 7
  };

  const numItems = randomInt(40, 50);

  // Generate Customers
  const customers: Customer[] = [];
  for (let i = 1; i <= numItems; i++) {
    const groom = `${randomChoice(lastNames)} ${randomChoice(firstNamesM)}`;
    const bride = `${randomChoice(lastNames)} ${randomChoice(firstNamesF)}`;
    customers.push({
      id: `cust-${i}`,
      full_name: `${groom} & ${bride}`,
      phone: `09${randomInt(10000000, 99999999)}`,
      email: `customer${i}@example.com`,
      address: randomChoice(addresses),
      notes: "Generated customer notes.",
      created_at: new Date(Date.now() - randomInt(0, 30) * 86400000).toISOString(),
      updated_at: new Date().toISOString()
    });
  }

  // Generate Orders
  const orders: Order[] = [];
  const orderStatuses = ['new', 'confirmed', 'shooting', 'editing', 'ready', 'delivered', 'cancelled'];
  for (let i = 1; i <= numItems; i++) {
    const pkg = randomChoice(packages);
    const dateStr = new Date(Date.now() + randomInt(-10, 30) * 86400000).toISOString().split('T')[0];
    orders.push({
      id: `order-${i}`,
      order_code: `HĐ-2026-${i.toString().padStart(4, '0')}`,
      customer_id: `cust-${randomInt(1, numItems)}`,
      status: randomChoice(orderStatuses) as any,
      shoot_date: dateStr,
      shoot_time: "08:00",
      package_name: pkg.name,
      package_price: pkg.price,
      deposit_amount: pkg.price * 0.3,
      total_amount: pkg.price,
      notes: "Generated order details.",
      created_by: randomChoice(users).id,
      created_at: new Date(Date.now() - randomInt(0, 30) * 86400000).toISOString(),
      updated_at: new Date().toISOString()
    });
  }

  // Generate Order Status History
  const order_status_history: OrderStatusHistory[] = [];
  for (let i = 1; i <= numItems; i++) {
    order_status_history.push({
      id: `osh-${i}`,
      order_id: `order-${randomInt(1, numItems)}`,
      from_status: "new",
      to_status: "confirmed",
      changed_by: randomChoice(users).id,
      note: "Status updated.",
      changed_at: new Date().toISOString()
    });
  }

  // Generate Tasks
  const tasks: Task[] = [];
  const taskPriorities = ['low', 'normal', 'high'];
  const taskStatuses = ['pending', 'in_progress', 'done', 'cancelled'];
  for (let i = 1; i <= numItems; i++) {
    tasks.push({
      id: `task-${i}`,
      title: `Task công việc điều phối ${i}`,
      description: "Chi tiết công việc cần hoàn thiện.",
      order_id: `order-${randomInt(1, numItems)}`,
      assigned_to: randomChoice(users).id,
      assigned_by: randomChoice(users).id,
      status: randomChoice(taskStatuses) as any,
      priority: randomChoice(taskPriorities) as any,
      due_date: new Date(Date.now() + randomInt(1, 10) * 86400000).toISOString().split('T')[0],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    });
  }

  // Generate Leads
  const leads: Lead[] = [];
  const sources = ["PAGE THE WILL", "PAGE FAMILY", "VÃNG LAI", "KHÁCH CŨ", "ĐƯỢC GIỚI THIỆU"];
  for (let i = 1; i <= numItems; i++) {
    const randStep = randomInt(1, 6);
    let status = 'consulting';
    if (randStep === 6) status = randomChoice(['won', 'lost']);
    
    leads.push({
      id: `lead-${i}`,
      date: new Date(Date.now() - randomInt(0, 15) * 86400000).toISOString().split('T')[0],
      customer_name: `${randomChoice(lastNames)} ${randomChoice(firstNamesF)}`,
      phone: `09${randomInt(10000000, 99999999)}`,
      source: randomChoice(sources),
      interested_packages: { beauty: false, family: false, wedding: true, combo: false, couple: false },
      sales_step: randStep,
      follow_up_status: { follow_1: true, follow_2: randStep > 2, follow_3: randStep > 4 },
      status: status as any,
      revenue: status === 'won' ? randomChoice(packages).price : null,
      success_reason: status === 'won' ? "Đã chốt" : null,
      failure_reason: status === 'lost' ? "Không có nhu cầu" : null,
      assigned_sale_id: randomChoice(users).id,
      support_needed: null,
      notes: "Lead note generated.",
      admin_feedbacks: [],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    });
  }

  // Generate Objectives & KRs
  const objectives: Objective[] = [];
  const objective_key_results: ObjectiveKeyResult[] = [];
  for (let i = 1; i <= 5; i++) {
    objectives.push({
      id: `obj-${i}`,
      title: `Mục tiêu phòng ban Q3 - Số ${i}`,
      description: "Đẩy mạnh doanh số và KPIs phòng ban.",
      status: 'active',
      created_by: randomChoice(users).id,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      completed_at: null
    });
    
    for (let j = 1; j <= randomInt(5, 8); j++) {
      objective_key_results.push({
        id: `kr-${i}-${j}`,
        objective_id: `obj-${i}`,
        title: `Kết quả then chốt KR ${j}`,
        assigned_department: "Kinh doanh",
        assigned_to_user_id: randomChoice(users).id,
        status: 'active',
        progress: randomInt(0, 100),
        notes: "Ghi chú tiến độ.",
        updated_at: new Date().toISOString()
      });
    }
  }

  // Generate Chat Messages
  const chat_messages: ChatMessage[] = [];
  for (let i = 1; i <= numItems; i++) {
    chat_messages.push({
      id: `msg-${i}`,
      sender_id: randomChoice(users).id,
      receiver_id: null,
      content: `Nội dung trao đổi công việc mẫu số ${i} về hợp đồng và setup.`,
      created_at: new Date(Date.now() - randomInt(0, 5) * 86400000).toISOString()
    });
  }

  return {
    users,
    roles: defaultRoles,
    studio_settings: defaultStudioSettings as any,
    customers,
    orders,
    order_status_history,
    tasks,
    task_updates: [],
    objectives,
    objective_key_results,
    objective_progress_updates: [],
    notifications: [],
    chat_messages,
    backups: [],
    leads
  };
};

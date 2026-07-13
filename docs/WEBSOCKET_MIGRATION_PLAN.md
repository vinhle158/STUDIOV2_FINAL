# 📋 Kế hoạch Chuyển đổi từ Polling sang WebSocket

> **Dự án:** STUDIO V2 - Studio V2  
> **Ngày tạo:** 13/07/2026  
> **Mục tiêu:** Thay thế HTTP Polling bằng WebSocket cho Chat nội bộ  

---

## 🎯 Mục tiêu Dự án

Thay thế cơ chế HTTP Polling (15 giây/lần) bằng WebSocket để:
- ✅ Nhận tin nhắn **real-time**
- ✅ Giảm tải server (giảm 75% request không cần thiết)
- ✅ Cải thiện trải nghiệm người dùng
- ✅ Tiết kiệm băng thông và tài nguyên client

---

## 📊 So sánh Kiến trúc

### Hiện tại (HTTP Polling)

`
Client                    Server
   │                         │
   │──GET /messages─────────→│  (mỗi 15s)
   │←───[200] Messages──────│
   │                         │
   │──GET /messages─────────→│  (mỗi 15s)
   │←───[200] Messages──────│
   │                         │
   ▼                         ▼
`

**Nhược điểm:**
- Tải server cao (40 request/phút với 10 users)
- Độ trễ 15 giây
- Truyền dữ liệu không cần thiết

### Mục tiêu (WebSocket)

`
Client                    Server
   │                         │
   │───────Connect──────────→│
   │←──[Connected]──────────│
   │                         │
   │───────Join Room────────→│
   │                         │
   │   ←──[New Message]─────│  (real-time khi có tin nhắn mới)
   │                         │
   │───────Send Message─────→│
   │←──[Message Sent]───────│
   │                         │
   ▼                         ▼
`

**Ưu điểm:**
- Real-time (millisecond latency)
- Giảm tải server đáng kể
- Tiết kiệm băng thông
- Hỗ trợ typing indicators, read receipts

---

## 🛠️ Các bước Thực hiện

### **Phase 1: Chuẩn bị (1-2 ngày)**

| # | Công việc | Chi tiết | Ưu tiên |
|---|-----------|----------|---------|
| 1 | Cài đặt thư viện | `npm install socket.io` (server), `npm install socket.io-client` (client) | Cao |
| 2 | Thiết kế schema events | Định nghĩa các event: `join_chat`, `new_message`, `typing`, `read_receipt` | Cao |
| 3 | Cập nhật Docker Compose | Thêm service Redis (nếu cần scale nhiều server) | Trung bình |
| 4 | Tạo tài liệu API WebSocket | Mô tả các events, payloads, error codes | Trung bình |

---

### **Phase 2: Backend (2-3 ngày)**

| # | Công việc | Chi tiết | Files cần sửa |
|---|-----------|----------|---------------|
| 1 | Tích hợp Socket.IO vào Express | Tạo WebSocket server cùng port 3005 | `server.ts` |
| 2 | Implement auth middleware | Verify JWT khi kết nối WebSocket | `server.ts` |
| 3 | Xử lý join/leave room | Mỗi cặp users hoặc group chat là 1 room | `server.ts` |
| 4 | Emit events khi có tin nhắn mới | Khi POST `/api/chat/messages` → emit `new_message` | `server.ts` |
| 5 | Lưu trữ connection state | Map userId → socketId | `server.ts` |

**Code mẫu Backend:**

`	ypescript
// server.ts
import { Server } from 'socket.io';

const io = new Server(server, {
  cors: { origin: process.env.CORS_ORIGIN }
});

// Auth middleware
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  try {
    const user = jwt.verify(token, JWT_SECRET);
    socket.data.user = user;
    next();
  } catch (err) {
    next(new Error('Authentication error'));
  }
});

io.on('connection', (socket) => {
  console.log(User connected: );
  
  // Join chat room
  socket.on('join_chat', ({ receiverId }) => {
    const roomId = [socket.data.user.id, receiverId].sort().join('_');
    socket.join(roomId);
  });
  
  // Handle new message
  socket.on('send_message', ({ receiverId, content }) => {
    const roomId = [socket.data.user.id, receiverId].sort().join('_');
    io.to(roomId).emit('new_message', {
      sender_id: socket.data.user.id,
      content,
      created_at: new Date().toISOString()
    });
  });
  
  socket.on('disconnect', () => {
    console.log(User disconnected: );
  });
});

// Trong POST /api/chat/messages
app.post('/api/chat/messages', authenticate, (req, res) => {
  // ... existing logic to save message ...
  
  // Emit to WebSocket
  const roomId = [req.user.id, targetUserId].sort().join('_');
  io.to(roomId).emit('new_message', newMsg);
  
  res.status(201).json(newMsg);
});
`

---

### **Phase 3: Frontend (2-3 ngày)**

| # | Công việc | Chi tiết | Files cần sửa |
|---|-----------|----------|---------------|
| 1 | Tạo Socket.IO client hook | `useSocket.ts` quản lý kết nối | `src/hooks/useSocket.ts` (mới) |
| 2 | Cập nhật Chat.tsx | Subscribe vào `new_message` event | `src/components/Chat.tsx` |
| 3 | Cập nhật MobileChat.tsx | Tương tự cho mobile | `src/components/mobile/screens/MobileChat.tsx` |
| 4 | Remove polling logic | Xóa `setInterval` trong `useEffect` | `Chat.tsx`, `MobileChat.tsx` |
| 5 | Thêm typing indicators | Optional: hiển thị "đang nhập..." | `Chat.tsx`, `MobileChat.tsx` |
| 6 | Xử lý reconnect | Tự động kết nối lại khi mất mạng | `useSocket.ts` |

**Code mẫu Frontend:**

`	ypescript
// hooks/useSocket.ts
import { useEffect, useRef } from 'react';
import { io, Socket } from 'socket.io-client';
import { useAuth } from './useAuth';

export const useSocket = () => {
  const socketRef = useRef<Socket | null>(null);
  const { token } = useAuth();

  useEffect(() => {
    if (!token) return;

    socketRef.current = io(process.env.REACT_APP_API_URL, {
      auth: { token }
    });

    return () => {
      socketRef.current?.disconnect();
    };
  }, [token]);

  return socketRef.current;
};

// components/Chat.tsx
const socket = useSocket();

useEffect(() => {
  if (!socket || !selectedReceiverId) return;

  // Join chat room
  socket.emit('join_chat', { receiverId: selectedReceiverId });

  // Listen for new messages
  socket.on('new_message', (message) => {
    setMessages(prev => [...prev, message]);
  });

  return () => {
    socket.off('new_message');
  };
}, [socket, selectedReceiverId]);
`

---

### **Phase 4: Testing & Migration (1-2 ngày)**

| # | Công việc | Chi tiết |
|---|-----------|----------|
| 1 | Unit tests | Test socket events, auth middleware |
| 2 | Integration tests | Test real-time message flow |
| 3 | Load testing | Kiểm tra với nhiều connections |
| 4 | Feature flags | Bật/tắt WebSocket để rollback dễ dàng |
| 5 | Deploy & monitor | Theo dõi logs, performance |

---

## ⚠️ Rủi ro & Giải pháp

| Rủi ro | Mức độ | Giải pháp |
|--------|--------|-----------|
| **Scaling** (nhiều server) | Cao | Sử dụng Redis Adapter để share state giữa các server instances |
| **Reconnect** | Trung bình | Implement exponential backoff, hiển thị "Đang kết nối lại..." |
| **Battery drain** (mobile) | Trung bình | Tối ưu reconnect strategy, giảm heartbeat frequency |
| **Firewall/Proxy** | Thấp | Fallback sang HTTP Long Polling nếu WebSocket bị chặn |
| **Complexity** | Trung bình | Giữ HTTP API cho REST operations, chỉ dùng WS cho real-time events |

---

## 📅 Timeline Ước tính

`
┌─────────────────────────────────────────────────────────────┐
│  WEEK 1: Phase 1 + Phase 2 (Backend)                        │
│  ├── Day 1-2: Chuẩn bị (cài đặt, thiết kế)                  │
│  └── Day 3-5: Backend WebSocket implementation               │
├─────────────────────────────────────────────────────────────┤
│  WEEK 2: Phase 3 (Frontend) + Phase 4 (Testing)              │
│  ├── Day 1-3: Frontend WebSocket integration                 │
│  └── Day 4-5: Testing & bug fixes                            │
├─────────────────────────────────────────────────────────────┤
│  WEEK 3: Deploy & Monitor                                    │
│  ├── Day 1-2: Deploy to staging                              │
│  ├── Day 3-4: A/B testing (10% → 50% users)                  │
│  └── Day 5: Full rollout + monitoring                        │
└─────────────────────────────────────────────────────────────┘
`

**Tổng thời gian:** 2-3 tuần (1 developer)

---

## 🔄 Chiến lược Migration

`
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Deploy WebSocket alongside Polling                  │
│  (Cả 2 cơ chế hoạt động song song)                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Enable WebSocket cho 10% users (A/B testing)        │
│  (Theo dõi performance, errors)                              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Tăng dần lên 50% → 100%                             │
│  (Nếu ổn định)                                               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Remove Polling code                                 │
│  (Sau khi xác nhận WebSocket ổn định 1-2 tuần)              │
└─────────────────────────────────────────────────────────────┘
`

---

## 📦 Dependencies mới

`json
{
  "dependencies": {
    "socket.io": "^4.7.4",
    "socket.io-client": "^4.7.4",
    "@socket.io/redis-adapter": "^8.2.0"
  }
}
`

---

## ✅ Checklist Hoàn thành

### Phase 1: Chuẩn bị
- [ ] Cài đặt socket.io và socket.io-client
- [ ] Thiết kế WebSocket event schema
- [ ] Cập nhật Docker Compose (nếu cần Redis)
- [ ] Viết tài liệu API WebSocket

### Phase 2: Backend
- [ ] Tích hợp Socket.IO vào Express server
- [ ] Implement JWT authentication cho WebSocket
- [ ] Xử lý join/leave room logic
- [ ] Emit events khi có tin nhắn mới
- [ ] Test backend WebSocket endpoints

### Phase 3: Frontend
- [ ] Tạo useSocket hook
- [ ] Cập nhật Chat.tsx (Desktop)
- [ ] Cập nhật MobileChat.tsx (Mobile)
- [ ] Remove polling logic
- [ ] Implement typing indicators (optional)
- [ ] Xử lý reconnect logic

### Phase 4: Testing & Deploy
- [ ] Viết unit tests
- [ ] Viết integration tests
- [ ] Load testing
- [ ] Deploy to staging
- [ ] A/B testing
- [ ] Full rollout
- [ ] Monitoring setup

---

## 📚 Tài liệu Tham khảo

- [Socket.IO Documentation](https://socket.io/docs/v4/)
- [Socket.IO Redis Adapter](https://socket.io/docs/v4/redis-adapter/)
- [WebSocket Authentication Best Practices](https://socket.io/docs/v4/middlewares/)

---

## 👥 Stakeholders

| Vai trò | Người | Trách nhiệm |
|---------|-------|-------------|
| Developer | TBD | Implement WebSocket backend & frontend |
| DevOps | TBD | Cập nhật Docker, monitoring |
| QA | TBD | Testing real-time features |
| PM | TBD | Theo dõi tiến độ, review |

---

*"Real-time communication is no longer a luxury, it's a requirement."*

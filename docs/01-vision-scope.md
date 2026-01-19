# Vision & Scope - OldGoods Marketplace

## 1. Tên Dự án
**OldGoods** - Mini Marketplace cho Sinh viên/Khu Dân cư

## 2. Mục tiêu Dự án

### 2.1 Vấn đề Cần Giải quyết
- Sinh viên và cư dân trong khu vực có nhu cầu mua bán đồ cũ nội bộ nhưng thiếu kênh tin cậy, dễ tìm kiếm
- Không có nền tảng tập trung để đăng tin, tìm kiếm, và trao đổi trực tiếp
- Thiếu tính năng chat realtime để thương lượng và chốt giao dịch nhanh chóng
- Khó kiểm soát và báo cáo các hành vi không phù hợp

### 2.2 Mục tiêu Hệ thống
Tạo nền tảng web cho phép:
- **Đăng tin bán đồ cũ** với hình ảnh, mô tả, giá cả, vị trí
- **Tìm kiếm và lọc** sản phẩm theo nhiều tiêu chí (danh mục, giá, vị trí, tình trạng)
- **Chat realtime** giữa người mua và người bán để trao đổi, thương lượng
- **Tạo offer và deal** để chốt giao dịch
- **Lên lịch meetup** để gặp mặt trao đổi hàng hóa
- **Báo cáo và chặn** người dùng/sản phẩm không phù hợp
- **Quản trị** để kiểm duyệt nội dung và xử lý báo cáo

## 3. Phạm vi Dự án

### 3.1 In-Scope (MVP)

#### 3.1.1 Authentication & User Management
- Đăng ký tài khoản (email, password)
- Đăng nhập/Đăng xuất
- Quản lý hồ sơ người dùng (profile)
- Phân quyền: Guest, User (Buyer/Seller), Admin/Moderator

#### 3.1.2 Product Listings
- Tạo/Cập nhật/Xóa tin đăng sản phẩm
- Upload nhiều hình ảnh cho mỗi tin đăng
- Phân loại sản phẩm theo danh mục (Category)
- Quản lý trạng thái tin đăng (AVAILABLE, RESERVED, SOLD, EXPIRED)

#### 3.1.3 Search & Discovery
- Tìm kiếm theo từ khóa (keyword)
- Lọc theo danh mục, giá (min/max), vị trí, tình trạng
- Sắp xếp kết quả (mới nhất, giá tăng/giảm)
- Xem chi tiết tin đăng
- Thêm/Xóa sản phẩm vào danh sách yêu thích (Favorite)

#### 3.1.4 Real-time Chat
- Tạo cuộc trò chuyện giữa buyer và seller
- Gửi/nhận tin nhắn realtime qua WebSocket
- Lưu lịch sử tin nhắn
- Hiển thị trạng thái đã đọc (read receipt)
- Typing indicator (tùy chọn)

#### 3.1.5 Offers & Deals
- Tạo offer từ buyer cho listing
- Seller chấp nhận/từ chối offer
- Tạo deal khi offer được chấp nhận
- Lên lịch meetup (thời gian, địa điểm)
- Cập nhật trạng thái deal (PENDING, CONFIRMED, COMPLETED, CANCELLED)

#### 3.1.6 Moderation
- Báo cáo listing hoặc user
- Chặn user (block)
- Admin xem danh sách báo cáo
- Admin giải quyết báo cáo (resolve)
- Admin cấm user (ban)
- Admin xóa listing không phù hợp

### 3.2 Out-of-Scope (MVP)

#### 3.2.1 Thanh toán Online
- Không tích hợp cổng thanh toán thực (Stripe, PayPal, etc.)
- Không xử lý giao dịch tài chính thực tế
- Chỉ hỗ trợ trao đổi trực tiếp (cash on delivery)

#### 3.2.2 Vận chuyển
- Không tích hợp dịch vụ vận chuyển
- Không tính toán phí ship
- Người dùng tự thỏa thuận về giao hàng

#### 3.2.3 Tính năng Nâng cao
- AI recommendation (gợi ý sản phẩm)
- Livestream bán hàng
- Hệ thống đánh giá phức tạp (rating/review chi tiết)
- Thông báo push qua mobile app
- Social media integration
- Multi-language support

#### 3.2.4 Mobile App
- Chỉ phát triển web application
- Responsive design cho mobile browser
- Không có native mobile app

## 4. Stakeholders

### 4.1 Guest (Khách)
- **Mô tả**: Người dùng chưa đăng nhập
- **Quyền hạn**: Xem danh sách sản phẩm, tìm kiếm, xem chi tiết
- **Hạn chế**: Không thể chat, tạo offer, đăng tin

### 4.2 User - Buyer (Người mua)
- **Mô tả**: Người dùng đã đăng ký, muốn mua sản phẩm
- **Quyền hạn**: 
  - Tất cả quyền của Guest
  - Chat với seller
  - Tạo offer
  - Thêm vào favorite
  - Báo cáo listing/user
  - Chặn user

### 4.3 User - Seller (Người bán)
- **Mô tả**: Người dùng đã đăng ký, muốn bán sản phẩm
- **Quyền hạn**:
  - Tất cả quyền của Buyer
  - Tạo/Cập nhật/Xóa listing của mình
  - Quản lý offers nhận được
  - Chấp nhận/từ chối offer
  - Tạo deal và meetup

### 4.4 Admin/Moderator (Quản trị viên)
- **Mô tả**: Người quản lý hệ thống
- **Quyền hạn**:
  - Tất cả quyền của User
  - Xem tất cả báo cáo
  - Giải quyết báo cáo
  - Cấm user (ban)
  - Xóa listing không phù hợp
  - Xem thống kê hệ thống

## 5. Success Criteria

### 5.1 Functional Success
- Tất cả 9 use cases chính hoạt động end-to-end
- API endpoints trả về đúng format và status codes
- WebSocket chat hoạt động realtime không bị mất tin nhắn
- Database lưu trữ đầy đủ và nhất quán dữ liệu

### 5.2 Non-Functional Success
- Response time API < 500ms cho các endpoint chính
- Search trả về kết quả < 1s với 5000 listings
- WebSocket connection stable, reconnect tự động
- Code coverage > 60% cho domain/application layer
- Documentation đầy đủ và rõ ràng

### 5.3 Quality Success
- Không có critical bugs trong các use case chính
- Code tuân thủ coding conventions
- Database migrations chạy thành công
- Deployment guide đầy đủ để setup môi trường production

## 6. Definition of Done (MVP)

Một feature được coi là "Done" khi:
- ✅ Code được implement và review
- ✅ Unit tests được viết và pass
- ✅ Integration tests pass (nếu có)
- ✅ API documentation được cập nhật
- ✅ Database migrations được tạo và test
- ✅ Manual testing đã được thực hiện
- ✅ Không có critical bugs
- ✅ Code được merge vào main branch

## 7. Constraints & Assumptions

### 7.1 Constraints
- **Thời gian**: Dự án được thực hiện trong 4 sprints (8-10 tuần)
- **Team size**: Nhóm nhỏ (3-5 người)
- **Công nghệ**: Django, PostgreSQL (bắt buộc)
- **Budget**: Không có budget cho dịch vụ cloud trả phí (S3, etc.)

### 7.2 Assumptions
- Người dùng có kết nối Internet ổn định
- Người dùng có trình duyệt web hiện đại (Chrome, Firefox, Safari, Edge)
- Hình ảnh upload có dung lượng hợp lý (< 5MB mỗi ảnh)
- PostgreSQL database có thể truy cập từ server
- Redis là tùy chọn (cần khi scale realtime broadcast/pubsub hoặc caching)

## 8. Risks & Mitigation

### 8.1 Technical Risks
- **Risk**: WebSocket connection không ổn định
  - **Mitigation**: Implement reconnection logic, fallback polling
- **Risk**: Database performance với lượng dữ liệu lớn
  - **Mitigation**: Indexing strategy, pagination, query optimization

### 8.2 Project Risks
- **Risk**: Không đủ thời gian để hoàn thành tất cả features
  - **Mitigation**: Ưu tiên MVP features, loại bỏ nice-to-have
- **Risk**: Team members không quen với FastAPI WebSocket và async patterns
  - **Mitigation**: Training session, documentation, code review

## 9. Timeline Overview

- **Sprint 1** (2-3 tuần): Foundation - Auth, Listings CRUD, Database
- **Sprint 2** (2 tuần): Search, Media Upload, Favorites
- **Sprint 3** (2-3 tuần): Real-time Chat với WebSocket
- **Sprint 4** (2 tuần): Deals, Moderation, Testing, Documentation

## 10. References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- Alembic Documentation: https://alembic.sqlalchemy.org/
- PostgreSQL Documentation: https://www.postgresql.org/docs/

# Software Requirements Specification (SRS)
## OldGoods Marketplace

**Version**: 1.0  
**Date**: 2024  
**Authors**: Development Team

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [System Features](#3-system-features)
4. [External Interface Requirements](#4-external-interface-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Business Rules](#6-business-rules)

---

## 1. Introduction

### 1.1 Purpose
Tài liệu này mô tả chi tiết các yêu cầu chức năng và phi chức năng của hệ thống OldGoods Marketplace - một nền tảng mua bán đồ cũ cho sinh viên và cư dân trong khu vực.

### 1.2 Scope
Hệ thống bao gồm:
- Quản lý người dùng và xác thực
- Đăng tin và quản lý sản phẩm
- Tìm kiếm và lọc sản phẩm
- Chat realtime giữa người mua và người bán
- Tạo offer và deal
- Báo cáo và kiểm duyệt

### 1.3 Definitions, Acronyms, and Abbreviations
- **MVP**: Minimum Viable Product
- **UC**: Use Case
- **API**: Application Programming Interface
- **REST**: Representational State Transfer
- **WebSocket**: Communication protocol for real-time bidirectional communication
- **ORM**: Object-Relational Mapping
- **JWT**: JSON Web Token

### 1.4 References
- Vision & Scope Document (01-vision-scope.md)
- FastAPI Documentation
- SQLAlchemy Documentation
- Alembic Documentation

### 1.5 Overview
Tài liệu được tổ chức theo cấu trúc use-case based, mô tả chi tiết từng chức năng của hệ thống.

---

## 2. Overall Description

### 2.1 Product Perspective
OldGoods là một web application độc lập, hoạt động theo mô hình client-server:
- **Client**: Web browser (frontend tách rời)
- **Server**: FastAPI REST API + FastAPI WebSocket (chat realtime)
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Database**: PostgreSQL
- **Storage**: Local file system hoặc cloud storage (S3-compatible, tùy chọn)

### 2.2 Product Functions
Hệ thống cung cấp các chức năng chính:
1. Authentication & Authorization
2. Product Listing Management
3. Search & Filter
4. Real-time Chat
5. Offer & Deal Management
6. Moderation & Reporting

### 2.3 User Classes and Characteristics

#### 2.3.1 Guest
- Chưa đăng nhập
- Chỉ xem danh sách và chi tiết sản phẩm
- Không thể tương tác

#### 2.3.2 User (Buyer/Seller)
- Đã đăng ký và đăng nhập
- Có thể đăng tin (seller) hoặc mua hàng (buyer)
- Có thể chat, tạo offer, favorite

#### 2.3.3 Admin/Moderator
- Quyền quản trị cao nhất
- Kiểm duyệt nội dung, xử lý báo cáo

### 2.4 Operating Environment
- **Server**: Linux/Windows server với Python 3.10+
- **Database**: PostgreSQL 12+
- **Web Server**: Uvicorn (ASGI) (production có thể chạy multiple workers)
- **Client**: Modern web browsers (Chrome, Firefox, Safari, Edge)

### 2.5 Design and Implementation Constraints
- Sử dụng Django framework
- Database: PostgreSQL (bắt buộc)
- API: RESTful + WebSocket
- Code phải tuân thủ PEP 8

### 2.6 Assumptions and Dependencies
- Người dùng có Internet connection
- PostgreSQL đã được cài đặt
- Redis là tùy chọn (cần khi scale realtime broadcast)
- Python 3.10+ đã được cài đặt

---

## 3. System Features

### 3.1 Feature 1: Authentication & User Management

#### UC01: Register
**ID**: UC01  
**Actors**: Guest  
**Preconditions**: 
- Người dùng chưa đăng nhập
- Email chưa được sử dụng trong hệ thống

**Trigger**: Người dùng điền form đăng ký và submit

**Main Flow**:
1. Người dùng truy cập trang đăng ký
2. Điền thông tin: email, password, confirm password, full name
3. Hệ thống validate dữ liệu (email format, password strength, match password)
4. Hệ thống kiểm tra email đã tồn tại chưa
5. Hệ thống tạo tài khoản mới với password đã hash
6. Hệ thống tạo profile mặc định cho user
7. Hệ thống trả về success message và redirect đến trang đăng nhập

**Alternate Flows**:
- 3a. Email không hợp lệ: Hiển thị lỗi "Email không hợp lệ"
- 3b. Password quá yếu: Hiển thị lỗi "Mật khẩu phải có ít nhất 8 ký tự"
- 3c. Password không khớp: Hiển thị lỗi "Mật khẩu không khớp"
- 4a. Email đã tồn tại: Hiển thị lỗi "Email đã được sử dụng"

**Postconditions**: 
- User account được tạo trong database
- User có thể đăng nhập

**Business Rules**:
- Email phải unique
- Password phải được hash bằng bcrypt/argon2
- User mặc định có role "USER"

---

#### UC02: Login
**ID**: UC02  
**Actors**: Guest  
**Preconditions**: User đã có tài khoản

**Trigger**: Người dùng điền email/password và click Login

**Main Flow**:
1. Người dùng truy cập trang đăng nhập
2. Điền email và password
3. Hệ thống validate dữ liệu
4. Hệ thống kiểm tra email tồn tại
5. Hệ thống verify password
6. Hệ thống tạo JWT token
7. Hệ thống trả về token và user info
8. Client lưu token và redirect đến trang chủ

**Alternate Flows**:
- 4a. Email không tồn tại: Hiển thị lỗi "Email hoặc mật khẩu không đúng"
- 5a. Password sai: Hiển thị lỗi "Email hoặc mật khẩu không đúng"
- 5b. User bị ban: Hiển thị lỗi "Tài khoản đã bị khóa"

**Postconditions**: 
- User đã đăng nhập
- JWT token được lưu ở client

**Business Rules**:
- JWT token có thời hạn 7 ngày
- Refresh token có thời hạn 30 ngày

---

#### UC03: Logout
**ID**: UC03  
**Actors**: User  
**Preconditions**: User đã đăng nhập

**Trigger**: User click nút Logout

**Main Flow**:
1. User click Logout
2. Client xóa JWT token
3. Client redirect đến trang đăng nhập

**Postconditions**: User đã đăng xuất

---

### 3.2 Feature 2: Product Listing Management

#### UC04: Create Listing
**ID**: UC04  
**Actors**: Seller  
**Preconditions**: 
- User đã đăng nhập
- User có role SELLER hoặc USER

**Trigger**: User click "Đăng tin mới"

**Main Flow**:
1. User truy cập trang tạo listing
2. Điền thông tin: title, description, category, price, condition, location
3. Upload ít nhất 1 hình ảnh (tối đa 5 ảnh)
4. Hệ thống validate dữ liệu
5. Hệ thống lưu hình ảnh vào storage
6. Hệ thống tạo Listing record với status AVAILABLE
7. Hệ thống tạo các ListingImage records
8. Hệ thống trả về success và redirect đến trang chi tiết listing

**Alternate Flows**:
- 3a. Không upload ảnh: Hiển thị lỗi "Vui lòng upload ít nhất 1 hình ảnh"
- 3b. Upload quá 5 ảnh: Chỉ lấy 5 ảnh đầu tiên
- 4a. Title trống: Hiển thị lỗi "Tiêu đề không được để trống"
- 4b. Price <= 0: Hiển thị lỗi "Giá phải lớn hơn 0"
- 4c. Category không hợp lệ: Hiển thị lỗi "Danh mục không hợp lệ"

**Postconditions**: 
- Listing được tạo với status AVAILABLE
- Hình ảnh được lưu trong storage

**Business Rules**:
- Mỗi listing chỉ có 1 seller (owner)
- Listing mặc định có status AVAILABLE
- Listing có thể có nhiều hình ảnh (1-5 ảnh)

---

#### UC05: Update Listing
**ID**: UC05  
**Actors**: Seller (Owner)  
**Preconditions**: 
- User đã đăng nhập
- Listing tồn tại và thuộc về user hiện tại
- Listing có status AVAILABLE hoặc RESERVED

**Trigger**: User click "Chỉnh sửa" trên listing của mình

**Main Flow**:
1. User truy cập trang chỉnh sửa listing
2. Hệ thống load thông tin hiện tại của listing
3. User chỉnh sửa thông tin (title, description, price, etc.)
4. User có thể thêm/xóa hình ảnh
5. Hệ thống validate dữ liệu
6. Hệ thống cập nhật Listing record
7. Hệ thống cập nhật ListingImage records
8. Hệ thống trả về success

**Alternate Flows**:
- 2a. Listing không tồn tại: Hiển thị lỗi 404
- 2b. User không phải owner: Hiển thị lỗi 403 Forbidden
- 2c. Listing đã SOLD: Hiển thị lỗi "Không thể chỉnh sửa listing đã bán"

**Postconditions**: Listing được cập nhật

**Business Rules**:
- Chỉ owner mới có thể chỉnh sửa listing
- Không thể chỉnh sửa listing đã SOLD

---

#### UC06: Delete Listing
**ID**: UC06  
**Actors**: Seller (Owner), Admin  
**Preconditions**: 
- User đã đăng nhập
- Listing tồn tại

**Trigger**: User click "Xóa" trên listing

**Main Flow**:
1. User click "Xóa listing"
2. Hệ thống kiểm tra quyền (owner hoặc admin)
3. Hệ thống hiển thị xác nhận
4. User xác nhận xóa
5. Hệ thống xóa các ListingImage records
6. Hệ thống xóa Listing record
7. Hệ thống trả về success

**Alternate Flows**:
- 2a. User không có quyền: Hiển thị lỗi 403
- 4a. User hủy: Không thực hiện xóa

**Postconditions**: Listing và hình ảnh được xóa

**Business Rules**:
- Owner và Admin có thể xóa listing
- Xóa listing sẽ xóa luôn các offers liên quan (hoặc đánh dấu cancelled)

---

### 3.3 Feature 3: Search & Filter

#### UC07: Search & Filter Listings
**ID**: UC07  
**Actors**: Guest, User  
**Preconditions**: Hệ thống có ít nhất 1 listing

**Trigger**: User nhập từ khóa hoặc chọn filter và click Search

**Main Flow**:
1. User truy cập trang danh sách listings
2. User nhập từ khóa vào ô search (optional)
3. User chọn category filter (optional)
4. User chọn price range (min/max) (optional)
5. User chọn location filter (optional)
6. User chọn condition filter (optional)
7. User click Search hoặc filter tự động apply
8. Hệ thống query database với các điều kiện
9. Hệ thống sắp xếp kết quả (mặc định: mới nhất)
10. Hệ thống phân trang kết quả
11. Hệ thống trả về danh sách listings

**Alternate Flows**:
- 8a. Không có kết quả: Hiển thị "Không tìm thấy sản phẩm nào"
- 9a. User chọn sort khác: Sắp xếp theo giá tăng/giảm, hoặc cũ nhất

**Postconditions**: Danh sách listings được hiển thị

**Business Rules**:
- Search không phân biệt hoa thường
- Chỉ hiển thị listings có status AVAILABLE
- Mỗi trang hiển thị tối đa 20 listings

---

#### UC08: View Listing Details
**ID**: UC08  
**Actors**: Guest, User  
**Preconditions**: Listing tồn tại

**Trigger**: User click vào một listing

**Main Flow**:
1. User click vào listing từ danh sách
2. Hệ thống load thông tin listing (title, description, price, images, seller info)
3. Hệ thống load các offers liên quan (nếu user là owner)
4. Hệ thống hiển thị trang chi tiết
5. Nếu user đã đăng nhập và là buyer: Hiển thị nút "Chat với người bán" và "Tạo Offer"
6. Nếu user đã đăng nhập và đã favorite: Hiển thị icon favorite đã được đánh dấu

**Alternate Flows**:
- 2a. Listing không tồn tại: Hiển thị lỗi 404
- 2b. Listing đã bị xóa: Hiển thị lỗi "Listing không còn tồn tại"

**Postconditions**: User xem được chi tiết listing

**Business Rules**:
- Guest chỉ xem được thông tin cơ bản
- User có thể xem thêm seller contact và tạo offer

---

#### UC09: Add/Remove Favorite
**ID**: UC09  
**Actors**: User (Buyer)  
**Preconditions**: 
- User đã đăng nhập
- Listing tồn tại và có status AVAILABLE

**Trigger**: User click nút "Favorite" (heart icon)

**Main Flow - Add Favorite**:
1. User click nút Favorite trên listing
2. Hệ thống kiểm tra user chưa favorite listing này
3. Hệ thống tạo Favorite record
4. Hệ thống trả về success và cập nhật UI

**Main Flow - Remove Favorite**:
1. User click nút Favorite (đã được đánh dấu)
2. Hệ thống kiểm tra user đã favorite listing này
3. Hệ thống xóa Favorite record
4. Hệ thống trả về success và cập nhật UI

**Alternate Flows**:
- 2a. User đã favorite: Chuyển sang flow Remove Favorite
- 2b. Listing không tồn tại: Hiển thị lỗi 404

**Postconditions**: Favorite được thêm/xóa

**Business Rules**:
- User không thể favorite listing của chính mình
- Mỗi user chỉ có thể favorite một listing một lần

---

### 3.4 Feature 4: Real-time Chat

#### UC10: Send Message
**ID**: UC10  
**Actors**: User (Buyer/Seller)  
**Preconditions**: 
- User đã đăng nhập
- Conversation đã tồn tại hoặc được tạo mới
- User là member của conversation

**Trigger**: User nhập tin nhắn và click Send hoặc press Enter

**Main Flow**:
1. User mở conversation với một user khác
2. User nhập tin nhắn vào ô input
3. User click Send hoặc press Enter
4. Hệ thống validate tin nhắn (không rỗng, không quá dài)
5. Hệ thống tạo Message record trong database
6. Hệ thống gửi message qua WebSocket đến receiver
7. Hệ thống gửi confirmation qua WebSocket đến sender
8. UI cập nhật hiển thị tin nhắn mới

**Alternate Flows**:
- 1a. Conversation chưa tồn tại: Hệ thống tạo conversation mới
- 4a. Tin nhắn rỗng: Không gửi
- 4b. Tin nhắn quá dài (>1000 ký tự): Hiển thị lỗi "Tin nhắn quá dài"
- 6a. Receiver không online: Message được lưu, sẽ hiển thị khi receiver online

**Postconditions**: 
- Message được lưu trong database
- Message được gửi đến receiver qua WebSocket

**Business Rules**:
- Message phải được lưu database trước khi gửi qua WebSocket
- Mỗi conversation chỉ có 2 members (buyer và seller)
- User chỉ có thể chat với seller của listing hoặc buyer đã tạo offer

---

#### UC11: Receive Message
**ID**: UC11  
**Actors**: User  
**Preconditions**: 
- User đã đăng nhập và có WebSocket connection
- User là member của conversation

**Trigger**: Có tin nhắn mới từ user khác

**Main Flow**:
1. Sender gửi message (UC10)
2. Hệ thống gửi message qua WebSocket đến receiver
3. Receiver nhận message qua WebSocket
4. UI hiển thị tin nhắn mới
5. Hệ thống đánh dấu message là "delivered"
6. Nếu receiver đang mở conversation: Đánh dấu message là "read"

**Alternate Flows**:
- 2a. Receiver không online: Message được lưu, sẽ load khi receiver mở conversation
- 3a. WebSocket connection bị mất: Client tự động reconnect và load messages từ database

**Postconditions**: Receiver nhận được tin nhắn

**Business Rules**:
- Message phải được lưu database để đảm bảo không mất dữ liệu
- Read receipt chỉ được gửi khi receiver thực sự đọc message

---

### 3.5 Feature 5: Offers & Deals

#### UC12: Make Offer
**ID**: UC12  
**Actors**: User (Buyer)  
**Preconditions**: 
- User đã đăng nhập
- Listing tồn tại và có status AVAILABLE
- User không phải owner của listing

**Trigger**: User click "Tạo Offer" và điền giá

**Main Flow**:
1. User xem chi tiết listing
2. User click "Tạo Offer"
3. User nhập giá offer (phải <= giá listing)
4. User có thể nhập message (optional)
5. Hệ thống validate dữ liệu
6. Hệ thống tạo Offer record với status PENDING
7. Hệ thống gửi notification đến seller
8. Hệ thống trả về success

**Alternate Flows**:
- 3a. Giá offer > giá listing: Hiển thị lỗi "Giá offer không được vượt quá giá listing"
- 3b. Giá offer <= 0: Hiển thị lỗi "Giá phải lớn hơn 0"
- 5a. User đã tạo offer cho listing này: Hiển thị lỗi "Bạn đã tạo offer cho listing này"

**Postconditions**: 
- Offer được tạo với status PENDING
- Seller nhận được notification

**Business Rules**:
- Mỗi buyer chỉ có thể tạo 1 offer cho 1 listing (hoặc có thể tạo nhiều nhưng chỉ 1 PENDING)
- Offer chỉ có thể tạo khi listing có status AVAILABLE
- Giá offer không được vượt quá giá listing

---

#### UC13: Accept Offer
**ID**: UC13  
**Actors**: Seller (Owner)  
**Preconditions**: 
- User đã đăng nhập và là owner của listing
- Offer tồn tại và có status PENDING
- Listing có status AVAILABLE

**Trigger**: Seller click "Chấp nhận" trên offer

**Main Flow**:
1. Seller xem danh sách offers cho listing của mình
2. Seller click "Chấp nhận" trên một offer
3. Hệ thống validate offer và listing
4. Hệ thống cập nhật Offer status thành ACCEPTED
5. Hệ thống tự động reject các offers khác cho listing này
6. Hệ thống tạo Deal record với status PENDING
7. Hệ thống cập nhật Listing status thành RESERVED
8. Hệ thống gửi notification đến buyer
9. Hệ thống trả về success

**Alternate Flows**:
- 3a. Listing đã RESERVED hoặc SOLD: Hiển thị lỗi "Listing không còn available"
- 3b. Offer không tồn tại: Hiển thị lỗi 404

**Postconditions**: 
- Offer được accept
- Deal được tạo
- Listing chuyển sang RESERVED
- Các offers khác bị reject

**Business Rules**:
- Khi accept một offer, tất cả offers khác cho listing đó tự động reject
- Mỗi listing chỉ có thể có 1 deal active
- Listing chuyển sang RESERVED khi có deal

---

#### UC14: Create Meetup
**ID**: UC14  
**Actors**: Seller, Buyer (Deal participants)  
**Preconditions**: 
- User đã đăng nhập
- Deal tồn tại và user là participant (buyer hoặc seller)
- Deal có status PENDING hoặc CONFIRMED

**Trigger**: User click "Lên lịch Meetup"

**Main Flow**:
1. User xem chi tiết deal
2. User click "Lên lịch Meetup"
3. User điền thông tin: date, time, location, notes (optional)
4. Hệ thống validate dữ liệu (date phải trong tương lai)
5. Hệ thống tạo Meetup record
6. Hệ thống gửi notification đến participant còn lại
7. Hệ thống trả về success

**Alternate Flows**:
- 4a. Date trong quá khứ: Hiển thị lỗi "Ngày phải trong tương lai"
- 4b. Location trống: Hiển thị lỗi "Địa điểm không được để trống"

**Postconditions**: Meetup được tạo

**Business Rules**:
- Cả buyer và seller đều có thể tạo meetup
- Một deal có thể có nhiều meetups (nếu cần thay đổi)

---

#### UC15: Update Deal Status
**ID**: UC15  
**Actors**: Seller, Buyer (Deal participants)  
**Preconditions**: 
- User đã đăng nhập
- Deal tồn tại và user là participant

**Trigger**: User click "Xác nhận hoàn thành" hoặc "Hủy deal"

**Main Flow - Complete Deal**:
1. User xem chi tiết deal
2. User click "Xác nhận hoàn thành"
3. Hệ thống cập nhật Deal status thành COMPLETED
4. Hệ thống cập nhật Listing status thành SOLD
5. Hệ thống gửi notification đến participant còn lại
6. Hệ thống trả về success

**Main Flow - Cancel Deal**:
1. User xem chi tiết deal
2. User click "Hủy deal"
3. Hệ thống cập nhật Deal status thành CANCELLED
4. Hệ thống cập nhật Listing status thành AVAILABLE
5. Hệ thống gửi notification đến participant còn lại
6. Hệ thống trả về success

**Alternate Flows**:
- 2a. Deal đã COMPLETED: Không thể hủy
- 2b. Deal đã CANCELLED: Không thể complete

**Postconditions**: Deal status được cập nhật

**Business Rules**:
- Chỉ buyer hoặc seller của deal mới có thể update status
- Khi deal COMPLETED, listing chuyển sang SOLD
- Khi deal CANCELLED, listing chuyển về AVAILABLE

---

### 3.6 Feature 6: Moderation

#### UC16: Report Listing/User
**ID**: UC16  
**Actors**: User  
**Preconditions**: User đã đăng nhập

**Trigger**: User click "Báo cáo" trên listing hoặc profile user

**Main Flow**:
1. User click "Báo cáo" trên listing hoặc user profile
2. Hệ thống hiển thị form báo cáo
3. User chọn loại báo cáo (spam, inappropriate content, scam, etc.)
4. User nhập mô tả chi tiết (optional)
5. Hệ thống validate dữ liệu
6. Hệ thống tạo Report record với status PENDING
7. Hệ thống gửi notification đến admin
8. Hệ thống trả về success message

**Alternate Flows**:
- 3a. User không chọn loại báo cáo: Hiển thị lỗi "Vui lòng chọn loại báo cáo"
- 5a. User đã báo cáo item này: Hiển thị lỗi "Bạn đã báo cáo item này rồi" (hoặc cho phép update report)

**Postconditions**: Report được tạo và gửi đến admin

**Business Rules**:
- Mỗi user chỉ có thể báo cáo một item một lần (hoặc có thể update report cũ)
- Report được gửi đến admin để xem xét

---

#### UC17: Block User
**ID**: UC17  
**Actors**: User  
**Preconditions**: User đã đăng nhập

**Trigger**: User click "Chặn" trên profile user khác

**Main Flow**:
1. User xem profile của user khác
2. User click "Chặn user"
3. Hệ thống hiển thị xác nhận
4. User xác nhận
5. Hệ thống tạo Block record
6. Hệ thống ẩn các listings của user bị chặn
7. Hệ thống ngăn user bị chặn gửi message
8. Hệ thống trả về success

**Alternate Flows**:
- 2a. User đã chặn user này: Hiển thị "Đã chặn" và cho phép "Bỏ chặn"
- 4a. User hủy: Không thực hiện block

**Postconditions**: User bị chặn

**Business Rules**:
- User không thể chặn chính mình
- Block là một chiều (A chặn B không có nghĩa B chặn A)

---

#### UC18: Admin View Reports
**ID**: UC18  
**Actors**: Admin  
**Preconditions**: 
- User đã đăng nhập
- User có role ADMIN

**Trigger**: Admin truy cập trang quản lý reports

**Main Flow**:
1. Admin truy cập trang "Quản lý Báo cáo"
2. Hệ thống load danh sách reports với status PENDING
3. Hệ thống hiển thị danh sách với thông tin: loại báo cáo, item bị báo cáo, người báo cáo, ngày báo cáo
4. Admin có thể filter theo loại báo cáo, status
5. Admin click vào một report để xem chi tiết

**Alternate Flows**:
- 2a. Không có reports: Hiển thị "Không có báo cáo nào"

**Postconditions**: Admin xem được danh sách reports

**Business Rules**:
- Chỉ admin mới có thể xem tất cả reports
- Reports được sắp xếp theo ngày (mới nhất trước)

---

#### UC19: Admin Resolve Report
**ID**: UC19  
**Actors**: Admin  
**Preconditions**: 
- User đã đăng nhập và có role ADMIN
- Report tồn tại và có status PENDING

**Trigger**: Admin click "Giải quyết" trên report

**Main Flow**:
1. Admin xem chi tiết report
2. Admin xem xét nội dung bị báo cáo
3. Admin quyết định hành động:
   - Dismiss (bỏ qua): Report không hợp lệ
   - Warn user: Cảnh báo user
   - Ban user: Cấm user
   - Remove listing: Xóa listing
4. Admin chọn action và nhập lý do (optional)
5. Hệ thống cập nhật Report status thành RESOLVED
6. Hệ thống thực hiện action tương ứng (nếu có)
7. Hệ thống gửi notification đến reporter và user bị báo cáo
8. Hệ thống trả về success

**Alternate Flows**:
- 3a. Admin chọn "Dismiss": Chỉ cập nhật status, không có action khác
- 3b. Admin chọn "Ban user": Cập nhật user status thành BANNED

**Postconditions**: 
- Report được giải quyết
- Action được thực hiện (nếu có)

**Business Rules**:
- Chỉ admin mới có thể resolve reports
- Khi ban user, tất cả listings của user đó tự động bị ẩn
- User bị ban không thể đăng nhập

---

#### UC20: Admin Ban User
**ID**: UC20  
**Actors**: Admin  
**Preconditions**: 
- User đã đăng nhập và có role ADMIN
- Target user tồn tại

**Trigger**: Admin click "Cấm user" từ trang quản lý users hoặc từ report

**Main Flow**:
1. Admin xem danh sách users hoặc từ report detail
2. Admin click "Cấm user"
3. Hệ thống hiển thị xác nhận
4. Admin nhập lý do ban (optional)
5. Admin xác nhận
6. Hệ thống cập nhật user status thành BANNED
7. Hệ thống ẩn tất cả listings của user
8. Hệ thống gửi notification đến user bị ban
9. Hệ thống trả về success

**Alternate Flows**:
- 2a. User đã bị ban: Hiển thị "Đã bị cấm" và cho phép "Bỏ cấm"
- 4a. Admin hủy: Không thực hiện ban

**Postconditions**: User bị ban

**Business Rules**:
- Admin không thể ban chính mình
- User bị ban không thể đăng nhập
- Listings của user bị ban tự động ẩn

---

## 4. External Interface Requirements

### 4.1 User Interfaces
- **Web Interface**: Responsive web design, hỗ trợ desktop và mobile browsers
- **API Interface**: RESTful API với JSON format
- **WebSocket Interface**: Real-time communication cho chat

### 4.2 Hardware Interfaces
- Server với CPU, RAM đủ để chạy Django application
- Storage đủ để lưu hình ảnh và files

### 4.3 Software Interfaces
- **Database**: PostgreSQL 12+
- **Cache/PubSub**: Redis (optional)
- **Web Server**: Uvicorn (ASGI)
- **Reverse Proxy**: Nginx (production)

### 4.4 Communication Interfaces
- **HTTP/HTTPS**: REST API communication
- **WebSocket**: Real-time chat communication
- **Email**: SMTP server cho notifications (optional)

---

## 5. Non-Functional Requirements

### 5.1 Performance
- API response time < 500ms cho các endpoint chính
- Search trả về kết quả < 1s với 5000 listings
- WebSocket message delivery < 100ms
- Page load time < 2s

### 5.2 Security
- Password phải được hash (bcrypt/argon2)
- JWT token với expiration
- HTTPS trong production
- Input validation và sanitization
- SQL injection prevention (ORM)
- XSS prevention
- CSRF protection

### 5.3 Reliability
- Message chat phải được lưu database trước khi gửi
- WebSocket reconnection tự động
- Error handling và logging
- Database backup strategy

### 5.4 Maintainability
- Code tuân thủ PEP 8
- Tách layer rõ ràng (presentation/application/domain/infrastructure)
- Documentation đầy đủ
- Unit test coverage > 60%

### 5.5 Scalability
- Database indexing cho search
- Pagination cho danh sách
- Caching strategy (Redis)
- Stateless API design

---

## 6. Business Rules

### 6.1 Listing Rules
- Mỗi listing chỉ có 1 seller (owner)
- Listing mặc định có status AVAILABLE
- Listing chỉ có thể chỉnh sửa khi status AVAILABLE hoặc RESERVED
- Listing đã SOLD không thể chỉnh sửa hoặc xóa

### 6.2 Offer Rules
- Offer chỉ có thể tạo khi Listing ở trạng thái AVAILABLE
- Mỗi buyer chỉ có thể có 1 offer PENDING cho 1 listing
- Giá offer không được vượt quá giá listing
- Khi accept một offer, tất cả offers khác tự động reject

### 6.3 Deal Rules
- Deal chỉ có 1 buyer + 1 seller
- Khi Deal được tạo, Listing chuyển sang RESERVED
- Khi Deal COMPLETED, Listing chuyển sang SOLD
- Khi Deal CANCELLED, Listing chuyển về AVAILABLE

### 6.4 Chat Rules
- Conversation chỉ có 2 members (buyer và seller)
- User chỉ có thể chat với seller của listing hoặc buyer đã tạo offer
- Message phải được lưu database để đảm bảo không mất dữ liệu

### 6.5 Moderation Rules
- Mỗi user chỉ có thể báo cáo một item một lần
- Chỉ admin mới có thể resolve reports và ban users
- User bị ban không thể đăng nhập
- Listings của user bị ban tự động ẩn

### 6.6 User Rules
- Email phải unique trong hệ thống
- User mặc định có role USER
- User có thể vừa là buyer vừa là seller

---

## 7. Appendices

### 7.1 Glossary
- **Listing**: Tin đăng sản phẩm
- **Offer**: Lời đề nghị mua từ buyer
- **Deal**: Giao dịch được chốt giữa buyer và seller
- **Meetup**: Lịch hẹn gặp mặt để trao đổi hàng hóa
- **Conversation**: Cuộc trò chuyện giữa 2 users
- **Report**: Báo cáo về listing hoặc user không phù hợp

### 7.2 Use Case Summary
| UC ID | Use Case Name | Actor | Priority |
|-------|---------------|-------|----------|
| UC01 | Register | Guest | High |
| UC02 | Login | Guest | High |
| UC03 | Logout | User | High |
| UC04 | Create Listing | Seller | High |
| UC05 | Update Listing | Seller | High |
| UC06 | Delete Listing | Seller/Admin | Medium |
| UC07 | Search & Filter | Guest/User | High |
| UC08 | View Listing Details | Guest/User | High |
| UC09 | Add/Remove Favorite | User | Medium |
| UC10 | Send Message | User | High |
| UC11 | Receive Message | User | High |
| UC12 | Make Offer | Buyer | High |
| UC13 | Accept Offer | Seller | High |
| UC14 | Create Meetup | Buyer/Seller | Medium |
| UC15 | Update Deal Status | Buyer/Seller | High |
| UC16 | Report Listing/User | User | Medium |
| UC17 | Block User | User | Low |
| UC18 | Admin View Reports | Admin | High |
| UC19 | Admin Resolve Report | Admin | High |
| UC20 | Admin Ban User | Admin | High |

---

**End of Document**

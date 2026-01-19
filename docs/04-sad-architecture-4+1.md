# Software Architecture Document (SAD)
## OldGoods Marketplace - 4+1 Views

**Version**: 1.0  
**Date**: 2024  
**Architecture Style**: Layered Architecture + Event-Driven (WebSocket)

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Architectural Goals & Constraints](#2-architectural-goals--constraints)
3. [+1 Scenarios View](#3-1-scenarios-view)
4. [Logical View](#4-logical-view)
5. [Process View](#5-process-view)
6. [Development View](#6-development-view)
7. [Physical View](#7-physical-view)
8. [Architectural Decisions](#8-architectural-decisions)

---

## 1. Introduction

### 1.1 Purpose
Tài liệu này mô tả kiến trúc phần mềm của hệ thống OldGoods Marketplace sử dụng mô hình 4+1 Views của Philippe Kruchten. Mô hình này cung cấp nhiều góc nhìn khác nhau về hệ thống để các stakeholders khác nhau có thể hiểu và đánh giá kiến trúc.

### 1.2 Scope
Tài liệu bao gồm:
- 4 views chính: Logical, Process, Development, Physical
- +1 Scenarios view để "neo" các views khác
- Architectural decisions và rationale

### 1.3 Stakeholders
- Developers: Hiểu code structure và implementation
- Architects: Đánh giá và review kiến trúc
- Project Managers: Hiểu dependencies và risks
- Testers: Hiểu data flow để viết tests

---

## 2. Architectural Goals & Constraints

### 2.1 Goals

#### 2.1.1 Maintainability
- **Goal**: Code dễ đọc, dễ hiểu, dễ maintain
- **Rationale**: Dự án học tập cần code rõ ràng để review và học hỏi
- **Approach**: Layered architecture, clear separation of concerns, comprehensive documentation

#### 2.1.2 Scalability
- **Goal**: Hệ thống có thể mở rộng khi cần
- **Rationale**: Có thể cần handle nhiều users và data trong tương lai
- **Approach**: Stateless API design, database indexing, caching strategy

#### 2.1.3 Realtime Communication
- **Goal**: Chat realtime với WebSocket
- **Rationale**: Yêu cầu chính của hệ thống
- **Approach**: Django Channels với WebSocket support

#### 2.1.4 Security
- **Goal**: Bảo mật cơ bản cho user data và authentication
- **Rationale**: Yêu cầu bắt buộc cho bất kỳ hệ thống nào
- **Approach**: JWT authentication, password hashing, input validation

### 2.2 Constraints

#### 2.2.1 Technology Constraints
- **Django**: Framework bắt buộc
- **PostgreSQL**: Database bắt buộc
- **Python 3.10+**: Runtime requirement

#### 2.2.2 Time Constraints
- **4 Sprints**: Timeline cố định
- **MVP Focus**: Chỉ implement features cần thiết

#### 2.2.3 Resource Constraints
- **Team Size**: Nhóm nhỏ (3-5 người)
- **Budget**: Không có budget cho cloud services trả phí

---

## 3. +1 Scenarios View

Scenarios view mô tả các use case quan trọng nhất để "neo" các views khác. Các scenarios này được sử dụng để validate kiến trúc và đảm bảo tất cả các views đều hỗ trợ các use cases này.

### 3.1 Scenario 1: Create Listing

**Description**: Seller tạo một listing mới với hình ảnh

**Actors**: Seller

**Flow**:
1. Seller đăng nhập và truy cập trang "Đăng tin"
2. Seller điền thông tin (title, description, category, price, location)
3. Seller upload 1-5 hình ảnh
4. System validate dữ liệu
5. System lưu hình ảnh vào storage
6. System tạo Listing record trong database
7. System tạo các ListingImage records
8. System trả về success và redirect đến trang chi tiết

**Architectural Concerns**:
- **Logical**: Listing entity, ListingImage entity, relationships
- **Process**: HTTP request → validation → storage → database transaction
- **Development**: Listing model, ListingSerializer, ListingViewSet
- **Physical**: Web server → File storage → Database server

**Validation**: Kiến trúc phải hỗ trợ file upload, validation, và database transactions

---

### 3.2 Scenario 2: Search Listings

**Description**: User tìm kiếm listings với keyword và filters

**Actors**: Guest, User

**Flow**:
1. User nhập keyword và chọn filters (category, price range, location)
2. System query database với các điều kiện
3. System sử dụng indexes để optimize query
4. System paginate kết quả
5. System trả về danh sách listings

**Architectural Concerns**:
- **Logical**: Listing entity, Category entity, search logic
- **Process**: HTTP GET request → Database query với filters → Pagination → Response
- **Development**: Search filters, ListingViewSet với filtering, Pagination
- **Physical**: Web server → Database server (với indexes)

**Validation**: Kiến trúc phải hỗ trợ efficient search với indexes và pagination

---

### 3.3 Scenario 3: Send Message (WebSocket)

**Description**: Buyer gửi tin nhắn realtime cho Seller

**Actors**: Buyer, Seller

**Flow**:
1. Buyer mở conversation với Seller
2. Buyer nhập tin nhắn và click Send
3. Client gửi message qua WebSocket
4. Server nhận message qua WebSocket consumer
5. Server validate message
6. Server lưu message vào database (transaction)
7. Server gửi message qua WebSocket đến Seller (nếu online)
8. Server gửi confirmation đến Buyer
9. Client hiển thị tin nhắn mới

**Architectural Concerns**:
- **Logical**: Conversation entity, Message entity, relationships
- **Process**: WebSocket connection → Message consumer → Database write → WebSocket broadcast
- **Development**: ChatConsumer (Django Channels), Message model, WebSocket routing
- **Physical**: WebSocket server (ASGI) → Database server → Redis (channel layers)

**Validation**: Kiến trúc phải hỗ trợ WebSocket, message persistence, và realtime delivery

---

### 3.4 Scenario 4: Offer → Accept → Create Deal

**Description**: Buyer tạo offer, Seller accept, hệ thống tạo deal

**Actors**: Buyer, Seller

**Flow**:
1. Buyer xem listing và click "Tạo Offer"
2. Buyer nhập giá offer và submit
3. System tạo Offer record với status PENDING
4. System gửi notification đến Seller
5. Seller xem offers và click "Chấp nhận"
6. System validate offer và listing
7. System update Offer status thành ACCEPTED (transaction)
8. System reject các offers khác cho listing này (transaction)
9. System tạo Deal record với status PENDING (transaction)
10. System update Listing status thành RESERVED (transaction)
11. System gửi notification đến Buyer

**Architectural Concerns**:
- **Logical**: Offer entity, Deal entity, Listing entity, business rules
- **Process**: HTTP POST → Business logic → Database transactions → Notifications
- **Development**: OfferService, DealService, transaction management
- **Physical**: Web server → Database server (ACID transactions)

**Validation**: Kiến trúc phải hỗ trợ transactions để đảm bảo data consistency

---

## 4. Logical View

Logical view mô tả các entities, relationships, và business logic của hệ thống. Đây là domain model của ứng dụng.

### 4.1 Domain Model Overview

Hệ thống được tổ chức thành các **Aggregates** (theo DDD - Domain-Driven Design):

1. **User Aggregate**: User, Profile
2. **Listing Aggregate**: Listing, ListingImage, Category, Favorite
3. **Conversation Aggregate**: Conversation, Message, ConversationMember
4. **Deal Aggregate**: Offer, Deal, Meetup
5. **Moderation Aggregate**: Report, Block

### 4.2 Core Entities

#### 4.2.1 User Aggregate

**User** (Root Entity)
- id: UUID
- email: String (unique)
- password_hash: String
- role: Enum (USER, ADMIN)
- status: Enum (ACTIVE, BANNED)
- created_at: DateTime
- updated_at: DateTime

**Profile**
- id: UUID
- user: ForeignKey → User (one-to-one)
- full_name: String
- phone: String (optional)
- location: String (optional)
- avatar: File (optional)
- bio: Text (optional)

**Relationships**:
- User 1:1 Profile
- User 1:N Listing (as seller)
- User 1:N Favorite
- User 1:N Conversation (through ConversationMember)
- User 1:N Offer (as buyer)
- User 1:N Report (as reporter)

---

#### 4.2.2 Listing Aggregate

**Category**
- id: UUID
- name: String (unique)
- slug: String (unique)
- description: Text (optional)
- parent: ForeignKey → Category (self-referential, optional, for subcategories)

**Listing** (Root Entity)
- id: UUID
- seller: ForeignKey → User
- category: ForeignKey → Category
- title: String
- description: Text
- price: Decimal
- condition: Enum (NEW, LIKE_NEW, USED, POOR)
- location: String
- status: Enum (AVAILABLE, RESERVED, SOLD, EXPIRED)
- created_at: DateTime
- updated_at: DateTime

**ListingImage**
- id: UUID
- listing: ForeignKey → Listing (many-to-one)
- image: File
- order: Integer (for ordering images)
- created_at: DateTime

**Favorite**
- id: UUID
- user: ForeignKey → User
- listing: ForeignKey → Listing
- created_at: DateTime
- Unique constraint: (user, listing)

**Relationships**:
- Category 1:N Listing
- User 1:N Listing (as seller)
- Listing 1:N ListingImage
- Listing 1:N Favorite
- Listing 1:N Offer
- Listing 1:N Report

---

#### 4.2.3 Conversation Aggregate

**Conversation** (Root Entity)
- id: UUID
- listing: ForeignKey → Listing (optional, for listing-based conversations)
- created_at: DateTime
- updated_at: DateTime

**ConversationMember**
- id: UUID
- conversation: ForeignKey → Conversation
- user: ForeignKey → User
- joined_at: DateTime
- Unique constraint: (conversation, user)

**Message**
- id: UUID
- conversation: ForeignKey → Conversation
- sender: ForeignKey → User
- content: Text
- read_at: DateTime (optional)
- sent_at: DateTime

**Relationships**:
- Conversation N:M User (through ConversationMember)
- Conversation 1:N Message
- Listing 1:N Conversation (optional)

---

#### 4.2.4 Deal Aggregate

**Offer**
- id: UUID
- listing: ForeignKey → Listing
- buyer: ForeignKey → User
- price: Decimal
- message: Text (optional)
- status: Enum (PENDING, ACCEPTED, REJECTED, CANCELLED)
- created_at: DateTime
- updated_at: DateTime

**Deal** (Root Entity)
- id: UUID
- listing: ForeignKey → Listing
- buyer: ForeignKey → User
- seller: ForeignKey → User
- offer: ForeignKey → Offer
- status: Enum (PENDING, CONFIRMED, COMPLETED, CANCELLED)
- created_at: DateTime
- updated_at: DateTime

**Meetup**
- id: UUID
- deal: ForeignKey → Deal
- scheduled_at: DateTime
- location: String
- notes: Text (optional)
- created_at: DateTime

**Relationships**:
- Listing 1:N Offer
- User 1:N Offer (as buyer)
- Offer 1:1 Deal
- Deal 1:N Meetup
- Listing 1:1 Deal (at a time, when RESERVED)

---

#### 4.2.5 Moderation Aggregate

**Report**
- id: UUID
- reporter: ForeignKey → User
- reported_listing: ForeignKey → Listing (optional)
- reported_user: ForeignKey → User (optional)
- report_type: Enum (SPAM, INAPPROPRIATE, SCAM, OTHER)
- description: Text (optional)
- status: Enum (PENDING, RESOLVED, DISMISSED)
- resolved_by: ForeignKey → User (optional, admin)
- resolved_at: DateTime (optional)
- created_at: DateTime

**Block**
- id: UUID
- blocker: ForeignKey → User
- blocked_user: ForeignKey → User
- created_at: DateTime
- Unique constraint: (blocker, blocked_user)

**Relationships**:
- User 1:N Report (as reporter)
- User 1:N Report (as reported_user)
- Listing 1:N Report
- User 1:N Block (as blocker)
- User 1:N Block (as blocked_user)

---

### 4.3 Value Objects

**Money**
- amount: Decimal
- currency: String (default: "VND")

**Location**
- address: String
- city: String
- district: String (optional)
- coordinates: Point (optional, for future geolocation)

---

### 4.4 Domain Services

**ListingService**: Business logic cho listing operations
- validate_listing_creation()
- update_listing_status()
- expire_old_listings()

**OfferService**: Business logic cho offer operations
- create_offer()
- accept_offer()
- reject_offer()

**DealService**: Business logic cho deal operations
- create_deal_from_offer()
- complete_deal()
- cancel_deal()

**ChatService**: Business logic cho chat operations
- create_conversation()
- send_message()
- mark_as_read()

---

## 5. Process View

Process view mô tả runtime behavior của hệ thống, bao gồm các processes, threads, và interactions giữa các components.

### 5.1 Runtime Architecture

Hệ thống chạy với các processes chính:

1. **Web Server Process** (Gunicorn/Uvicorn)
   - Handle HTTP requests
   - Handle WebSocket connections
   - Run Django application

2. **Database Process** (PostgreSQL)
   - Store persistent data
   - Handle transactions

3. **Channel Layer Process** (Redis)
   - Manage WebSocket connections
   - Route messages between consumers

### 5.2 HTTP Request Flow

```
Client → Nginx (Reverse Proxy) → Gunicorn/Uvicorn → Django Application
                                                      ↓
                                              Django REST Framework
                                                      ↓
                                              Application Services
                                                      ↓
                                              Domain Services
                                                      ↓
                                              Repository Layer
                                                      ↓
                                              PostgreSQL Database
```

**Example: Create Listing Request**

1. Client sends POST /api/listings/ với JSON data và images
2. Nginx receives request và forward đến Gunicorn
3. Django URL router routes đến ListingViewSet
4. ViewSet validates request (authentication, permissions)
5. ListingSerializer validates data
6. ListingService.create_listing() executes business logic
7. FileStorageService.save_images() saves images
8. Repository saves Listing và ListingImage records (transaction)
9. Response returned to client

### 5.3 WebSocket Message Flow

```
Client (WebSocket) → ASGI Server → Django Channels → ChatConsumer
                                                          ↓
                                                  ChatService
                                                          ↓
                                                  Database (Save Message)
                                                          ↓
                                                  Channel Layer (Redis)
                                                          ↓
                                                  Receiver's Consumer
                                                          ↓
                                                  Client (WebSocket)
```

**Example: Send Chat Message**

1. Client establishes WebSocket connection với authentication token
2. Client sends message: `{"type": "send_message", "conversation_id": "...", "content": "..."}`
3. ASGI server routes đến ChatConsumer
4. ChatConsumer validates message và user permissions
5. ChatService.send_message() executes business logic
6. Message saved to database (transaction)
7. ChatConsumer broadcasts message qua channel layer
8. Receiver's consumer receives message và sends to client
9. Client receives message và updates UI

### 5.4 Concurrency Model

#### 5.4.1 HTTP Requests
- **Model**: Multi-threaded hoặc async (tùy server)
- **Concurrency**: Gunicorn workers handle multiple requests
- **Database**: Connection pooling để handle concurrent queries
- **Stateless**: Mỗi request độc lập, không share state

#### 5.4.2 WebSocket Connections
- **Model**: Async (Django Channels)
- **Concurrency**: Mỗi WebSocket connection là một async task
- **Channel Layer**: Redis manages message routing
- **Scalability**: Multiple server instances có thể share channel layer

### 5.5 Background Tasks

**Listing Expiration Task** (Future)
- Chạy định kỳ (cron job hoặc Celery)
- Tìm các listings cũ (ví dụ: > 30 ngày)
- Update status thành EXPIRED

**Notification Task** (Future)
- Gửi email notifications khi có offer mới, message mới, etc.
- Sử dụng Celery hoặc Django background tasks

---

## 6. Development View

Development view mô tả cấu trúc code, modules, và dependencies từ góc nhìn của developer.

### 6.1 Layered Architecture

Hệ thống được tổ chức theo **Layered Architecture** với các layers:

```
┌─────────────────────────────────────┐
│   Presentation Layer                │
│   (HTTP/WebSocket Endpoints)       │
├─────────────────────────────────────┤
│   Application Layer                 │
│   (Services, Use Cases)             │
├─────────────────────────────────────┤
│   Domain Layer                      │
│   (Entities, Value Objects, Rules)  │
├─────────────────────────────────────┤
│   Infrastructure Layer              │
│   (Database, Storage, External)    │
└─────────────────────────────────────┘
```

### 6.2 Module Structure

```
oldgoods_marketplace/
├── manage.py
├── oldgoods_marketplace/          # Main project package
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py                     # ASGI config for WebSocket
│   ├── wsgi.py
│   └── routing.py                  # WebSocket routing
│
├── accounts/                       # User management app
│   ├── models.py                   # User, Profile
│   ├── views.py                    # API views
│   ├── serializers.py
│   ├── urls.py
│   └── admin.py
│
├── listings/                       # Product listings app
│   ├── models.py                   # Listing, Category, ListingImage, Favorite
│   ├── views.py                    # ListingViewSet
│   ├── serializers.py
│   ├── filters.py                  # Search filters
│   ├── urls.py
│   └── admin.py
│
├── chat/                           # Chat app (Django Channels)
│   ├── models.py                   # Conversation, Message, ConversationMember
│   ├── consumers.py                # ChatConsumer (WebSocket)
│   ├── serializers.py
│   └── routing.py                  # WebSocket routes
│
├── deals/                          # Offers & Deals app
│   ├── models.py                   # Offer, Deal, Meetup
│   ├── views.py                    # OfferViewSet, DealViewSet
│   ├── serializers.py
│   ├── services.py                 # OfferService, DealService
│   ├── urls.py
│   └── admin.py
│
├── moderation/                     # Reports & Blocks app
│   ├── models.py                   # Report, Block
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── admin.py
│
├── admin_panel/                    # Admin moderation app
│   ├── views.py                    # Admin views
│   ├── serializers.py
│   └── urls.py
│
├── core/                           # Shared utilities
│   ├── permissions.py              # Custom permissions
│   ├── pagination.py               # Custom pagination
│   ├── filters.py                  # Shared filters
│   ├── exceptions.py               # Custom exceptions
│   └── utils.py                    # Helper functions
│
└── infrastructure/                 # External services
    ├── storage.py                  # File storage (local/S3)
    ├── email.py                    # Email notifications
    └── cache.py                    # Caching utilities
```

### 6.3 Dependency Rules

**Dependency Flow** (từ trên xuống dưới):
- Presentation → Application → Domain
- Application → Infrastructure
- Domain → (không phụ thuộc gì)

**Rules**:
- Domain layer không phụ thuộc vào Infrastructure hoặc Presentation
- Application layer không phụ thuộc vào Presentation
- Infrastructure có thể phụ thuộc vào Domain (cho implementations)

### 6.4 Technology Stack

**Backend Framework**:
- Django 4.2+
- Django REST Framework
- Django Channels (WebSocket)

**Database**:
- PostgreSQL 12+
- Django ORM

**Authentication**:
- JWT (djangorestframework-simplejwt)

**File Storage**:
- Django FileField (local) hoặc django-storages (S3)

**Channel Layer**:
- Redis (production) hoặc InMemoryChannelLayer (development)

**Testing**:
- pytest
- pytest-django
- pytest-asyncio (cho WebSocket tests)

---

## 7. Physical View

Physical view mô tả deployment architecture, hardware, và network topology.

### 7.1 Deployment Architecture (MVP)

```
┌─────────────────────────────────────────┐
│         Internet/Network                 │
└─────────────────┬───────────────────────┘
                  │
         ┌────────┴────────┐
         │   Nginx (Proxy)  │
         └────────┬─────────┘
                  │
    ┌─────────────┴─────────────┐
    │                           │
┌───┴────┐              ┌───────┴──────┐
│ Django │              │   Redis      │
│  App   │              │ (Channels)    │
│(Gunicorn)             └──────────────┘
└───┬────┘
    │
┌───┴──────────┐
│ PostgreSQL   │
│  Database    │
└──────────────┘
```

### 7.2 Server Components

#### 7.2.1 Web Server
- **Component**: Nginx (Reverse Proxy)
- **Port**: 80 (HTTP), 443 (HTTPS)
- **Role**: 
  - Reverse proxy cho Django app
  - Serve static files
  - SSL termination

#### 7.2.2 Application Server
- **Component**: Gunicorn/Uvicorn
- **Port**: 8000 (internal)
- **Role**: 
  - Run Django application
  - Handle HTTP requests
  - Handle WebSocket connections (ASGI)

#### 7.2.3 Database Server
- **Component**: PostgreSQL
- **Port**: 5432
- **Role**: 
  - Store persistent data
  - Handle transactions
  - Provide ACID guarantees

#### 7.2.4 Channel Layer
- **Component**: Redis
- **Port**: 6379
- **Role**: 
  - Manage WebSocket connections
  - Route messages between consumers
  - Support horizontal scaling

### 7.3 File Storage

**Local Storage** (MVP):
- Directory: `/media/listings/`
- Served by: Nginx hoặc Django (development)

**Cloud Storage** (Future):
- AWS S3 hoặc similar
- CDN for images

### 7.4 Environment Configuration

**Development**:
- Single server với tất cả components
- SQLite hoặc PostgreSQL local
- InMemoryChannelLayer (không cần Redis)

**Production**:
- Separate servers cho database và Redis (nếu scale)
- Environment variables cho secrets
- SSL certificates cho HTTPS

### 7.5 Network Ports

| Component | Port | Protocol | Access |
|-----------|------|----------|--------|
| Nginx | 80, 443 | HTTP/HTTPS | Public |
| Django App | 8000 | HTTP/WebSocket | Internal |
| PostgreSQL | 5432 | TCP | Internal |
| Redis | 6379 | TCP | Internal |

### 7.6 Scaling Considerations

**Vertical Scaling**:
- Tăng CPU/RAM cho server
- Tăng database resources

**Horizontal Scaling**:
- Multiple Django app instances behind load balancer
- Shared Redis channel layer
- Database replication (read replicas)

---

## 8. Architectural Decisions

### 8.1 AD-001: Layered Architecture

**Decision**: Sử dụng Layered Architecture với 4 layers

**Rationale**:
- Dễ hiểu và maintain
- Separation of concerns rõ ràng
- Phù hợp với Django structure

**Alternatives Considered**:
- Microservices: Quá phức tạp cho MVP
- Monolithic: Không đủ structure

**Consequences**:
- Code organization rõ ràng
- Dễ test từng layer
- Có thể refactor từng layer độc lập

---

### 8.2 AD-002: Django Channels for WebSocket

**Decision**: Sử dụng Django Channels cho WebSocket support

**Rationale**:
- Tích hợp tốt với Django
- Support async/await
- Channel layers hỗ trợ scaling

**Alternatives Considered**:
- Socket.io: Cần Node.js server riêng
- Tornado: Không tích hợp với Django

**Consequences**:
- Cần Redis cho channel layers
- ASGI server required
- Learning curve cho team

---

### 8.3 AD-003: PostgreSQL as Database

**Decision**: Sử dụng PostgreSQL

**Rationale**:
- Yêu cầu bắt buộc của dự án
- ACID compliance
- Good performance với indexes
- Support JSON fields nếu cần

**Alternatives Considered**:
- MySQL: Similar, nhưng PostgreSQL tốt hơn cho complex queries
- MongoDB: NoSQL không phù hợp với relational data

**Consequences**:
- Cần setup PostgreSQL server
- ORM migrations với Django

---

### 8.4 AD-004: JWT for Authentication

**Decision**: Sử dụng JWT tokens cho authentication

**Rationale**:
- Stateless authentication (phù hợp với scaling)
- Không cần server-side session storage
- Standard và secure

**Alternatives Considered**:
- Session-based: Cần session storage, không stateless
- OAuth2: Quá phức tạp cho MVP

**Consequences**:
- Token expiration management
- Refresh token strategy
- Token revocation (nếu cần)

---

### 8.5 AD-005: REST API + WebSocket

**Decision**: REST API cho CRUD operations, WebSocket cho realtime chat

**Rationale**:
- REST phù hợp cho CRUD
- WebSocket phù hợp cho realtime communication
- Separation of concerns

**Alternatives Considered**:
- GraphQL: Quá phức tạp cho MVP
- Pure WebSocket: Không phù hợp cho CRUD

**Consequences**:
- Cần maintain cả REST và WebSocket
- Different authentication cho WebSocket

---

## 9. Quality Attributes

### 9.1 Performance
- **Strategy**: Database indexing, pagination, caching
- **Mechanisms**: PostgreSQL indexes, Redis cache, query optimization

### 9.2 Security
- **Strategy**: Authentication, authorization, input validation
- **Mechanisms**: JWT, password hashing, Django security middleware

### 9.3 Reliability
- **Strategy**: Error handling, transactions, logging
- **Mechanisms**: Database transactions, exception handling, logging

### 9.4 Maintainability
- **Strategy**: Layered architecture, documentation, testing
- **Mechanisms**: Code organization, docstrings, unit tests

---

## 10. References

- Django Documentation: https://docs.djangoproject.com/
- Django Channels: https://channels.readthedocs.io/
- Django REST Framework: https://www.django-rest-framework.org/
- 4+1 Views: Philippe Kruchten, "Architectural Blueprints—The 4+1 View Model of Software Architecture"

---

**End of Document**

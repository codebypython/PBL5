# Database Design
## OldGoods Marketplace

**Version**: 1.0  
**Date**: 2024  
**Database**: PostgreSQL 12+

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Entity Relationship Diagram (ERD)](#2-entity-relationship-diagram-erd)
3. [Data Dictionary](#3-data-dictionary)
4. [Indexes Strategy](#4-indexes-strategy)
5. [Django ORM Models](#5-django-orm-models)
6. [Migration Strategy](#6-migration-strategy)
7. [Data Integrity Constraints](#7-data-integrity-constraints)

---

## 1. Introduction

### 1.1 Purpose
Tài liệu này mô tả thiết kế database cho hệ thống OldGoods Marketplace, bao gồm ERD, data dictionary, indexes, và Django ORM mapping.

### 1.2 Database Overview
- **Database System**: PostgreSQL 12+
- **Character Encoding**: UTF-8
- **Naming Convention**: snake_case cho tables và columns
- **Primary Keys**: UUID (uuid4) cho tất cả tables
- **Timestamps**: created_at và updated_at cho audit trail

---

## 2. Entity Relationship Diagram (ERD)

### 2.1 High-Level ERD

```
┌──────────┐         ┌──────────┐
│   User   │─────────│ Profile  │ (1:1)
└────┬─────┘         └──────────┘
     │
     │ (1:N)
     ├─────────────────────────────────┐
     │                                   │
┌────▼─────┐                      ┌──────▼──────┐
│ Listing  │                      │  Favorite   │
└────┬─────┘                      └─────────────┘
     │
     │ (1:N)
     ├──────────────┬──────────────┬──────────────┐
     │              │              │              │
┌────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
│ListingImg│  │  Offer    │  │Conversation│  │  Report   │
└──────────┘  └─────┬─────┘  └─────┬──────┘  └───────────┘
                    │              │
                    │ (1:1)        │ (1:N)
                    │              │
              ┌─────▼─────┐  ┌─────▼──────┐
              │   Deal    │  │  Message   │
              └─────┬─────┘  └─────────────┘
                    │
                    │ (1:N)
                    │
              ┌─────▼─────┐
              │  Meetup   │
              └───────────┘

┌──────────┐
│ Category │───────┐
└──────────┘       │ (1:N)
                   │
              ┌────▼─────┐
              │ Listing  │
              └──────────┘

┌──────────┐         ┌──────────┐
│   User   │────────│  Block   │ (N:M, self-referential)
└──────────┘         └──────────┘
```

### 2.2 Detailed Relationships

**User ↔ Profile**: One-to-One
- Mỗi User có 1 Profile
- Profile không thể tồn tại không có User

**User ↔ Listing**: One-to-Many
- Mỗi User có thể có nhiều Listings (as seller)
- Mỗi Listing chỉ có 1 seller

**User ↔ Favorite**: One-to-Many
- Mỗi User có thể favorite nhiều Listings
- Mỗi Listing có thể được favorite bởi nhiều Users
- Unique constraint: (user_id, listing_id)

**Listing ↔ ListingImage**: One-to-Many
- Mỗi Listing có thể có nhiều Images (1-5)
- Mỗi Image chỉ thuộc về 1 Listing

**Listing ↔ Category**: Many-to-One
- Mỗi Listing thuộc về 1 Category
- Mỗi Category có thể có nhiều Listings

**Listing ↔ Offer**: One-to-Many
- Mỗi Listing có thể có nhiều Offers
- Mỗi Offer chỉ thuộc về 1 Listing

**Offer ↔ Deal**: One-to-One
- Mỗi Offer có thể tạo 1 Deal (khi accepted)
- Mỗi Deal được tạo từ 1 Offer

**Deal ↔ Meetup**: One-to-Many
- Mỗi Deal có thể có nhiều Meetups (nếu cần reschedule)
- Mỗi Meetup chỉ thuộc về 1 Deal

**Conversation ↔ User**: Many-to-Many (through ConversationMember)
- Mỗi Conversation có 2 Users (buyer và seller)
- Mỗi User có thể có nhiều Conversations

**Message ↔ Conversation**: Many-to-One
- Mỗi Message thuộc về 1 Conversation
- Mỗi Conversation có nhiều Messages

**User ↔ Block**: Many-to-Many (self-referential)
- Mỗi User có thể block nhiều Users
- Unique constraint: (blocker_id, blocked_user_id)

**User ↔ Report**: One-to-Many (as reporter)
- Mỗi User có thể tạo nhiều Reports
- Mỗi Report chỉ có 1 reporter

**Listing ↔ Report**: One-to-Many
- Mỗi Listing có thể bị báo cáo nhiều lần
- Mỗi Report có thể báo cáo 1 Listing (optional)

**User ↔ Report**: One-to-Many (as reported_user)
- Mỗi User có thể bị báo cáo nhiều lần
- Mỗi Report có thể báo cáo 1 User (optional)

---

## 3. Data Dictionary

### 3.1 Table: users

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email (login) |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password (bcrypt/argon2) |
| role | VARCHAR(20) | NOT NULL, DEFAULT 'USER' | Role: USER, ADMIN |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'ACTIVE' | Status: ACTIVE, BANNED |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Account active flag |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (email)
- INDEX (status) - for filtering banned users
- INDEX (role) - for admin queries

---

### 3.2 Table: profiles

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique identifier |
| user_id | UUID | FOREIGN KEY → users(id), UNIQUE, NOT NULL | Reference to User |
| full_name | VARCHAR(255) | NOT NULL | User's full name |
| phone | VARCHAR(20) | NULL | Phone number (optional) |
| location | VARCHAR(255) | NULL | Location/address (optional) |
| avatar | VARCHAR(500) | NULL | Avatar image path (optional) |
| bio | TEXT | NULL | User bio (optional) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (user_id)
- FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE

---

### 3.3 Table: categories

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique identifier |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Category name |
| slug | VARCHAR(100) | UNIQUE, NOT NULL | URL-friendly slug |
| description | TEXT | NULL | Category description (optional) |
| parent_id | UUID | FOREIGN KEY → categories(id), NULL | Parent category (for subcategories) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (name)
- UNIQUE INDEX (slug)
- INDEX (parent_id) - for hierarchical queries
- FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL

---

### 3.4 Table: listings

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique identifier |
| seller_id | UUID | FOREIGN KEY → users(id), NOT NULL | Seller (owner) |
| category_id | UUID | FOREIGN KEY → categories(id), NOT NULL | Category |
| title | VARCHAR(255) | NOT NULL | Listing title |
| description | TEXT | NOT NULL | Detailed description |
| price | DECIMAL(12,2) | NOT NULL, CHECK (price > 0) | Price in VND |
| condition | VARCHAR(20) | NOT NULL | Condition: NEW, LIKE_NEW, USED, POOR |
| location | VARCHAR(255) | NOT NULL | Location/address |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'AVAILABLE' | Status: AVAILABLE, RESERVED, SOLD, EXPIRED |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (seller_id) - for user's listings
- INDEX (category_id) - for category filtering
- INDEX (status) - for filtering by status
- INDEX (price) - for price sorting/filtering
- INDEX (created_at) - for sorting by date
- INDEX (location) - for location filtering (if needed)
- COMPOSITE INDEX (status, category_id) - for common queries
- COMPOSITE INDEX (status, created_at DESC) - for listing pages
- FOREIGN KEY (seller_id) REFERENCES users(id) ON DELETE CASCADE
- FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT

---

### 3.5 Table: listing_images

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique identifier |
| listing_id | UUID | FOREIGN KEY → listings(id), NOT NULL | Reference to Listing |
| image | VARCHAR(500) | NOT NULL | Image file path |
| order | INTEGER | NOT NULL, DEFAULT 0 | Display order (0-4) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (listing_id) - for fetching listing images
- COMPOSITE INDEX (listing_id, order) - for ordered display
- FOREIGN KEY (listing_id) REFERENCES listings(id) ON DELETE CASCADE

**Constraints**:
- CHECK (order >= 0 AND order <= 4) - max 5 images

---

### 3.6 Table: favorites

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique identifier |
| user_id | UUID | FOREIGN KEY → users(id), NOT NULL | User who favorited |
| listing_id | UUID | FOREIGN KEY → listings(id), NOT NULL | Listing favorited |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (user_id, listing_id) - prevent duplicate favorites
- INDEX (user_id) - for user's favorites
- INDEX (listing_id) - for listing's favorite count
- FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
- FOREIGN KEY (listing_id) REFERENCES listings(id) ON DELETE CASCADE

---

### 3.7 Table: conversations

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique identifier |
| listing_id | UUID | FOREIGN KEY → listings(id), NULL | Related listing (optional) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (listing_id) - for listing-based conversations
- INDEX (updated_at DESC) - for sorting conversations
- FOREIGN KEY (listing_id) REFERENCES listings(id) ON DELETE SET NULL

---

### 3.8 Table: conversation_members

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique identifier |
| conversation_id | UUID | FOREIGN KEY → conversations(id), NOT NULL | Reference to Conversation |
| user_id | UUID | FOREIGN KEY → users(id), NOT NULL | Member user |
| joined_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Join timestamp |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (conversation_id, user_id) - prevent duplicate members
- INDEX (conversation_id) - for conversation members
- INDEX (user_id) - for user's conversations
- FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
- FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE

**Constraints**:
- CHECK: Mỗi conversation chỉ có tối đa 2 members (enforced in application logic)

---

### 3.9 Table: messages

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique identifier |
| conversation_id | UUID | FOREIGN KEY → conversations(id), NOT NULL | Reference to Conversation |
| sender_id | UUID | FOREIGN KEY → users(id), NOT NULL | Message sender |
| content | TEXT | NOT NULL | Message content |
| read_at | TIMESTAMP | NULL | Read timestamp (for read receipt) |
| sent_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Send timestamp |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (conversation_id) - for conversation messages
- INDEX (sender_id) - for sender queries
- COMPOSITE INDEX (conversation_id, sent_at DESC) - for message history
- INDEX (read_at) - for unread message queries
- FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
- FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE

---

### 3.10 Table: offers

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique identifier |
| listing_id | UUID | FOREIGN KEY → listings(id), NOT NULL | Reference to Listing |
| buyer_id | UUID | FOREIGN KEY → users(id), NOT NULL | Buyer (offer creator) |
| price | DECIMAL(12,2) | NOT NULL, CHECK (price > 0) | Offer price |
| message | TEXT | NULL | Optional message |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'PENDING' | Status: PENDING, ACCEPTED, REJECTED, CANCELLED |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (listing_id) - for listing's offers
- INDEX (buyer_id) - for buyer's offers
- INDEX (status) - for filtering by status
- COMPOSITE INDEX (listing_id, status) - for listing's pending offers
- FOREIGN KEY (listing_id) REFERENCES listings(id) ON DELETE CASCADE
- FOREIGN KEY (buyer_id) REFERENCES users(id) ON DELETE CASCADE

**Constraints**:
- CHECK: price <= listing.price (enforced in application logic)

---

### 3.11 Table: deals

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique identifier |
| listing_id | UUID | FOREIGN KEY → listings(id), NOT NULL | Reference to Listing |
| buyer_id | UUID | FOREIGN KEY → users(id), NOT NULL | Buyer |
| seller_id | UUID | FOREIGN KEY → users(id), NOT NULL | Seller |
| offer_id | UUID | FOREIGN KEY → offers(id), UNIQUE, NOT NULL | Accepted offer |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'PENDING' | Status: PENDING, CONFIRMED, COMPLETED, CANCELLED |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (offer_id) - one deal per offer
- INDEX (listing_id) - for listing's deal
- INDEX (buyer_id) - for buyer's deals
- INDEX (seller_id) - for seller's deals
- INDEX (status) - for filtering by status
- FOREIGN KEY (listing_id) REFERENCES listings(id) ON DELETE CASCADE
- FOREIGN KEY (buyer_id) REFERENCES users(id) ON DELETE CASCADE
- FOREIGN KEY (seller_id) REFERENCES users(id) ON DELETE CASCADE
- FOREIGN KEY (offer_id) REFERENCES offers(id) ON DELETE RESTRICT

**Constraints**:
- CHECK: buyer_id != seller_id (enforced in application logic)

---

### 3.12 Table: meetups

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique identifier |
| deal_id | UUID | FOREIGN KEY → deals(id), NOT NULL | Reference to Deal |
| scheduled_at | TIMESTAMP | NOT NULL | Scheduled date/time |
| location | VARCHAR(255) | NOT NULL | Meetup location |
| notes | TEXT | NULL | Optional notes |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (deal_id) - for deal's meetups
- INDEX (scheduled_at) - for upcoming meetups
- FOREIGN KEY (deal_id) REFERENCES deals(id) ON DELETE CASCADE

**Constraints**:
- CHECK: scheduled_at > NOW() (enforced in application logic)

---

### 3.13 Table: reports

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique identifier |
| reporter_id | UUID | FOREIGN KEY → users(id), NOT NULL | User who reported |
| reported_listing_id | UUID | FOREIGN KEY → listings(id), NULL | Reported listing (optional) |
| reported_user_id | UUID | FOREIGN KEY → users(id), NULL | Reported user (optional) |
| report_type | VARCHAR(50) | NOT NULL | Type: SPAM, INAPPROPRIATE, SCAM, OTHER |
| description | TEXT | NULL | Detailed description (optional) |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'PENDING' | Status: PENDING, RESOLVED, DISMISSED |
| resolved_by_id | UUID | FOREIGN KEY → users(id), NULL | Admin who resolved (optional) |
| resolved_at | TIMESTAMP | NULL | Resolution timestamp |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (reporter_id) - for reporter's reports
- INDEX (reported_listing_id) - for listing's reports
- INDEX (reported_user_id) - for user's reports
- INDEX (status) - for filtering pending reports
- COMPOSITE INDEX (status, created_at DESC) - for admin report list
- FOREIGN KEY (reporter_id) REFERENCES users(id) ON DELETE CASCADE
- FOREIGN KEY (reported_listing_id) REFERENCES listings(id) ON DELETE CASCADE
- FOREIGN KEY (reported_user_id) REFERENCES users(id) ON DELETE CASCADE
- FOREIGN KEY (resolved_by_id) REFERENCES users(id) ON DELETE SET NULL

**Constraints**:
- CHECK: reported_listing_id IS NOT NULL OR reported_user_id IS NOT NULL (at least one)

---

### 3.14 Table: blocks

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, DEFAULT uuid_generate_v4() | Unique identifier |
| blocker_id | UUID | FOREIGN KEY → users(id), NOT NULL | User who blocked |
| blocked_user_id | UUID | FOREIGN KEY → users(id), NOT NULL | User who was blocked |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (blocker_id, blocked_user_id) - prevent duplicate blocks
- INDEX (blocker_id) - for blocker's blocks
- INDEX (blocked_user_id) - for blocked user queries
- FOREIGN KEY (blocker_id) REFERENCES users(id) ON DELETE CASCADE
- FOREIGN KEY (blocked_user_id) REFERENCES users(id) ON DELETE CASCADE

**Constraints**:
- CHECK: blocker_id != blocked_user_id (enforced in application logic)

---

## 4. Indexes Strategy

### 4.1 Primary Indexes
Tất cả tables có PRIMARY KEY trên `id` column (UUID).

### 4.2 Foreign Key Indexes
Tất cả FOREIGN KEY columns đều có indexes để optimize JOIN queries.

### 4.3 Search Indexes
- **listings**: 
  - `category_id` - for category filtering
  - `status` - for status filtering
  - `price` - for price sorting/filtering
  - `created_at` - for date sorting
  - Composite: `(status, category_id)` - for common filtered queries
  - Composite: `(status, created_at DESC)` - for listing pages

### 4.4 Query Optimization Indexes
- **messages**: Composite `(conversation_id, sent_at DESC)` - for message history
- **conversations**: `updated_at DESC` - for sorting conversations
- **offers**: Composite `(listing_id, status)` - for listing's pending offers
- **reports**: Composite `(status, created_at DESC)` - for admin report list

### 4.5 Unique Constraints
- `users.email` - unique email
- `profiles.user_id` - one profile per user
- `favorites(user_id, listing_id)` - prevent duplicate favorites
- `conversation_members(conversation_id, user_id)` - prevent duplicate members
- `blocks(blocker_id, blocked_user_id)` - prevent duplicate blocks
- `deals.offer_id` - one deal per offer

---

## 5. Django ORM Models

### 5.1 Model Mapping

Django models sẽ map trực tiếp đến database tables với các conventions:

- Model class name: PascalCase (e.g., `Listing`, `ListingImage`)
- Table name: snake_case (e.g., `listings`, `listing_images`)
- Field names: snake_case (e.g., `seller_id`, `created_at`)

### 5.2 Key Django Model Features

#### 5.2.1 UUID Primary Keys
```python
import uuid
from django.db import models

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

#### 5.2.2 Relationships
- **One-to-One**: `OneToOneField` (User ↔ Profile)
- **One-to-Many**: `ForeignKey` (Listing → ListingImage)
- **Many-to-Many**: `ManyToManyField` hoặc through model (Conversation ↔ User)

#### 5.2.3 Field Types
- **UUID**: `UUIDField`
- **String**: `CharField`, `TextField`
- **Decimal**: `DecimalField` (for price)
- **Boolean**: `BooleanField`
- **DateTime**: `DateTimeField` với `auto_now_add`, `auto_now`
- **File**: `ImageField` hoặc `FileField`

### 5.3 Model Examples

#### User Model
```python
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # hashed
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
```

#### Listing Model
```python
class Listing(BaseModel):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    
    class Meta:
        indexes = [
            models.Index(fields=['seller_id']),
            models.Index(fields=['category_id']),
            models.Index(fields=['status']),
            models.Index(fields=['price']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status', 'category_id']),
            models.Index(fields=['status', '-created_at']),
        ]
```

---

## 6. Migration Strategy

### 6.1 Initial Migration
1. Enable UUID extension: `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";`
2. Create all tables theo thứ tự dependencies
3. Create indexes
4. Create foreign keys

### 6.2 Django Migrations
- Sử dụng Django's migration system (`python manage.py makemigrations`)
- Migrations được version control
- Migration files: `app_name/migrations/0001_initial.py`, etc.

### 6.3 Migration Best Practices
- **Never edit existing migrations**: Tạo migration mới để thay đổi
- **Test migrations**: Test trên development database trước
- **Backup before migration**: Backup database trước khi chạy migrations trong production
- **Rollback plan**: Có plan để rollback nếu migration fails

---

## 7. Data Integrity Constraints

### 7.1 Referential Integrity
- **CASCADE**: Khi parent record bị xóa, child records cũng bị xóa
  - User → Profile, Listings, Favorites, etc.
  - Listing → ListingImages, Offers, Favorites
  - Conversation → Messages, ConversationMembers
  
- **RESTRICT**: Không cho phép xóa parent nếu có child records
  - Category → Listings (không cho xóa category nếu có listings)
  
- **SET NULL**: Set foreign key thành NULL khi parent bị xóa
  - Listing → Conversations (conversation vẫn tồn tại nếu listing bị xóa)

### 7.2 Check Constraints
- **Price**: `price > 0` (listings, offers)
- **Order**: `order >= 0 AND order <= 4` (listing_images)
- **Date**: `scheduled_at > NOW()` (meetups) - enforced in application

### 7.3 Unique Constraints
- Email uniqueness
- One profile per user
- One favorite per user-listing pair
- One block per blocker-blocked pair
- One deal per offer

### 7.4 Business Logic Constraints (Application Level)
- Listing chỉ có thể edit khi status AVAILABLE hoặc RESERVED
- Offer chỉ có thể tạo khi Listing status AVAILABLE
- Offer price không được vượt quá Listing price
- Conversation chỉ có tối đa 2 members
- Deal buyer và seller phải khác nhau

---

## 8. Database Performance Considerations

### 8.1 Query Optimization
- Sử dụng `select_related()` cho ForeignKey
- Sử dụng `prefetch_related()` cho ManyToMany và reverse ForeignKey
- Sử dụng `only()` và `defer()` để limit columns
- Pagination cho list queries

### 8.2 Connection Pooling
- Django database connection pooling
- Configure `CONN_MAX_AGE` trong settings

### 8.3 Database Maintenance
- Regular VACUUM và ANALYZE
- Monitor slow queries
- Review và optimize indexes

---

## 9. Backup & Recovery

### 9.1 Backup Strategy
- **Daily backups**: Full database backup mỗi ngày
- **Transaction logs**: Enable WAL (Write-Ahead Logging) cho point-in-time recovery
- **Backup storage**: Store backups ở location khác server

### 9.2 Recovery Plan
- Test restore process định kỳ
- Document recovery procedures
- Recovery time objective (RTO): < 4 hours
- Recovery point objective (RPO): < 1 hour

---

## 10. References

- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Django Models: https://docs.djangoproject.com/en/stable/topics/db/models/
- Django Migrations: https://docs.djangoproject.com/en/stable/topics/migrations/

---

**End of Document**

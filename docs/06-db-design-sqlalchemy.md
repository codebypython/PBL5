# Database Design với SQLAlchemy ORM
## OldGoods Marketplace

**Version**: 2.0  
**Date**: 2024  
**Database**: PostgreSQL 12+  
**ORM**: SQLAlchemy 2.0+  
**Framework**: FastAPI

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [SQLAlchemy Models Design](#2-sqlalchemy-models-design)
3. [Domain-Driven Design Approach](#3-domain-driven-design-approach)
4. [Relationships & Constraints](#4-relationships--constraints)
5. [Indexes Strategy](#5-indexes-strategy)
6. [Migrations với Alembic](#6-migrations-với-alembic)
7. [Database Session Management](#7-database-session-management)

---

## 1. Introduction

### 1.1 Purpose
Tài liệu này mô tả thiết kế database cho hệ thống OldGoods Marketplace sử dụng SQLAlchemy ORM với FastAPI framework, theo hướng Object-Oriented Design và Domain-Driven Design.

### 1.2 Technology Stack
- **ORM**: SQLAlchemy 2.0+ (Declarative Base)
- **Migrations**: Alembic
- **Database**: PostgreSQL 12+
- **Framework**: FastAPI
- **Type Safety**: Pydantic models + SQLAlchemy type hints

### 1.3 Design Principles
- **OOD**: Object-Oriented Design với classes và inheritance
- **DDD**: Domain-Driven Design với Aggregates
- **Separation of Concerns**: Models tách biệt khỏi business logic
- **Type Safety**: Sử dụng type hints và enums

---

## 2. SQLAlchemy Models Design

### 2.1 Base Model

Tất cả models kế thừa từ `BaseModel` với common fields:

```python
class BaseModel(Base):
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
```

**Features**:
- UUID primary keys
- Automatic timestamps
- Index trên primary key

---

### 2.2 User Aggregate

#### User Model
```python
class User(BaseModel):
    __tablename__ = 'users'
    
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.USER)
    status = Column(SQLEnum(UserStatus), nullable=False, default=UserStatus.ACTIVE)
    is_active = Column(Boolean, default=True, nullable=False)
```

**Relationships**:
- One-to-One với Profile
- One-to-Many với Listings (as seller)
- One-to-Many với Offers (as buyer)
- Many-to-Many với Conversations (through ConversationMember)

#### Profile Model
```python
class Profile(BaseModel):
    __tablename__ = 'profiles'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    location = Column(String(255), nullable=True)
    avatar = Column(String(500), nullable=True)
    bio = Column(String(1000), nullable=True)
```

---

### 2.3 Listing Aggregate

#### Category Model
```python
class Category(BaseModel):
    __tablename__ = 'categories'
    
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey('categories.id', ondelete='SET NULL'))
```

**Self-referential relationship** cho hierarchical categories.

#### Listing Model
```python
class Listing(BaseModel):
    __tablename__ = 'listings'
    
    seller_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id', ondelete='RESTRICT'))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    condition = Column(SQLEnum(ListingCondition), nullable=False)
    location = Column(String(255), nullable=False)
    status = Column(SQLEnum(ListingStatus), nullable=False, default=ListingStatus.AVAILABLE)
```

**Constraints**:
- `CheckConstraint('price > 0')` - Price phải > 0

**Relationships**:
- Many-to-One với User (seller)
- Many-to-One với Category
- One-to-Many với ListingImage
- One-to-Many với Favorite
- One-to-Many với Offer

#### ListingImage Model
```python
class ListingImage(BaseModel):
    __tablename__ = 'listing_images'
    
    listing_id = Column(UUID(as_uuid=True), ForeignKey('listings.id', ondelete='CASCADE'))
    image = Column(String(500), nullable=False)
    order = Column(Integer, nullable=False, default=0)
```

**Constraints**:
- `CheckConstraint('order >= 0 AND order <= 4')` - Max 5 images

#### Favorite Model
```python
class Favorite(BaseModel):
    __tablename__ = 'favorites'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    listing_id = Column(UUID(as_uuid=True), ForeignKey('listings.id', ondelete='CASCADE'))
```

**Unique Constraint**: `(user_id, listing_id)` - Mỗi user chỉ favorite một listing một lần

---

### 2.4 Conversation Aggregate

#### Conversation Model
```python
class Conversation(BaseModel):
    __tablename__ = 'conversations'
    
    listing_id = Column(UUID(as_uuid=True), ForeignKey('listings.id', ondelete='SET NULL'), nullable=True)
```

**Relationships**:
- Optional Many-to-One với Listing
- One-to-Many với ConversationMember
- One-to-Many với Message

#### ConversationMember Model
```python
class ConversationMember(BaseModel):
    __tablename__ = 'conversation_members'
    
    conversation_id = Column(UUID(as_uuid=True), ForeignKey('conversations.id', ondelete='CASCADE'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    joined_at = Column(DateTime(timezone=True), nullable=False, server_default='now()')
```

**Unique Constraint**: `(conversation_id, user_id)` - Mỗi conversation chỉ có tối đa 2 members

#### Message Model
```python
class Message(BaseModel):
    __tablename__ = 'messages'
    
    conversation_id = Column(UUID(as_uuid=True), ForeignKey('conversations.id', ondelete='CASCADE'))
    sender_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    content = Column(Text, nullable=False)
    read_at = Column(DateTime(timezone=True), nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=False, server_default='now()')
```

---

### 2.5 Deal Aggregate

#### Offer Model
```python
class Offer(BaseModel):
    __tablename__ = 'offers'
    
    listing_id = Column(UUID(as_uuid=True), ForeignKey('listings.id', ondelete='CASCADE'))
    buyer_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    price = Column(Numeric(12, 2), nullable=False)
    message = Column(Text, nullable=True)
    status = Column(SQLEnum(OfferStatus), nullable=False, default=OfferStatus.PENDING)
```

**Constraints**:
- `CheckConstraint('price > 0')` - Price phải > 0

#### Deal Model
```python
class Deal(BaseModel):
    __tablename__ = 'deals'
    
    listing_id = Column(UUID(as_uuid=True), ForeignKey('listings.id', ondelete='CASCADE'))
    buyer_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    seller_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    offer_id = Column(UUID(as_uuid=True), ForeignKey('offers.id', ondelete='RESTRICT'), unique=True)
    status = Column(SQLEnum(DealStatus), nullable=False, default=DealStatus.PENDING)
```

**Unique Constraint**: `offer_id` - Mỗi offer chỉ tạo một deal

#### Meetup Model
```python
class Meetup(BaseModel):
    __tablename__ = 'meetups'
    
    deal_id = Column(UUID(as_uuid=True), ForeignKey('deals.id', ondelete='CASCADE'))
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(255), nullable=False)
    notes = Column(Text, nullable=True)
```

---

### 2.6 Moderation Aggregate

#### Report Model
```python
class Report(BaseModel):
    __tablename__ = 'reports'
    
    reporter_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    reported_listing_id = Column(UUID(as_uuid=True), ForeignKey('listings.id', ondelete='CASCADE'), nullable=True)
    reported_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    report_type = Column(SQLEnum(ReportType), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(ReportStatus), nullable=False, default=ReportStatus.PENDING)
    resolved_by_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
```

**Constraints**:
- `CheckConstraint('(reported_listing_id IS NOT NULL) OR (reported_user_id IS NOT NULL)')` - Phải có ít nhất một target

#### Block Model
```python
class Block(BaseModel):
    __tablename__ = 'blocks'
    
    blocker_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    blocked_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
```

**Unique Constraint**: `(blocker_id, blocked_user_id)` - Self-referential relationship

---

## 3. Domain-Driven Design Approach

### 3.1 Aggregates

Hệ thống được tổ chức thành các **Aggregates**:

1. **User Aggregate**
   - Root Entity: `User`
   - Entities: `Profile`

2. **Listing Aggregate**
   - Root Entity: `Listing`
   - Entities: `Category`, `ListingImage`, `Favorite`

3. **Conversation Aggregate**
   - Root Entity: `Conversation`
   - Entities: `ConversationMember`, `Message`

4. **Deal Aggregate**
   - Root Entity: `Deal`
   - Entities: `Offer`, `Meetup`

5. **Moderation Aggregate**
   - Entities: `Report`, `Block`

### 3.2 Value Objects

- **Enums**: UserRole, UserStatus, ListingCondition, ListingStatus, OfferStatus, DealStatus, ReportType, ReportStatus
- **UUID**: Primary keys
- **Money**: Numeric(12, 2) cho prices

---

## 4. Relationships & Constraints

### 4.1 One-to-One
- User ↔ Profile

### 4.2 One-to-Many
- User → Listings (seller)
- User → Offers (buyer)
- Listing → ListingImages
- Listing → Offers
- Conversation → Messages
- Deal → Meetups

### 4.3 Many-to-Many
- User ↔ Conversations (through ConversationMember)
- User ↔ Listings (through Favorite)
- User ↔ User (through Block - self-referential)

### 4.4 Foreign Key Constraints

**CASCADE Delete**:
- User → Profile, Listings, Offers, Favorites
- Listing → ListingImages, Offers, Favorites
- Conversation → Messages, ConversationMembers

**RESTRICT Delete**:
- Category → Listings (không cho xóa category nếu có listings)
- Offer → Deal (không cho xóa offer nếu đã có deal)

**SET NULL Delete**:
- Listing → Conversations (conversation vẫn tồn tại)
- User → Reports (resolved_by)

---

## 5. Indexes Strategy

### 5.1 Primary Key Indexes
Tất cả tables có index trên `id` (UUID).

### 5.2 Foreign Key Indexes
Tất cả foreign keys đều có indexes để optimize JOIN queries.

### 5.3 Search Indexes
- `users.email` - Unique index
- `listings.title`, `listings.description` - Full-text search (có thể thêm)
- `listings.price` - Price sorting/filtering
- `listings.created_at` - Date sorting

### 5.4 Composite Indexes
- `(listings.status, listings.category_id)` - Common filtered queries
- `(listings.status, listings.created_at DESC)` - Listing pages
- `(messages.conversation_id, messages.sent_at DESC)` - Message history
- `(offers.listing_id, offers.status)` - Listing's pending offers
- `(reports.status, reports.created_at DESC)` - Admin report list

---

## 6. Migrations với Alembic

### 6.1 Alembic Setup

**alembic.ini**:
```ini
[alembic]
script_location = alembic
sqlalchemy.url = driver://user:pass@localhost/dbname
```

**alembic/env.py**:
- Import Base và tất cả models
- Configure target_metadata = Base.metadata
- Setup database URL từ environment

### 6.2 Migration Commands

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# Show current revision
alembic current

# Show migration history
alembic history
```

### 6.3 Initial Migration

Initial migration (`001_initial_migration.py`) tạo:
- UUID extension
- Tất cả tables
- Tất cả indexes
- Tất cả constraints
- Tất cả enums

---

## 7. Database Session Management

### 7.1 Session Factory

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### 7.2 FastAPI Dependency

```python
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Usage trong FastAPI**:
```python
@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

### 7.3 Transaction Management

SQLAlchemy tự động quản lý transactions:
- `db.commit()` - Commit transaction
- `db.rollback()` - Rollback transaction
- Context manager tự động commit/rollback

---

## 8. Model Methods & Business Logic

### 8.1 Model Methods

```python
class User(BaseModel):
    def is_banned(self) -> bool:
        """Check if user is banned."""
        return self.status == UserStatus.BANNED

class Listing(BaseModel):
    def can_edit(self) -> bool:
        """Check if listing can be edited."""
        return self.status in [ListingStatus.AVAILABLE, ListingStatus.RESERVED]
```

### 8.2 Query Examples

```python
# Get user với profile
user = db.query(User).options(joinedload(User.profile)).filter(User.id == user_id).first()

# Get listings với images và seller
listings = db.query(Listing).options(
    joinedload(Listing.images),
    joinedload(Listing.seller).joinedload(User.profile)
).filter(Listing.status == ListingStatus.AVAILABLE).all()

# Search listings
listings = db.query(Listing).filter(
    Listing.title.ilike(f"%{keyword}%")
).order_by(Listing.created_at.desc()).limit(20).all()
```

---

## 9. Comparison với Django ORM

### 9.1 Advantages SQLAlchemy
- **Flexibility**: Linh hoạt hơn cho complex queries
- **Type Safety**: Better type hints support
- **Performance**: Có thể optimize queries tốt hơn
- **Independence**: Không phụ thuộc framework

### 9.2 Advantages Django ORM
- **Integration**: Tích hợp tốt với Django ecosystem
- **Admin**: Django Admin tự động
- **Migrations**: Django migrations đơn giản hơn
- **Conventions**: Follows Django conventions

---

## 10. References

- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- Alembic Documentation: https://alembic.sqlalchemy.org/
- FastAPI Documentation: https://fastapi.tiangolo.com/
- PostgreSQL Documentation: https://www.postgresql.org/docs/

---

**End of Document**

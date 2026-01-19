# OldGoods Marketplace - FastAPI + SQLAlchemy

Hệ thống marketplace đồ cũ cho sinh viên và cư dân trong khu vực, được xây dựng với FastAPI và SQLAlchemy ORM.

## Công nghệ

- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0+
- **Database**: PostgreSQL 12+
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose)

## Cấu trúc Dự án

```
oldgoods-marketplace/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── database/
│   │   ├── base.py            # Base model
│   │   ├── session.py         # Database session
│   │   └── models/            # SQLAlchemy models
│   │       ├── user.py
│   │       ├── listing.py
│   │       ├── chat.py
│   │       ├── deal.py
│   │       └── moderation.py
│   ├── core/
│   │   └── config.py         # Configuration
│   └── api/                   # API endpoints (sẽ được tạo)
├── alembic/                   # Alembic migrations
│   ├── versions/
│   └── env.py
├── alembic.ini
├── requirements-fastapi.txt
└── README-FASTAPI.md
```

## Cài đặt

### 1. Tạo Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements-fastapi.txt
```

### 3. Setup Environment Variables

Tạo file `.env`:

```env
# Database
DB_USER=oldgoods_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=oldgoods_db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days
REFRESH_TOKEN_EXPIRE_DAYS=30

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 4. Setup Database

```bash
# Tạo database PostgreSQL
createdb oldgoods_db

# Chạy migrations
alembic upgrade head
```

### 5. Run Application

```bash
uvicorn app.main:app --reload
```

API sẽ chạy tại: `http://localhost:8000`
Documentation: `http://localhost:8000/docs`

## Database Models

### Aggregates

1. **User Aggregate**
   - `User` (root entity)
   - `Profile`

2. **Listing Aggregate**
   - `Category`
   - `Listing` (root entity)
   - `ListingImage`
   - `Favorite`

3. **Conversation Aggregate**
   - `Conversation` (root entity)
   - `ConversationMember`
   - `Message`

4. **Deal Aggregate**
   - `Offer`
   - `Deal` (root entity)
   - `Meetup`

5. **Moderation Aggregate**
   - `Report`
   - `Block`

## Migrations

### Tạo Migration

```bash
alembic revision --autogenerate -m "description"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback

```bash
alembic downgrade -1
```

## Database Session Usage

Trong FastAPI endpoints:

```python
from fastapi import Depends
from app.database.session import get_db
from sqlalchemy.orm import Session

@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

## Testing

```bash
pytest
```

## Documentation

Xem chi tiết trong:
- [Database Design với SQLAlchemy](docs/06-db-design-sqlalchemy.md)
- [API Specification](docs/07-api-spec.md)

## Notes

- Models được thiết kế theo Domain-Driven Design với Aggregates
- Sử dụng UUID cho primary keys
- Timestamps tự động (created_at, updated_at)
- Indexes được tối ưu cho search và filtering

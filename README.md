# OldGoods Marketplace

Hệ thống marketplace đồ cũ cho sinh viên và cư dân trong khu vực.

> **Chốt hướng thiết kế**: FastAPI + SQLAlchemy + Alembic + PostgreSQL + WebSocket.  
> Xem quyết định kiến trúc tại `docs/00-architecture-decision.md`.

## Tính năng

- **Authentication**: Đăng ký, đăng nhập với JWT
- **Product Listings**: Đăng tin, quản lý sản phẩm với hình ảnh
- **Search & Filter**: Tìm kiếm và lọc sản phẩm theo nhiều tiêu chí
- **Real-time Chat**: Chat realtime giữa người mua và người bán
- **Offers & Deals**: Tạo offer, chấp nhận offer, tạo deal
- **Moderation**: Báo cáo và kiểm duyệt nội dung

## Công nghệ

- **Backend**: FastAPI
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Database**: PostgreSQL 12+
- **Realtime**: FastAPI WebSocket
- **Authentication**: JWT (python-jose + passlib/bcrypt)

## Cài đặt (hướng FastAPI)

### Yêu cầu

- Python 3.10+
- PostgreSQL 12+
- Redis (optional, cho production)

### Setup

1. Clone repository:
```bash
git clone <repository-url>
cd oldgoods-marketplace
```

2. Tạo virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements-fastapi.txt
```

4. Setup environment variables:
```bash
cp .env.example .env
# Edit .env với các giá trị phù hợp
```

5. Setup database:
```bash
# Create PostgreSQL database
createdb oldgoods_db

# Run migrations (Alembic)
alembic upgrade head
```

6. Run development server:
```bash
uvicorn app.main:app --reload
```

## Cấu trúc Dự án (tóm tắt)

```
app/
├── main.py                 # FastAPI app
├── core/                   # config, security, deps
└── database/
    ├── session.py          # SQLAlchemy session
    └── models/             # ORM models
alembic/                    # migrations
```

## API Documentation

API base URL: `http://localhost:8000/` (docs: `/docs`)

Xem chi tiết trong [API Specification](docs/07-api-spec.md)

## Documentation

Tất cả tài liệu dự án nằm trong thư mục `docs/`:

- [Vision & Scope](docs/01-vision-scope.md)
- [SRS](docs/02-srs.md)
- [NFR](docs/03-nfr.md)
- [SAD](docs/04-sad-architecture-4+1.md)
- [DB Design](docs/06-db-design.md)
- [DB Design (SQLAlchemy - tài liệu chính)](docs/06-db-design-sqlalchemy.md)
- [API Spec](docs/07-api-spec.md)
- [Test Plan](docs/08-test-plan.md)
- [Deployment Guide](docs/09-deployment-guide.md)
- [Project Plan](docs/10-project-plan.md)

## FastAPI README

Xem hướng dẫn chi tiết setup FastAPI tại `README-FASTAPI.md`.

## Testing

```bash
# Run all tests
pytest

# Run với coverage
pytest --cov=app --cov-report=html
```

## Deployment

Xem [Deployment Guide](docs/09-deployment-guide.md) để biết chi tiết.

## License

[Your License]

## Authors

Development Team

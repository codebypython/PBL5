# OldGoods Marketplace

Hệ thống marketplace đồ cũ cho sinh viên và cư dân trong khu vực.

## Tính năng

- **Authentication**: Đăng ký, đăng nhập với JWT
- **Product Listings**: Đăng tin, quản lý sản phẩm với hình ảnh
- **Search & Filter**: Tìm kiếm và lọc sản phẩm theo nhiều tiêu chí
- **Real-time Chat**: Chat realtime giữa người mua và người bán
- **Offers & Deals**: Tạo offer, chấp nhận offer, tạo deal
- **Moderation**: Báo cáo và kiểm duyệt nội dung

## Công nghệ

- **Backend**: Django 4.2+, Django REST Framework
- **Database**: PostgreSQL 12+
- **WebSocket**: Django Channels với Redis
- **Authentication**: JWT (djangorestframework-simplejwt)

## Cài đặt

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
pip install -r requirements.txt
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

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

## Cấu trúc Dự án

```
oldgoods_marketplace/
├── accounts/          # Authentication & User Management
├── listings/          # Product Listings
├── chat/             # Real-time Chat (WebSocket)
├── deals/            # Offers & Deals
├── moderation/       # Reports & Blocks
├── admin_panel/      # Admin Moderation
├── core/             # Shared Utilities
└── oldgoods_marketplace/  # Project Settings
```

## API Documentation

API base URL: `http://localhost:8000/api/v1/`

Xem chi tiết trong [API Specification](docs/07-api-spec.md)

## Documentation

Tất cả tài liệu dự án nằm trong thư mục `docs/`:

- [Vision & Scope](docs/01-vision-scope.md)
- [SRS](docs/02-srs.md)
- [NFR](docs/03-nfr.md)
- [SAD](docs/04-sad-architecture-4+1.md)
- [DB Design](docs/06-db-design.md)
- [API Spec](docs/07-api-spec.md)
- [Test Plan](docs/08-test-plan.md)
- [Deployment Guide](docs/09-deployment-guide.md)
- [Project Plan](docs/10-project-plan.md)

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

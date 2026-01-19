# Architecture Decision Record (ADR)
## OldGoods Marketplace - Chốt hướng thiết kế

**Ngày**: 2026-01-19  
**Trạng thái**: Accepted  

---

## 1. Bối cảnh

Trong các phiên bản tài liệu ban đầu, dự án được mô tả theo hướng **Django + Django ORM + Django migrations + Channels**.
Tuy nhiên, hướng triển khai mới đã được thống nhất là **ORDB (PostgreSQL) + ORM (SQLAlchemy) + FastAPI**, với migrations bằng **Alembic** và realtime bằng **FastAPI WebSocket**.

---

## 2. Quyết định

Chốt hướng thiết kế cho toàn bộ dự án như sau:

- **Backend framework**: FastAPI
- **ORM**: SQLAlchemy (Declarative/SQLAlchemy 2.x style)
- **Migrations**: Alembic
- **Database**: PostgreSQL
- **Realtime**: FastAPI WebSocket (và/hoặc Redis pubsub trong tương lai nếu cần scale)
- **Auth**: JWT (python-jose + passlib/bcrypt)

---

## 3. Hệ quả (Consequences)

### 3.1 Cập nhật tài liệu

Các tài liệu cần được cập nhật để nhất quán:
- `docs/04-sad-architecture-4+1.md`: thay Django/Channels → FastAPI/WebSocket; cập nhật development view/process view/physical view.
- `docs/06-db-design.md`: đánh dấu tài liệu Django ORM là *legacy*; tài liệu DB chính là `docs/06-db-design-sqlalchemy.md`.
- `docs/07-api-spec.md`: cập nhật ví dụ tech stack (FastAPI + Pydantic schemas), auth JWT, ws endpoint.
- `docs/09-deployment-guide.md`: cập nhật run commands (uvicorn), Alembic migrations.
- `docs/10-project-plan.md`: cập nhật stack, task breakdown theo FastAPI/Alembic.
- `README.md`: cập nhật hướng dẫn/entrypoint; trỏ sang `README-FASTAPI.md`.

### 3.2 Codebase

Code Django (nếu còn tồn tại) chỉ được coi là **prototype/legacy**; hướng phát triển chính thức bám theo cấu trúc:
- `app/` (FastAPI)
- `app/database/models/` (SQLAlchemy models)
- `alembic/` (migrations)

---

## 4. Lý do chọn

- Dễ kết hợp OOD (domain model) với ORDB (PostgreSQL) qua ORM (SQLAlchemy).
- Linh hoạt khi thiết kế query, index, migration.
- FastAPI phù hợp API-first và realtime WebSocket cho chat.


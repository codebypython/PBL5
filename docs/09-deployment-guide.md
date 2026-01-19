# Deployment Guide
## OldGoods Marketplace

**Version**: 1.0  
**Date**: 2024

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [System Requirements](#2-system-requirements)
3. [Prerequisites](#3-prerequisites)
4. [Environment Setup](#4-environment-setup)
5. [Database Setup](#5-database-setup)
6. [Application Deployment](#6-application-deployment)
7. [WebSocket Server Setup](#7-websocket-server-setup)
8. [Static Files & Media](#8-static-files--media)
9. [Configuration](#9-configuration)
10. [Docker Deployment](#10-docker-deployment)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. Introduction

### 1.1 Purpose
Hướng dẫn này mô tả cách deploy hệ thống OldGoods Marketplace lên production server hoặc development environment.

### 1.2 Deployment Architecture

```
Internet → Nginx → Gunicorn/Uvicorn → Django App
                              ↓
                         PostgreSQL
                              ↓
                          Redis (Channels)
```

---

## 2. System Requirements

### 2.1 Server Requirements

#### Minimum (Development)
- **CPU**: 2 cores
- **RAM**: 4 GB
- **Storage**: 20 GB
- **OS**: Ubuntu 20.04+ / Windows 10+ / macOS

#### Recommended (Production)
- **CPU**: 4+ cores
- **RAM**: 8+ GB
- **Storage**: 50+ GB (SSD recommended)
- **OS**: Ubuntu 22.04 LTS

### 2.2 Software Requirements
- **Python**: 3.10 or higher
- **PostgreSQL**: 12 or higher
- **Redis**: 6.0 or higher (for production WebSocket)
- **Nginx**: 1.18 or higher (for production)
- **Git**: Latest version

---

## 3. Prerequisites

### 3.1 Install Python
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip

# Verify
python3 --version
```

### 3.2 Install PostgreSQL
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verify
psql --version
```

### 3.3 Install Redis (for production)
```bash
# Ubuntu/Debian
sudo apt install redis-server

# Start Redis
sudo systemctl start redis
sudo systemctl enable redis

# Verify
redis-cli ping
```

### 3.4 Install Nginx (for production)
```bash
# Ubuntu/Debian
sudo apt install nginx

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

---

## 4. Environment Setup

### 4.1 Clone Repository
```bash
git clone <repository-url>
cd oldgoods-marketplace
```

### 4.2 Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4.3 Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4.4 Environment Variables

Create `.env` file từ `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` với các giá trị phù hợp:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,localhost

# Database
DB_NAME=oldgoods_db
DB_USER=oldgoods_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Redis (for Channels)
REDIS_URL=redis://localhost:6379/0

# Media Files
MEDIA_ROOT=/var/www/oldgoods/media
STATIC_ROOT=/var/www/oldgoods/static

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_LIFETIME=7  # days
JWT_REFRESH_TOKEN_LIFETIME=30  # days

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

**Generate Secret Keys**:
```bash
# Generate Django SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Generate JWT secret (any random string)
openssl rand -hex 32
```

---

## 5. Database Setup

### 5.1 Create PostgreSQL Database

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database và user
CREATE DATABASE oldgoods_db;
CREATE USER oldgoods_user WITH PASSWORD 'your-password';
ALTER ROLE oldgoods_user SET client_encoding TO 'utf8';
ALTER ROLE oldgoods_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE oldgoods_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE oldgoods_db TO oldgoods_user;

# Enable UUID extension
\c oldgoods_db
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

# Exit
\q
```

### 5.2 Update Database Settings

Trong `.env`, set:
```env
DB_NAME=oldgoods_db
DB_USER=oldgoods_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### 5.3 Run Migrations

```bash
# Make migrations (if needed)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

---

## 6. Application Deployment

### 6.1 Development Server

```bash
# Run development server
python manage.py runserver

# Server sẽ chạy tại http://localhost:8000
```

### 6.2 Production Server với Gunicorn

#### Install Gunicorn
```bash
pip install gunicorn
```

#### Run với Gunicorn
```bash
# Basic
gunicorn oldgoods_marketplace.wsgi:application

# With options
gunicorn oldgoods_marketplace.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
```

#### Gunicorn Configuration File

Create `gunicorn_config.py`:
```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"
```

Run với config file:
```bash
gunicorn -c gunicorn_config.py oldgoods_marketplace.wsgi:application
```

### 6.3 Systemd Service (Production)

Create `/etc/systemd/system/oldgoods.service`:
```ini
[Unit]
Description=OldGoods Marketplace Gunicorn
After=network.target postgresql.service redis.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/oldgoods
Environment="PATH=/var/www/oldgoods/venv/bin"
ExecStart=/var/www/oldgoods/venv/bin/gunicorn \
    --config /var/www/oldgoods/gunicorn_config.py \
    oldgoods_marketplace.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable và start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable oldgoods
sudo systemctl start oldgoods
sudo systemctl status oldgoods
```

---

## 7. WebSocket Server Setup

### 7.1 Development (InMemoryChannelLayer)

Không cần Redis, sử dụng InMemoryChannelLayer (chỉ cho development).

### 7.2 Production (Redis Channel Layer)

#### Install và Configure Redis
```bash
# Redis đã được install ở bước 3.3
# Configure Redis (optional)
sudo nano /etc/redis/redis.conf
```

#### Update Django Settings

Trong `settings.py`:
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```

#### Run ASGI Server với Uvicorn

```bash
# Install Uvicorn
pip install uvicorn

# Run ASGI server
uvicorn oldgoods_marketplace.asgi:application \
    --host 0.0.0.0 \
    --port 8001 \
    --workers 4
```

#### Systemd Service cho ASGI

Create `/etc/systemd/system/oldgoods-asgi.service`:
```ini
[Unit]
Description=OldGoods Marketplace ASGI (WebSocket)
After=network.target redis.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/oldgoods
Environment="PATH=/var/www/oldgoods/venv/bin"
ExecStart=/var/www/oldgoods/venv/bin/uvicorn \
    oldgoods_marketplace.asgi:application \
    --host 127.0.0.1 \
    --port 8001 \
    --workers 4

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

## 8. Static Files & Media

### 8.1 Collect Static Files

```bash
# Collect static files
python manage.py collectstatic --noinput

# Static files sẽ được copy đến STATIC_ROOT
```

### 8.2 Configure Nginx cho Static Files

Edit `/etc/nginx/sites-available/oldgoods`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Static files
    location /static/ {
        alias /var/www/oldgoods/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /var/www/oldgoods/media/;
        expires 7d;
        add_header Cache-Control "public";
    }

    # Proxy to Gunicorn (HTTP)
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Proxy to ASGI (WebSocket)
    location /ws/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/oldgoods /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 8.3 Set Permissions

```bash
# Set ownership
sudo chown -R www-data:www-data /var/www/oldgoods

# Set permissions
sudo chmod -R 755 /var/www/oldgoods
sudo chmod -R 775 /var/www/oldgoods/media  # For uploads
```

---

## 9. Configuration

### 9.1 Django Settings

#### Development Settings
```python
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

#### Production Settings
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 9.2 SSL Certificate (Production)

#### Using Let's Encrypt
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

Update Nginx config để redirect HTTP → HTTPS.

---

## 10. Docker Deployment

### 10.1 Docker Compose Setup

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: oldgoods_db
      POSTGRES_USER: oldgoods_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  web:
    build: .
    command: gunicorn oldgoods_marketplace.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/static
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DB_HOST=db
      - DB_PORT=5432
      - REDIS_URL=redis://redis:6379/0

  asgi:
    build: .
    command: uvicorn oldgoods_marketplace.asgi:application --host 0.0.0.0 --port 8001
    volumes:
      - .:/app
    ports:
      - "8001:8001"
    depends_on:
      - db
      - redis
    environment:
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379/0

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### 10.2 Dockerfile

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "oldgoods_marketplace.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### 10.3 Run với Docker

```bash
# Build và start
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# View logs
docker-compose logs -f
```

---

## 11. Troubleshooting

### 11.1 Common Issues

#### Database Connection Error
**Error**: `django.db.utils.OperationalError: could not connect to server`

**Solution**:
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Check database credentials in `.env`
- Check firewall rules

#### Static Files Not Found
**Error**: `404 Not Found` for static files

**Solution**:
- Run `python manage.py collectstatic`
- Check `STATIC_ROOT` và `STATIC_URL` in settings
- Check Nginx config for static files location

#### WebSocket Connection Failed
**Error**: WebSocket connection fails

**Solution**:
- Check Redis is running: `redis-cli ping`
- Check ASGI server is running
- Check Nginx WebSocket proxy config
- Check CORS settings (if frontend on different domain)

#### Permission Denied
**Error**: Permission denied khi upload files

**Solution**:
```bash
sudo chown -R www-data:www-data /var/www/oldgoods/media
sudo chmod -R 775 /var/www/oldgoods/media
```

### 11.2 Logs

#### Application Logs
```bash
# Gunicorn logs
tail -f /var/log/gunicorn/error.log

# Systemd logs
sudo journalctl -u oldgoods -f
```

#### Database Logs
```bash
# PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-*.log
```

#### Nginx Logs
```bash
# Access logs
sudo tail -f /var/log/nginx/access.log

# Error logs
sudo tail -f /var/log/nginx/error.log
```

### 11.3 Health Checks

#### Check Application
```bash
curl http://localhost:8000/api/v1/categories/
```

#### Check Database
```bash
psql -U oldgoods_user -d oldgoods_db -c "SELECT 1;"
```

#### Check Redis
```bash
redis-cli ping
```

#### Check WebSocket
```bash
# Test WebSocket connection (using wscat or similar)
wscat -c ws://localhost:8001/ws/chat/?token=<jwt_token>
```

---

## 12. Backup & Recovery

### 12.1 Database Backup

```bash
# Backup database
pg_dump -U oldgoods_user oldgoods_db > backup_$(date +%Y%m%d).sql

# Restore database
psql -U oldgoods_user oldgoods_db < backup_20240120.sql
```

### 12.2 Media Files Backup

```bash
# Backup media directory
tar -czf media_backup_$(date +%Y%m%d).tar.gz /var/www/oldgoods/media
```

### 12.3 Automated Backup Script

Create `backup.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/oldgoods"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U oldgoods_user oldgoods_db > $BACKUP_DIR/db_$DATE.sql

# Backup media
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/oldgoods/media

# Keep only last 7 days
find $BACKUP_DIR -type f -mtime +7 -delete
```

Add to crontab:
```bash
# Daily backup at 2 AM
0 2 * * * /path/to/backup.sh
```

---

## 13. Monitoring

### 13.1 Application Monitoring

#### Check Application Status
```bash
sudo systemctl status oldgoods
sudo systemctl status oldgoods-asgi
```

#### Monitor Resources
```bash
# CPU và Memory
htop

# Disk usage
df -h
```

### 13.2 Database Monitoring

```bash
# Check database connections
psql -U oldgoods_user -d oldgoods_db -c "SELECT count(*) FROM pg_stat_activity;"

# Check database size
psql -U oldgoods_user -d oldgoods_db -c "SELECT pg_size_pretty(pg_database_size('oldgoods_db'));"
```

---

## 14. References

- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
- Gunicorn Documentation: https://docs.gunicorn.org/
- Django Channels Deployment: https://channels.readthedocs.io/en/stable/deploying.html
- Nginx Configuration: https://nginx.org/en/docs/

---

**End of Document**

# API Specification
## OldGoods Marketplace

**Version**: 1.0  
**Date**: 2024  
**Base URL**: `https://api.oldgoods.example.com/api/v1` (production)  
**Base URL**: `http://localhost:8000/api/v1` (development)

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Authentication](#2-authentication)
3. [REST API Endpoints](#3-rest-api-endpoints)
4. [WebSocket API](#4-websocket-api)
5. [Error Handling](#5-error-handling)
6. [Request/Response Formats](#6-requestresponse-formats)

---

## 1. Introduction

### 1.1 API Overview
OldGoods Marketplace API cung cấp REST API cho CRUD operations và WebSocket API cho realtime chat.

### 1.2 API Versioning
- Current version: `v1`
- Version được specify trong URL: `/api/v1/...`
- Future versions: `v2`, `v3`, etc.

### 1.3 Content Types
- **Request**: `application/json` (REST), `text/plain` (WebSocket messages)
- **Response**: `application/json`
- **File Upload**: `multipart/form-data`

### 1.4 Authentication
- REST API: JWT Bearer Token
- WebSocket: JWT Token trong query string hoặc header

---

## 2. Authentication

### 2.1 JWT Authentication

#### Register
**Endpoint**: `POST /auth/register`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "password_confirm": "SecurePass123",
  "full_name": "John Doe"
}
```

**Response** (201 Created):
```json
{
  "message": "User registered successfully",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe"
  }
}
```

**Error Responses**:
- `400 Bad Request`: Validation errors
- `409 Conflict`: Email already exists

---

#### Login
**Endpoint**: `POST /auth/login`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response** (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "USER"
  }
}
```

**Error Responses**:
- `400 Bad Request`: Invalid credentials
- `401 Unauthorized`: Account banned

---

#### Refresh Token
**Endpoint**: `POST /auth/refresh`

**Request Body**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response** (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

#### Logout
**Endpoint**: `POST /auth/logout`

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "message": "Logged out successfully"
}
```

---

### 2.2 Using JWT Token

Include JWT token trong `Authorization` header:
```
Authorization: Bearer <access_token>
```

---

## 3. REST API Endpoints

### 3.1 User & Profile Endpoints

#### Get Current User Profile
**Endpoint**: `GET /users/me`

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "full_name": "John Doe",
  "phone": "+84123456789",
  "location": "Ho Chi Minh City",
  "avatar": "/media/avatars/user123.jpg",
  "bio": "Student at University",
  "role": "USER",
  "status": "ACTIVE",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

#### Update Profile
**Endpoint**: `PUT /users/me`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "full_name": "John Updated",
  "phone": "+84123456789",
  "location": "Hanoi",
  "bio": "Updated bio"
}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "full_name": "John Updated",
  "phone": "+84123456789",
  "location": "Hanoi",
  "bio": "Updated bio",
  "updated_at": "2024-01-20T15:45:00Z"
}
```

---

### 3.2 Category Endpoints

#### List Categories
**Endpoint**: `GET /categories`

**Response** (200 OK):
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "cat-001",
      "name": "Electronics",
      "slug": "electronics",
      "description": "Electronic devices",
      "parent_id": null
    },
    {
      "id": "cat-002",
      "name": "Books",
      "slug": "books",
      "description": "Books and magazines",
      "parent_id": null
    }
  ]
}
```

---

#### Get Category Detail
**Endpoint**: `GET /categories/{id}`

**Response** (200 OK):
```json
{
  "id": "cat-001",
  "name": "Electronics",
  "slug": "electronics",
  "description": "Electronic devices",
  "parent_id": null,
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

### 3.3 Listing Endpoints

#### List Listings
**Endpoint**: `GET /listings`

**Query Parameters**:
- `search` (string, optional): Search keyword
- `category` (UUID, optional): Filter by category ID
- `min_price` (decimal, optional): Minimum price
- `max_price` (decimal, optional): Maximum price
- `condition` (string, optional): NEW, LIKE_NEW, USED, POOR
- `location` (string, optional): Location filter
- `status` (string, optional): AVAILABLE, RESERVED, SOLD
- `ordering` (string, optional): `created_at`, `-created_at`, `price`, `-price`
- `page` (integer, optional): Page number (default: 1)
- `page_size` (integer, optional): Items per page (default: 20, max: 100)

**Example**: `GET /listings?search=laptop&category=cat-001&min_price=1000000&max_price=5000000&ordering=-created_at&page=1`

**Response** (200 OK):
```json
{
  "count": 150,
  "next": "http://api.example.com/api/v1/listings?page=2",
  "previous": null,
  "results": [
    {
      "id": "listing-001",
      "seller": {
        "id": "user-001",
        "full_name": "John Doe",
        "avatar": "/media/avatars/user001.jpg"
      },
      "category": {
        "id": "cat-001",
        "name": "Electronics",
        "slug": "electronics"
      },
      "title": "MacBook Pro 2020",
      "description": "Good condition, used for 2 years",
      "price": "25000000",
      "condition": "USED",
      "location": "Ho Chi Minh City",
      "status": "AVAILABLE",
      "images": [
        {
          "id": "img-001",
          "image": "/media/listings/img001.jpg",
          "order": 0
        }
      ],
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

#### Get Listing Detail
**Endpoint**: `GET /listings/{id}`

**Response** (200 OK):
```json
{
  "id": "listing-001",
  "seller": {
    "id": "user-001",
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "+84123456789",
    "avatar": "/media/avatars/user001.jpg"
  },
  "category": {
    "id": "cat-001",
    "name": "Electronics",
    "slug": "electronics"
  },
  "title": "MacBook Pro 2020",
  "description": "Good condition, used for 2 years. No scratches.",
  "price": "25000000",
  "condition": "USED",
  "location": "Ho Chi Minh City",
  "status": "AVAILABLE",
  "images": [
    {
      "id": "img-001",
      "image": "/media/listings/img001.jpg",
      "order": 0
    },
    {
      "id": "img-002",
      "image": "/media/listings/img002.jpg",
      "order": 1
    }
  ],
  "is_favorited": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Note**: `is_favorited` chỉ có khi user đã đăng nhập.

---

#### Create Listing
**Endpoint**: `POST /listings`

**Headers**: `Authorization: Bearer <token>`

**Request Body** (multipart/form-data):
```
title: "MacBook Pro 2020"
description: "Good condition laptop"
category_id: "cat-001"
price: 25000000
condition: "USED"
location: "Ho Chi Minh City"
images: [file1.jpg, file2.jpg, ...] (max 5 files, each < 5MB)
```

**Response** (201 Created):
```json
{
  "id": "listing-001",
  "seller": {
    "id": "user-001",
    "full_name": "John Doe"
  },
  "title": "MacBook Pro 2020",
  "description": "Good condition laptop",
  "price": "25000000",
  "condition": "USED",
  "location": "Ho Chi Minh City",
  "status": "AVAILABLE",
  "images": [...],
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Validation errors
- `401 Unauthorized`: Not authenticated

---

#### Update Listing
**Endpoint**: `PUT /listings/{id}` hoặc `PATCH /listings/{id}`

**Headers**: `Authorization: Bearer <token>`

**Request Body**: Same as Create Listing (all fields optional for PATCH)

**Response** (200 OK): Same as Get Listing Detail

**Error Responses**:
- `403 Forbidden`: Not the owner
- `404 Not Found`: Listing not found
- `400 Bad Request`: Cannot edit SOLD listing

---

#### Delete Listing
**Endpoint**: `DELETE /listings/{id}`

**Headers**: `Authorization: Bearer <token>`

**Response** (204 No Content)

**Error Responses**:
- `403 Forbidden`: Not the owner or admin
- `404 Not Found`: Listing not found

---

### 3.4 Favorite Endpoints

#### Add Favorite
**Endpoint**: `POST /listings/{id}/favorite`

**Headers**: `Authorization: Bearer <token>`

**Response** (201 Created):
```json
{
  "message": "Added to favorites",
  "listing_id": "listing-001"
}
```

**Error Responses**:
- `400 Bad Request`: Already favorited or cannot favorite own listing
- `404 Not Found`: Listing not found

---

#### Remove Favorite
**Endpoint**: `DELETE /listings/{id}/favorite`

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "message": "Removed from favorites"
}
```

---

#### List User's Favorites
**Endpoint**: `GET /users/me/favorites`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**: Same as List Listings (pagination)

**Response** (200 OK): Same format as List Listings

---

### 3.5 Offer Endpoints

#### Create Offer
**Endpoint**: `POST /offers`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "listing_id": "listing-001",
  "price": "23000000",
  "message": "I can pick up today"
}
```

**Response** (201 Created):
```json
{
  "id": "offer-001",
  "listing": {
    "id": "listing-001",
    "title": "MacBook Pro 2020"
  },
  "buyer": {
    "id": "user-002",
    "full_name": "Jane Smith"
  },
  "price": "23000000",
  "message": "I can pick up today",
  "status": "PENDING",
  "created_at": "2024-01-16T14:20:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid price, listing not available, already has pending offer
- `404 Not Found`: Listing not found

---

#### List Offers for Listing
**Endpoint**: `GET /listings/{id}/offers`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `status` (string, optional): PENDING, ACCEPTED, REJECTED
- `page`, `page_size`: Pagination

**Response** (200 OK):
```json
{
  "count": 5,
  "results": [
    {
      "id": "offer-001",
      "buyer": {
        "id": "user-002",
        "full_name": "Jane Smith",
        "avatar": "/media/avatars/user002.jpg"
      },
      "price": "23000000",
      "message": "I can pick up today",
      "status": "PENDING",
      "created_at": "2024-01-16T14:20:00Z"
    }
  ]
}
```

**Note**: Chỉ seller của listing mới có thể xem offers.

---

#### Accept Offer
**Endpoint**: `POST /offers/{id}/accept`

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "message": "Offer accepted, deal created",
  "offer": {
    "id": "offer-001",
    "status": "ACCEPTED"
  },
  "deal": {
    "id": "deal-001",
    "status": "PENDING",
    "created_at": "2024-01-16T15:00:00Z"
  }
}
```

**Error Responses**:
- `403 Forbidden`: Not the seller
- `400 Bad Request`: Offer already processed or listing not available

---

#### Reject Offer
**Endpoint**: `POST /offers/{id}/reject`

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "message": "Offer rejected",
  "offer": {
    "id": "offer-001",
    "status": "REJECTED"
  }
}
```

---

### 3.6 Deal Endpoints

#### Get Deal Detail
**Endpoint**: `GET /deals/{id}`

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "id": "deal-001",
  "listing": {
    "id": "listing-001",
    "title": "MacBook Pro 2020"
  },
  "buyer": {
    "id": "user-002",
    "full_name": "Jane Smith"
  },
  "seller": {
    "id": "user-001",
    "full_name": "John Doe"
  },
  "offer": {
    "id": "offer-001",
    "price": "23000000"
  },
  "status": "PENDING",
  "meetups": [
    {
      "id": "meetup-001",
      "scheduled_at": "2024-01-20T10:00:00Z",
      "location": "Coffee Shop XYZ",
      "notes": "Near the entrance"
    }
  ],
  "created_at": "2024-01-16T15:00:00Z",
  "updated_at": "2024-01-16T15:00:00Z"
}
```

---

#### Create Meetup
**Endpoint**: `POST /deals/{id}/meetups`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "scheduled_at": "2024-01-20T10:00:00Z",
  "location": "Coffee Shop XYZ",
  "notes": "Near the entrance"
}
```

**Response** (201 Created):
```json
{
  "id": "meetup-001",
  "deal_id": "deal-001",
  "scheduled_at": "2024-01-20T10:00:00Z",
  "location": "Coffee Shop XYZ",
  "notes": "Near the entrance",
  "created_at": "2024-01-16T16:00:00Z"
}
```

---

#### Update Deal Status
**Endpoint**: `PATCH /deals/{id}`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "status": "COMPLETED"
}
```

**Valid status transitions**:
- PENDING → CONFIRMED (both buyer/seller)
- PENDING → CANCELLED (both buyer/seller)
- CONFIRMED → COMPLETED (both buyer/seller)
- CONFIRMED → CANCELLED (both buyer/seller)

**Response** (200 OK): Updated deal object

---

### 3.7 Chat Endpoints

#### List Conversations
**Endpoint**: `GET /conversations`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**: `page`, `page_size`

**Response** (200 OK):
```json
{
  "count": 10,
  "results": [
    {
      "id": "conv-001",
      "listing": {
        "id": "listing-001",
        "title": "MacBook Pro 2020",
        "image": "/media/listings/img001.jpg"
      },
      "other_user": {
        "id": "user-002",
        "full_name": "Jane Smith",
        "avatar": "/media/avatars/user002.jpg"
      },
      "last_message": {
        "content": "Hello, is this still available?",
        "sent_at": "2024-01-16T14:00:00Z"
      },
      "unread_count": 2,
      "updated_at": "2024-01-16T14:00:00Z"
    }
  ]
}
```

---

#### Get Conversation Messages
**Endpoint**: `GET /conversations/{id}/messages`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**: `page`, `page_size` (default: 50 messages per page)

**Response** (200 OK):
```json
{
  "count": 25,
  "next": null,
  "previous": "http://api.example.com/api/v1/conversations/conv-001/messages?page=1",
  "results": [
    {
      "id": "msg-001",
      "sender": {
        "id": "user-002",
        "full_name": "Jane Smith",
        "avatar": "/media/avatars/user002.jpg"
      },
      "content": "Hello, is this still available?",
      "sent_at": "2024-01-16T14:00:00Z",
      "read_at": "2024-01-16T14:05:00Z"
    },
    {
      "id": "msg-002",
      "sender": {
        "id": "user-001",
        "full_name": "John Doe",
        "avatar": "/media/avatars/user001.jpg"
      },
      "content": "Yes, it's still available",
      "sent_at": "2024-01-16T14:02:00Z",
      "read_at": null
    }
  ]
}
```

---

### 3.8 Report Endpoints

#### Create Report
**Endpoint**: `POST /reports`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "reported_listing_id": "listing-001",
  "report_type": "SPAM",
  "description": "This listing is spam"
}
```

Hoặc:
```json
{
  "reported_user_id": "user-001",
  "report_type": "SCAM",
  "description": "This user is a scammer"
}
```

**Response** (201 Created):
```json
{
  "id": "report-001",
  "reported_listing": {
    "id": "listing-001",
    "title": "MacBook Pro 2020"
  },
  "report_type": "SPAM",
  "description": "This listing is spam",
  "status": "PENDING",
  "created_at": "2024-01-16T17:00:00Z"
}
```

---

#### Block User
**Endpoint**: `POST /users/{id}/block`

**Headers**: `Authorization: Bearer <token>`

**Response** (201 Created):
```json
{
  "message": "User blocked",
  "blocked_user_id": "user-001"
}
```

---

### 3.9 Admin Endpoints

#### List Reports
**Endpoint**: `GET /admin/reports`

**Headers**: `Authorization: Bearer <admin_token>`

**Query Parameters**:
- `status` (string, optional): PENDING, RESOLVED, DISMISSED
- `report_type` (string, optional): SPAM, INAPPROPRIATE, SCAM, OTHER
- `page`, `page_size`

**Response** (200 OK): List of reports với đầy đủ thông tin

---

#### Resolve Report
**Endpoint**: `POST /admin/reports/{id}/resolve`

**Headers**: `Authorization: Bearer <admin_token>`

**Request Body**:
```json
{
  "action": "BAN_USER",
  "reason": "User violated terms of service"
}
```

**Actions**: `DISMISS`, `WARN_USER`, `BAN_USER`, `REMOVE_LISTING`

**Response** (200 OK):
```json
{
  "message": "Report resolved",
  "report": {
    "id": "report-001",
    "status": "RESOLVED",
    "resolved_by": "admin-001",
    "resolved_at": "2024-01-17T10:00:00Z"
  }
}
```

---

#### Ban User
**Endpoint**: `POST /admin/users/{id}/ban`

**Headers**: `Authorization: Bearer <admin_token>`

**Request Body**:
```json
{
  "reason": "Violated terms of service"
}
```

**Response** (200 OK):
```json
{
  "message": "User banned",
  "user": {
    "id": "user-001",
    "status": "BANNED"
  }
}
```

---

## 4. WebSocket API

### 4.1 Connection

**Endpoint**: `ws://localhost:8000/ws/chat/`

**Authentication**: JWT token trong query string:
```
ws://localhost:8000/ws/chat/?token=<jwt_token>
```

Hoặc trong header (nếu supported):
```
Authorization: Bearer <jwt_token>
```

**Connection Flow**:
1. Client establishes WebSocket connection với token
2. Server validates token
3. Server sends `connection_established` message
4. Client can now send/receive messages

---

### 4.2 Message Types

#### Client → Server Messages

##### Join Conversation
```json
{
  "type": "join_conversation",
  "conversation_id": "conv-001"
}
```

**Response** (Server → Client):
```json
{
  "type": "conversation_joined",
  "conversation_id": "conv-001"
}
```

---

##### Send Message
```json
{
  "type": "send_message",
  "conversation_id": "conv-001",
  "content": "Hello, is this still available?"
}
```

**Response** (Server → Client):
```json
{
  "type": "message_sent",
  "message": {
    "id": "msg-001",
    "conversation_id": "conv-001",
    "sender": {
      "id": "user-002",
      "full_name": "Jane Smith"
    },
    "content": "Hello, is this still available?",
    "sent_at": "2024-01-16T14:00:00Z"
  }
}
```

**Broadcast** (Server → Other Client):
```json
{
  "type": "message_received",
  "message": {
    "id": "msg-001",
    "conversation_id": "conv-001",
    "sender": {
      "id": "user-002",
      "full_name": "Jane Smith"
    },
    "content": "Hello, is this still available?",
    "sent_at": "2024-01-16T14:00:00Z"
  }
}
```

---

##### Typing Indicator
```json
{
  "type": "typing",
  "conversation_id": "conv-001",
  "is_typing": true
}
```

**Broadcast** (Server → Other Client):
```json
{
  "type": "user_typing",
  "conversation_id": "conv-001",
  "user": {
    "id": "user-002",
    "full_name": "Jane Smith"
  },
  "is_typing": true
}
```

---

##### Mark as Read
```json
{
  "type": "mark_read",
  "conversation_id": "conv-001",
  "message_id": "msg-001"
}
```

**Response** (Server → Client):
```json
{
  "type": "read_receipt",
  "conversation_id": "conv-001",
  "message_id": "msg-001",
  "read_at": "2024-01-16T14:05:00Z"
}
```

---

#### Server → Client Messages

##### Error
```json
{
  "type": "error",
  "error": "Invalid conversation",
  "code": "INVALID_CONVERSATION"
}
```

**Error Codes**:
- `INVALID_CONVERSATION`: Conversation not found or access denied
- `INVALID_MESSAGE`: Message validation failed
- `UNAUTHORIZED`: Authentication failed
- `SERVER_ERROR`: Internal server error

---

##### Connection Established
```json
{
  "type": "connection_established",
  "user_id": "user-001",
  "timestamp": "2024-01-16T14:00:00Z"
}
```

---

### 4.3 WebSocket Events Summary

| Event | Direction | Description |
|-------|-----------|-------------|
| `join_conversation` | Client → Server | Join a conversation |
| `send_message` | Client → Server | Send a chat message |
| `typing` | Client → Server | Typing indicator |
| `mark_read` | Client → Server | Mark message as read |
| `connection_established` | Server → Client | Connection confirmed |
| `conversation_joined` | Server → Client | Joined conversation |
| `message_sent` | Server → Client | Message sent confirmation |
| `message_received` | Server → Client | New message received |
| `user_typing` | Server → Client | Other user typing |
| `read_receipt` | Server → Client | Message read receipt |
| `error` | Server → Client | Error occurred |

---

## 5. Error Handling

### 5.1 Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "email": ["This field is required."],
      "password": ["Password must be at least 8 characters."]
    }
  }
}
```

### 5.2 HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation errors, invalid input |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but no permission |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource conflict (e.g., email exists) |
| 500 | Internal Server Error | Server error |

### 5.3 Error Codes

| Code | Description |
|------|-------------|
| `VALIDATION_ERROR` | Input validation failed |
| `AUTHENTICATION_ERROR` | Authentication failed |
| `PERMISSION_DENIED` | No permission |
| `NOT_FOUND` | Resource not found |
| `DUPLICATE_ENTRY` | Duplicate resource |
| `INVALID_STATE` | Invalid state transition |
| `SERVER_ERROR` | Internal server error |

---

## 6. Request/Response Formats

### 6.1 Pagination

Tất cả list endpoints sử dụng pagination:

**Query Parameters**:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

**Response Format**:
```json
{
  "count": 150,
  "next": "http://api.example.com/api/v1/resource?page=3",
  "previous": "http://api.example.com/api/v1/resource?page=1",
  "results": [...]
}
```

### 6.2 Date/Time Format

ISO 8601 format: `YYYY-MM-DDTHH:mm:ssZ`

Example: `2024-01-16T14:30:00Z`

### 6.3 Decimal Format

Prices sử dụng string để tránh precision issues:
```json
{
  "price": "25000000"
}
```

### 6.4 File Upload

**Content-Type**: `multipart/form-data`

**Example** (cURL):
```bash
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -F "title=MacBook Pro" \
  -F "description=Good condition" \
  -F "price=25000000" \
  -F "images=@image1.jpg" \
  -F "images=@image2.jpg" \
  http://api.example.com/api/v1/listings
```

---

## 7. Rate Limiting

**Current**: No rate limiting (MVP)

**Future**: Implement rate limiting để prevent abuse:
- 100 requests/minute per user
- 10 requests/minute cho authentication endpoints

---

## 8. References

- Django REST Framework: https://www.django-rest-framework.org/
- Django Channels: https://channels.readthedocs.io/
- JWT: https://jwt.io/
- REST API Best Practices: https://restfulapi.net/

---

**End of Document**

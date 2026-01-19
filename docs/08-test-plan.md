# Test Plan
## OldGoods Marketplace

**Version**: 1.0  
**Date**: 2024  
**Test Manager**: Development Team

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Test Scope](#2-test-scope)
3. [Test Strategy](#3-test-strategy)
4. [Test Levels](#4-test-levels)
5. [Test Cases](#5-test-cases)
6. [Test Environment](#6-test-environment)
7. [Test Deliverables](#7-test-deliverables)
8. [Defect Management](#8-defect-management)

---

## 1. Introduction

### 1.1 Purpose
Tài liệu này mô tả chiến lược và kế hoạch testing cho hệ thống OldGoods Marketplace, bao gồm các test levels, test cases, và test environment.

### 1.2 Scope
Test plan bao gồm:
- Unit tests cho domain logic và services
- Integration tests cho API endpoints và database
- System tests cho end-to-end workflows
- Security tests cho authentication và authorization
- Performance tests cho API response times

> **Tech stack áp dụng cho Test Plan**: FastAPI + SQLAlchemy + Alembic + PostgreSQL (+ Redis optional cho realtime).

### 1.3 Objectives
- Đảm bảo tất cả use cases hoạt động đúng
- Đảm bảo code quality và reliability
- Đạt test coverage > 60% cho domain/application layers
- Identify và fix bugs trước khi release

---

## 2. Test Scope

### 2.1 In-Scope

#### Functional Testing
- Authentication (Register, Login, Logout)
- User Profile Management
- Listing CRUD operations
- Search & Filter functionality
- Favorite functionality
- Chat (WebSocket) functionality
- Offer & Deal workflow
- Report & Block functionality
- Admin moderation features

#### Non-Functional Testing
- API performance (response time)
- WebSocket message delivery
- Database query performance
- Security (authentication, authorization, input validation)
- Error handling và recovery

### 2.2 Out-of-Scope

#### Not Testing
- UI/UX testing (frontend not in scope)
- Load testing với large scale (1000+ concurrent users)
- Browser compatibility (assume modern browsers)
- Mobile app testing (web only)

---

## 3. Test Strategy

### 3.1 Testing Approach

#### 3.1.1 Test Pyramid
```
        /\
       /  \      E2E Tests (10%)
      /____\     
     /      \    Integration Tests (30%)
    /________\   
   /          \  Unit Tests (60%)
  /____________\
```

- **Unit Tests (60%)**: Test individual functions, methods, classes
- **Integration Tests (30%)**: Test API endpoints, database interactions
- **E2E Tests (10%)**: Test complete user workflows

### 3.2 Test Types

#### 3.2.1 Unit Tests
- **Purpose**: Test individual components in isolation
- **Tools**: pytest, pytest-django
- **Coverage Target**: > 60% cho domain/application layers
- **Examples**:
  - Domain entity validation
  - Business logic trong services
  - Utility functions

#### 3.2.2 Integration Tests
- **Purpose**: Test interactions giữa components
- **Tools**: pytest, pytest-django, Django TestClient
- **Examples**:
  - API endpoints với database
  - Authentication flow
  - Database transactions

#### 3.2.3 System/E2E Tests
- **Purpose**: Test complete user workflows
- **Tools**: pytest, Django TestClient, WebSocket client
- **Examples**:
  - Register → Login → Create Listing → Search → Chat → Offer → Deal
  - Admin workflow: View Reports → Resolve Report → Ban User

#### 3.2.4 Security Tests
- **Purpose**: Test security vulnerabilities
- **Tools**: pytest, manual testing
- **Examples**:
  - SQL injection prevention
  - XSS prevention
  - Authentication bypass attempts
  - Authorization checks

#### 3.2.5 Performance Tests
- **Purpose**: Test response times và throughput
- **Tools**: pytest, Locust (optional)
- **Examples**:
  - API response time < 500ms
  - Search query < 1s với 5000 listings
  - WebSocket message delivery < 100ms

---

## 4. Test Levels

### 4.1 Level 1: Unit Tests

#### 4.1.1 Domain Layer Tests
**Files**: `tests/unit/test_domain_*.py`

**Test Cases**:
- User entity validation
- Listing entity validation và business rules
- Offer validation (price <= listing price)
- Deal status transitions
- Message validation

**Example**:
```python
def test_listing_cannot_be_edited_when_sold():
    listing = Listing(status=ListingStatus.SOLD)
    with pytest.raises(InvalidStateError):
        listing.update_title("New Title")
```

---

#### 4.1.2 Application Layer Tests
**Files**: `tests/unit/test_services_*.py`

**Test Cases**:
- ListingService.create_listing()
- OfferService.create_offer()
- OfferService.accept_offer() (reject other offers)
- DealService.complete_deal()
- ChatService.send_message()

**Example**:
```python
def test_accept_offer_rejects_other_offers():
    listing = create_listing()
    offer1 = create_offer(listing)
    offer2 = create_offer(listing)
    
    offer_service.accept_offer(offer1.id)
    
    assert offer1.status == OfferStatus.ACCEPTED
    assert offer2.status == OfferStatus.REJECTED
```

---

### 4.2 Level 2: Integration Tests

#### 4.2.1 API Integration Tests
**Files**: `tests/integration/test_api_*.py`

**Test Cases**:
- POST /auth/register → creates user và profile
- POST /auth/login → returns JWT token
- POST /listings → creates listing với images
- GET /listings?search=... → returns filtered results
- POST /offers → creates offer
- POST /offers/{id}/accept → creates deal và updates listing

**Example**:
```python
def test_create_listing_api(client, authenticated_user):
    data = {
        "title": "Test Listing",
        "description": "Test",
        "category_id": category.id,
        "price": "1000000",
        "condition": "USED",
        "location": "HCM"
    }
    files = {"images": [test_image]}
    
    response = client.post("/api/v1/listings/", data=data, files=files)
    
    assert response.status_code == 201
    assert response.json()["title"] == "Test Listing"
```

---

#### 4.2.2 Database Integration Tests
**Files**: `tests/integration/test_db_*.py`

**Test Cases**:
- Database transactions (rollback on error)
- Foreign key constraints
- Unique constraints
- Cascade deletes

**Example**:
```python
def test_delete_user_cascades_to_listings():
    user = create_user()
    listing = create_listing(seller=user)
    
    user.delete()
    
    assert Listing.objects.filter(id=listing.id).exists() == False
```

---

#### 4.2.3 WebSocket Integration Tests
**Files**: `tests/integration/test_websocket_*.py`

**Test Cases**:
- WebSocket connection với authentication
- Send message → saved to database → broadcast to receiver
- Join conversation
- Typing indicator
- Read receipt

**Example**:
```python
@pytest.mark.asyncio
async def test_send_message_saves_to_database():
    conversation = create_conversation()
    consumer = ChatConsumer()
    
    await consumer.send_message({
        "conversation_id": conversation.id,
        "content": "Test message"
    })
    
    assert Message.objects.filter(content="Test message").exists()
```

---

### 4.3 Level 3: System/E2E Tests

#### 4.3.1 User Workflows
**Files**: `tests/e2e/test_workflows_*.py`

**Test Cases**:
- **Workflow 1**: Register → Login → Create Listing → Search → View Detail
- **Workflow 2**: Buyer → Search → View Listing → Chat → Create Offer → Seller Accept → Create Deal → Schedule Meetup → Complete Deal
- **Workflow 3**: User → Report Listing → Admin View Report → Admin Resolve → Ban User

**Example**:
```python
def test_complete_buyer_seller_workflow(client):
    # Register buyer và seller
    buyer = register_user(client, "buyer@test.com")
    seller = register_user(client, "seller@test.com")
    
    # Seller creates listing
    listing = create_listing(client, seller_token)
    
    # Buyer searches và views listing
    search_results = search_listings(client, "laptop")
    assert listing.id in [r["id"] for r in search_results]
    
    # Buyer creates offer
    offer = create_offer(client, buyer_token, listing.id)
    
    # Seller accepts offer → creates deal
    deal = accept_offer(client, seller_token, offer.id)
    
    # Both schedule meetup
    meetup = create_meetup(client, buyer_token, deal.id)
    
    # Complete deal
    complete_deal(client, buyer_token, deal.id)
    
    # Verify listing status is SOLD
    listing = get_listing(client, listing.id)
    assert listing["status"] == "SOLD"
```

---

### 4.4 Level 4: Security Tests

#### 4.4.1 Authentication Tests
**Files**: `tests/security/test_auth_*.py`

**Test Cases**:
- Invalid credentials → 401
- Expired token → 401
- Missing token → 401
- Password hash verification (not plain text)
- JWT token validation

---

#### 4.4.2 Authorization Tests
**Files**: `tests/security/test_authorization_*.py`

**Test Cases**:
- User cannot edit other user's listing → 403
- User cannot accept offer for other user's listing → 403
- Guest cannot create listing → 401
- User cannot access admin endpoints → 403
- Only admin can resolve reports → 403

---

#### 4.4.3 Input Validation Tests
**Files**: `tests/security/test_validation_*.py`

**Test Cases**:
- SQL injection attempts → rejected
- XSS payloads → escaped/sanitized
- File upload validation (type, size)
- Price validation (must be > 0)

---

## 5. Test Cases

### 5.1 Use Case Test Cases

#### UC01: Register
**Test ID**: TC-UC01-001  
**Description**: User đăng ký thành công với email hợp lệ  
**Preconditions**: Email chưa tồn tại  
**Steps**:
1. POST /auth/register với email, password, full_name
2. Verify response status 201
3. Verify user được tạo trong database
4. Verify profile được tạo

**Expected Result**: User và profile được tạo thành công

---

**Test ID**: TC-UC01-002  
**Description**: Register fails với email đã tồn tại  
**Preconditions**: Email đã tồn tại  
**Steps**:
1. POST /auth/register với email đã tồn tại
2. Verify response status 409

**Expected Result**: Error message "Email already exists"

---

#### UC02: Login
**Test ID**: TC-UC02-001  
**Description**: Login thành công với credentials hợp lệ  
**Preconditions**: User đã tồn tại  
**Steps**:
1. POST /auth/login với email và password đúng
2. Verify response status 200
3. Verify response contains access và refresh tokens
4. Verify token có thể dùng để authenticate

**Expected Result**: JWT tokens được trả về và valid

---

#### UC04: Create Listing
**Test ID**: TC-UC04-001  
**Description**: Seller tạo listing thành công  
**Preconditions**: User đã đăng nhập  
**Steps**:
1. POST /listings với title, description, category, price, images
2. Verify response status 201
3. Verify listing được tạo trong database
4. Verify images được lưu
5. Verify listing status là AVAILABLE

**Expected Result**: Listing được tạo với status AVAILABLE

---

**Test ID**: TC-UC04-002  
**Description**: Create listing fails khi không có images  
**Preconditions**: User đã đăng nhập  
**Steps**:
1. POST /listings không có images
2. Verify response status 400

**Expected Result**: Error "At least one image required"

---

#### UC05: Search & Filter
**Test ID**: TC-UC05-001  
**Description**: Search listings với keyword  
**Preconditions**: Có listings trong database  
**Steps**:
1. GET /listings?search=laptop
2. Verify response status 200
3. Verify results chỉ chứa listings có "laptop" trong title/description
4. Verify pagination works

**Expected Result**: Filtered results được trả về

---

#### UC10: Send Message
**Test ID**: TC-UC10-001  
**Description**: Send message qua WebSocket  
**Preconditions**: 
- User đã đăng nhập
- Conversation đã tồn tại
- WebSocket connection established

**Steps**:
1. Send message qua WebSocket: `{"type": "send_message", "conversation_id": "...", "content": "Hello"}`
2. Verify message được lưu trong database
3. Verify message được broadcast đến receiver
4. Verify sender nhận confirmation

**Expected Result**: Message được lưu và deliver thành công

---

#### UC12: Make Offer
**Test ID**: TC-UC12-001  
**Description**: Buyer tạo offer thành công  
**Preconditions**: 
- Buyer đã đăng nhập
- Listing tồn tại và có status AVAILABLE

**Steps**:
1. POST /offers với listing_id, price
2. Verify response status 201
3. Verify offer được tạo với status PENDING
4. Verify offer price <= listing price

**Expected Result**: Offer được tạo thành công

---

**Test ID**: TC-UC12-002  
**Description**: Create offer fails khi price > listing price  
**Preconditions**: Listing tồn tại  
**Steps**:
1. POST /offers với price > listing.price
2. Verify response status 400

**Expected Result**: Error "Offer price cannot exceed listing price"

---

#### UC13: Accept Offer
**Test ID**: TC-UC13-001  
**Description**: Seller accept offer → creates deal  
**Preconditions**: 
- Seller đã đăng nhập
- Offer tồn tại và có status PENDING
- Listing có status AVAILABLE

**Steps**:
1. POST /offers/{id}/accept
2. Verify response status 200
3. Verify offer status → ACCEPTED
4. Verify deal được tạo với status PENDING
5. Verify listing status → RESERVED
6. Verify other offers cho listing này → REJECTED

**Expected Result**: Deal được tạo, listing → RESERVED, other offers → REJECTED

---

### 5.2 Security Test Cases

#### SEC-001: SQL Injection Prevention
**Test ID**: TC-SEC-001  
**Description**: SQL injection attempts bị reject  
**Steps**:
1. POST /listings với title: `'; DROP TABLE listings; --`
2. Verify response status 400 hoặc 500 (không crash)
3. Verify database không bị modify

**Expected Result**: SQL injection bị reject, database safe

---

#### SEC-002: XSS Prevention
**Test ID**: TC-SEC-002  
**Description**: XSS payloads được escape  
**Steps**:
1. POST /listings với description: `<script>alert('XSS')</script>`
2. Verify response status 201
3. GET /listings/{id}
4. Verify description được escape trong response

**Expected Result**: XSS payload được escape, không execute

---

#### SEC-003: Authorization Check
**Test ID**: TC-SEC-003  
**Description**: User cannot edit other user's listing  
**Preconditions**: 
- User A có listing
- User B đã đăng nhập

**Steps**:
1. User B: PUT /listings/{user_a_listing_id}
2. Verify response status 403

**Expected Result**: 403 Forbidden

---

## 6. Test Environment

### 6.1 Test Environment Setup

#### 6.1.1 Development Environment
- **Database**: PostgreSQL (local hoặc Docker)
- **Redis**: Redis (local hoặc Docker) hoặc InMemoryChannelLayer
- **Python**: 3.10+
- **Django**: 4.2+
- **Test Database**: Separate test database (Django tự động tạo)

#### 6.1.2 Test Data
- **Fixtures**: `tests/fixtures/` chứa sample data
- **Factories**: Sử dụng Factory Boy để tạo test data
- **Seeding**: Script để seed test data cho integration tests

### 6.2 Test Execution

#### 6.2.1 Running Tests
```bash
# Run all tests
pytest

# Run với coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_listing_service.py

# Run specific test
pytest tests/unit/test_listing_service.py::test_create_listing
```

#### 6.2.2 CI/CD Integration
- Tests chạy tự động trong CI/CD pipeline
- Tests phải pass trước khi merge code
- Coverage report được generate và track

---

## 7. Test Deliverables

### 7.1 Test Artifacts

#### 7.1.1 Test Plan
- This document

#### 7.1.2 Test Cases
- Test cases trong test files (pytest format)
- Test case documentation trong code comments

#### 7.1.3 Test Scripts
- Automated test scripts (pytest)
- Manual test scripts (nếu có)

#### 7.1.4 Test Reports
- Test execution reports
- Coverage reports
- Defect reports

### 7.2 Test Metrics

#### 7.2.1 Coverage Metrics
- **Target**: > 60% coverage cho domain/application layers
- **Critical**: 100% coverage cho business logic

#### 7.2.2 Test Execution Metrics
- Total test cases
- Passed/Failed/Skipped
- Execution time

#### 7.2.3 Defect Metrics
- Total defects found
- Defects by severity
- Defects by component

---

## 8. Defect Management

### 8.1 Defect Severity

#### Critical
- System crash
- Data loss
- Security vulnerability
- Blocking use case

#### High
- Major functionality không hoạt động
- Performance issue nghiêm trọng
- Workaround available

#### Medium
- Minor functionality issue
- UI/UX issue
- Non-blocking

#### Low
- Cosmetic issue
- Documentation issue
- Enhancement suggestion

### 8.2 Defect Lifecycle

1. **Open**: Defect được tìm thấy và logged
2. **Assigned**: Defect được assign cho developer
3. **In Progress**: Developer đang fix
4. **Fixed**: Fix đã được implement
5. **Verified**: Tester verify fix
6. **Closed**: Defect được close

### 8.3 Defect Reporting

**Defect Report Template**:
- Defect ID
- Title
- Description
- Steps to Reproduce
- Expected Result
- Actual Result
- Severity
- Priority
- Status
- Assigned To
- Found By
- Found Date

---

## 9. Test Schedule

### 9.1 Sprint 1 Testing
- Unit tests cho User và Listing models
- Integration tests cho Auth và Listing APIs
- **Target**: 50% coverage

### 9.2 Sprint 2 Testing
- Unit tests cho Search và Favorite
- Integration tests cho Search API
- **Target**: 60% coverage

### 9.3 Sprint 3 Testing
- Unit tests cho Chat service
- Integration tests cho WebSocket
- E2E tests cho Chat workflow
- **Target**: 65% coverage

### 9.4 Sprint 4 Testing
- Unit tests cho Deal và Moderation
- E2E tests cho complete workflows
- Security tests
- Performance tests
- **Target**: 70% coverage

---

## 10. Risk & Mitigation

### 10.1 Testing Risks

#### Risk 1: Insufficient Test Coverage
- **Mitigation**: Set coverage targets, review coverage reports

#### Risk 2: WebSocket Testing Complexity
- **Mitigation**: Use pytest-asyncio, mock WebSocket connections

#### Risk 3: Test Data Management
- **Mitigation**: Use factories, fixtures, test database isolation

---

## 11. References

- pytest Documentation: https://docs.pytest.org/
- pytest-django: https://pytest-django.readthedocs.io/
- Django Testing: https://docs.djangoproject.com/en/stable/topics/testing/
- Factory Boy: https://factoryboy.readthedocs.io/

---

**End of Document**

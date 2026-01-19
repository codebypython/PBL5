# Non-Functional Requirements (NFR)
## OldGoods Marketplace

**Version**: 1.0  
**Date**: 2024

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Performance Requirements](#2-performance-requirements)
3. [Security Requirements](#3-security-requirements)
4. [Reliability Requirements](#4-reliability-requirements)
5. [Maintainability Requirements](#5-maintainability-requirements)
6. [Scalability Requirements](#6-scalability-requirements)
7. [Usability Requirements](#7-usability-requirements)
8. [Portability Requirements](#8-portability-requirements)
9. [Compatibility Requirements](#9-compatibility-requirements)

---

## 1. Introduction

### 1.1 Purpose
Tài liệu này mô tả các yêu cầu phi chức năng (Non-Functional Requirements) của hệ thống OldGoods Marketplace. Các yêu cầu này định nghĩa chất lượng, hiệu suất, và các thuộc tính hệ thống không liên quan trực tiếp đến chức năng cụ thể.

### 1.2 Scope
Tài liệu bao gồm các yêu cầu về:
- Performance (hiệu suất)
- Security (bảo mật)
- Reliability (độ tin cậy)
- Maintainability (khả năng bảo trì)
- Scalability (khả năng mở rộng)
- Usability (khả năng sử dụng)
- Portability (khả năng di chuyển)
- Compatibility (tương thích)

### 1.3 Format
Mỗi yêu cầu được mô tả theo format:
- **Scenario**: Tình huống sử dụng
- **Requirement**: Yêu cầu cụ thể
- **Constraints**: Ràng buộc và giới hạn
- **Verification**: Cách kiểm tra/đo lường

---

## 2. Performance Requirements

### 2.1 API Response Time

#### NFR-PERF-001: API Endpoint Response Time
- **Scenario**: User gọi API endpoint để lấy dữ liệu
- **Requirement**: 
  - 95% các API requests phải trả về response trong vòng 500ms
  - 99% các API requests phải trả về response trong vòng 1s
- **Constraints**: 
  - Đo trong môi trường test với database có 10,000 listings
  - Network latency không tính vào response time
- **Verification**: 
  - Sử dụng load testing tool (Apache JMeter, Locust)
  - Monitor response time metrics
  - Target: P95 < 500ms, P99 < 1s

#### NFR-PERF-002: Search Performance
- **Scenario**: User thực hiện tìm kiếm với keyword và filters
- **Requirement**: 
  - Search query phải trả về kết quả trong vòng 1s với database có 5,000 listings
  - Search query phải trả về kết quả trong vòng 2s với database có 50,000 listings
- **Constraints**: 
  - Database có indexes phù hợp trên các cột search (title, description, category, price)
  - Kết quả được paginated (20 items/page)
- **Verification**: 
  - Performance test với database có số lượng listings khác nhau
  - Monitor query execution time trong PostgreSQL
  - Target: < 1s cho 5K listings, < 2s cho 50K listings

#### NFR-PERF-003: Image Upload Performance
- **Scenario**: User upload hình ảnh cho listing
- **Requirement**: 
  - Upload 1 ảnh (< 5MB) phải hoàn thành trong vòng 5s
  - Upload 5 ảnh (< 5MB mỗi ảnh) phải hoàn thành trong vòng 15s
- **Constraints**: 
  - Network upload speed: tối thiểu 1 Mbps
  - Image được resize/compress nếu cần
- **Verification**: 
  - Test upload với các kích thước file khác nhau
  - Monitor upload time và success rate
  - Target: 100% success rate, < 5s cho 1 ảnh

#### NFR-PERF-004: WebSocket Message Delivery
- **Scenario**: User gửi tin nhắn qua WebSocket
- **Requirement**: 
  - Message phải được deliver đến receiver trong vòng 100ms (khi cả 2 users đều online)
  - Message phải được lưu database trong vòng 200ms
- **Constraints**: 
  - Cả sender và receiver đều có WebSocket connection active
  - Database connection pool đủ
- **Verification**: 
  - Monitor WebSocket message latency
  - Monitor database write time
  - Target: < 100ms delivery, < 200ms DB write

### 2.2 Throughput

#### NFR-PERF-005: Concurrent Users
- **Scenario**: Nhiều users sử dụng hệ thống đồng thời
- **Requirement**: 
  - Hệ thống phải hỗ trợ ít nhất 100 concurrent users
  - Hệ thống phải hỗ trợ ít nhất 50 concurrent WebSocket connections
- **Constraints**: 
  - Server có đủ resources (CPU, RAM)
  - Database connection pool được cấu hình đúng
- **Verification**: 
  - Load testing với số lượng concurrent users tăng dần
  - Monitor server resources và response times
  - Target: 100 concurrent users với response time < 1s

#### NFR-PERF-006: Database Query Throughput
- **Scenario**: Hệ thống xử lý nhiều database queries đồng thời
- **Requirement**: 
  - Database phải xử lý ít nhất 100 queries/second
  - Read queries phải chiếm 80% tổng số queries
- **Constraints**: 
  - Database có indexes phù hợp
  - Connection pooling được cấu hình
- **Verification**: 
  - Monitor database query rate
  - Target: > 100 queries/second

### 2.3 Resource Utilization

#### NFR-PERF-007: Server Resource Usage
- **Scenario**: Hệ thống chạy với tải bình thường
- **Requirement**: 
  - CPU usage < 70% trong điều kiện bình thường
  - RAM usage < 80% trong điều kiện bình thường
  - Disk I/O không bị bottleneck
- **Constraints**: 
  - Server có đủ resources
  - Application được optimize
- **Verification**: 
  - Monitor server metrics (CPU, RAM, Disk I/O)
  - Target: CPU < 70%, RAM < 80%

---

## 3. Security Requirements

### 3.1 Authentication & Authorization

#### NFR-SEC-001: Password Security
- **Scenario**: User đăng ký hoặc đổi mật khẩu
- **Requirement**: 
  - Password phải được hash bằng bcrypt hoặc argon2 (không lưu plain text)
  - Password phải có độ dài tối thiểu 8 ký tự
  - Password phải chứa ít nhất 1 chữ hoa, 1 chữ thường, 1 số
- **Constraints**: 
  - Hash algorithm: bcrypt với cost factor >= 12 hoặc argon2
  - Password validation ở cả client và server
- **Verification**: 
  - Kiểm tra database không chứa plain text passwords
  - Test password validation rules
  - Target: 100% passwords được hash

#### NFR-SEC-002: JWT Token Security
- **Scenario**: User đăng nhập và nhận JWT token
- **Requirement**: 
  - JWT token phải có expiration time (7 ngày cho access token, 30 ngày cho refresh token)
  - JWT token phải được ký bằng secret key mạnh
  - JWT token phải được validate ở mọi API request
- **Constraints**: 
  - Secret key phải được lưu trong environment variable
  - Token được gửi qua HTTPS trong production
- **Verification**: 
  - Test token expiration
  - Test token validation
  - Test với invalid/expired tokens
  - Target: 100% API requests được authenticate

#### NFR-SEC-003: Authorization
- **Scenario**: User truy cập resource hoặc thực hiện action
- **Requirement**: 
  - User chỉ có thể truy cập resources của chính mình hoặc public resources
  - Owner chỉ có thể edit/delete listing của mình
  - Chỉ admin mới có thể access admin endpoints
- **Constraints**: 
  - Permission checks ở cả API level và business logic level
- **Verification**: 
  - Test với các users khác nhau và roles khác nhau
  - Test unauthorized access attempts
  - Target: 0 unauthorized access

### 3.2 Data Protection

#### NFR-SEC-004: Input Validation & Sanitization
- **Scenario**: User nhập dữ liệu vào form hoặc API
- **Requirement**: 
  - Tất cả user inputs phải được validate và sanitize
  - Prevent SQL injection (sử dụng ORM, không dùng raw SQL)
  - Prevent XSS (escape HTML, validate content)
  - Prevent CSRF (Django CSRF protection)
- **Constraints**: 
  - Validation ở cả client và server
  - Server-side validation là bắt buộc
- **Verification**: 
  - Test với malicious inputs (SQL injection, XSS payloads)
  - Test CSRF protection
  - Target: 0 security vulnerabilities

#### NFR-SEC-005: Data Encryption
- **Scenario**: Dữ liệu được truyền qua network hoặc lưu trong database
- **Requirement**: 
  - Tất cả communications phải sử dụng HTTPS trong production
  - Sensitive data trong database có thể được encrypt (nếu cần)
  - Passwords không bao giờ được log
- **Constraints**: 
  - SSL/TLS certificate phải hợp lệ
  - Database connections có thể sử dụng SSL
- **Verification**: 
  - Test HTTPS enforcement
  - Check SSL certificate validity
  - Target: 100% HTTPS trong production

#### NFR-SEC-006: File Upload Security
- **Scenario**: User upload hình ảnh
- **Requirement**: 
  - Chỉ cho phép upload các file types được phép (jpg, jpeg, png, webp)
  - File size limit: 5MB mỗi file
  - Scan files để detect malicious content (nếu có thể)
  - Files được lưu ở thư mục không thể execute
- **Constraints**: 
  - File validation ở cả client và server
  - Server-side validation là bắt buộc
- **Verification**: 
  - Test upload với các file types không hợp lệ
  - Test upload với files quá lớn
  - Target: 0 malicious files được upload

### 3.3 Audit & Logging

#### NFR-SEC-007: Audit Logging
- **Scenario**: User thực hiện các actions quan trọng
- **Requirement**: 
  - Log tất cả authentication events (login, logout, failed login)
  - Log các admin actions (ban user, delete listing, resolve report)
  - Logs phải chứa: timestamp, user ID, action, IP address
- **Constraints**: 
  - Logs không chứa sensitive data (passwords, tokens)
  - Logs được rotate để tránh đầy disk
- **Verification**: 
  - Check log files có đầy đủ thông tin
  - Target: 100% critical actions được log

---

## 4. Reliability Requirements

### 4.1 Availability

#### NFR-REL-001: System Uptime
- **Scenario**: Hệ thống hoạt động trong production
- **Requirement**: 
  - System uptime phải đạt ít nhất 99% (tương đương ~7.2 giờ downtime/tháng)
  - Planned maintenance phải được thông báo trước
- **Constraints**: 
  - Server có monitoring và alerting
  - Có backup và recovery plan
- **Verification**: 
  - Monitor system uptime
  - Track downtime incidents
  - Target: > 99% uptime

#### NFR-REL-002: Database Availability
- **Scenario**: Database phải accessible từ application
- **Requirement**: 
  - Database connection phải stable
  - Connection pool phải handle connection failures gracefully
  - Automatic reconnection khi connection bị mất
- **Constraints**: 
  - Database có backup strategy
  - Connection pooling được cấu hình đúng
- **Verification**: 
  - Test database connection failures
  - Monitor connection pool metrics
  - Target: < 0.1% connection failures

### 4.2 Error Handling

#### NFR-REL-003: Error Recovery
- **Scenario**: Hệ thống gặp lỗi
- **Requirement**: 
  - Application phải handle errors gracefully (không crash)
  - User phải nhận được error message rõ ràng
  - Errors phải được log để debug
  - Critical errors phải được alert đến admin
- **Constraints**: 
  - Error handling ở tất cả các layers
  - Error messages không expose sensitive information
- **Verification**: 
  - Test với các error scenarios
  - Check error logs
  - Target: 0 unhandled exceptions

#### NFR-REL-004: Data Consistency
- **Scenario**: Dữ liệu được cập nhật trong database
- **Requirement**: 
  - Database transactions phải đảm bảo ACID properties
  - Không được mất dữ liệu khi có lỗi
  - Message chat phải được lưu database trước khi gửi qua WebSocket
- **Constraints**: 
  - Sử dụng database transactions cho các operations quan trọng
  - WebSocket messages phải được persist
- **Verification**: 
  - Test transaction rollback
  - Test message persistence
  - Target: 0 data loss

### 4.3 Fault Tolerance

#### NFR-REL-005: WebSocket Reconnection
- **Scenario**: WebSocket connection bị mất
- **Requirement**: 
  - Client phải tự động reconnect khi connection bị mất
  - Messages phải được queue và gửi lại khi reconnect
  - Connection phải stable với ping/pong heartbeat
- **Constraints**: 
  - Reconnection logic ở client side
  - Server phải handle reconnection gracefully
- **Verification**: 
  - Test WebSocket disconnection scenarios
  - Monitor reconnection success rate
  - Target: > 95% successful reconnections

---

## 5. Maintainability Requirements

### 5.1 Code Quality

#### NFR-MAIN-001: Code Standards
- **Scenario**: Developer viết code
- **Requirement**: 
  - Code phải tuân thủ PEP 8 (Python style guide)
  - Code phải có comments và docstrings
  - Code phải được format bằng Black hoặc similar tool
- **Constraints**: 
  - Code review process
  - Automated linting và formatting
- **Verification**: 
  - Run linters (flake8, pylint)
  - Check code coverage
  - Target: 0 critical linting errors

#### NFR-MAIN-002: Code Organization
- **Scenario**: Code được tổ chức trong project
- **Requirement**: 
  - Code phải được tổ chức theo layered architecture (presentation/application/domain/infrastructure)
  - Mỗi module phải có trách nhiệm rõ ràng (Single Responsibility Principle)
  - Dependencies phải được quản lý rõ ràng
- **Constraints**: 
  - Follow Django best practices
  - Domain layer không phụ thuộc infrastructure layer
- **Verification**: 
  - Review code structure
  - Check dependency graph
  - Target: Clear separation of concerns

### 5.2 Testing

#### NFR-MAIN-003: Test Coverage
- **Scenario**: Code được test
- **Requirement**: 
  - Unit test coverage phải đạt ít nhất 60% cho domain/application layers
  - Critical business logic phải có 100% test coverage
  - Integration tests cho các workflows chính
- **Constraints**: 
  - Tests phải chạy nhanh và reliable
  - Tests phải được maintain cùng với code
- **Verification**: 
  - Run test coverage tool (coverage.py)
  - Review test reports
  - Target: > 60% coverage

#### NFR-MAIN-004: Test Automation
- **Scenario**: Code được commit
- **Requirement**: 
  - Tests phải chạy tự động trong CI/CD pipeline
  - Tests phải pass trước khi merge code
  - Failed tests phải block deployment
- **Constraints**: 
  - CI/CD pipeline được setup
  - Tests phải stable và không flaky
- **Verification**: 
  - Check CI/CD pipeline
  - Monitor test results
  - Target: 100% tests pass before merge

### 5.3 Documentation

#### NFR-MAIN-005: Code Documentation
- **Scenario**: Developer đọc code
- **Requirement**: 
  - Tất cả functions và classes phải có docstrings
  - API endpoints phải có documentation (OpenAPI/Swagger)
  - README phải có hướng dẫn setup và run
- **Constraints**: 
  - Documentation phải được update cùng với code
- **Verification**: 
  - Check docstring coverage
  - Review API documentation
  - Target: 100% public APIs documented

---

## 6. Scalability Requirements

### 6.1 Horizontal Scalability

#### NFR-SCAL-001: Stateless API Design
- **Scenario**: Application chạy trên nhiều servers
- **Requirement**: 
  - API phải stateless (không lưu session state trên server)
  - Authentication sử dụng JWT (stateless)
  - Có thể scale horizontally bằng cách thêm servers
- **Constraints**: 
  - Session state được lưu ở client hoặc shared storage (Redis)
- **Verification**: 
  - Test với multiple server instances
  - Target: Stateless architecture

#### NFR-SCAL-002: Database Scalability
- **Scenario**: Database phải handle nhiều queries
- **Requirement**: 
  - Database có indexes phù hợp cho search queries
  - Pagination cho tất cả list endpoints
  - Database có thể scale bằng cách optimize queries và indexes
- **Constraints**: 
  - Indexes được tạo cho các cột thường xuyên query
  - Queries được optimize
- **Verification**: 
  - Monitor query performance
  - Review database indexes
  - Target: Efficient queries với indexes

### 6.2 Caching

#### NFR-SCAL-003: Caching Strategy
- **Scenario**: Dữ liệu được truy cập thường xuyên
- **Requirement**: 
  - Cache các dữ liệu ít thay đổi (categories, user profiles)
  - Cache search results với TTL hợp lý
  - Cache invalidation khi dữ liệu thay đổi
- **Constraints**: 
  - Redis hoặc in-memory cache
  - Cache TTL phù hợp
- **Verification**: 
  - Monitor cache hit rate
  - Test cache invalidation
  - Target: > 50% cache hit rate cho cached data

---

## 7. Usability Requirements

### 7.1 User Interface

#### NFR-USA-001: Responsive Design
- **Scenario**: User truy cập từ các devices khác nhau
- **Requirement**: 
  - Website phải responsive và hoạt động tốt trên desktop, tablet, mobile
  - UI phải intuitive và dễ sử dụng
  - Loading states phải được hiển thị rõ ràng
- **Constraints**: 
  - Support các browsers hiện đại (Chrome, Firefox, Safari, Edge)
  - Mobile-first design approach
- **Verification**: 
  - Test trên các devices và browsers khác nhau
  - User testing
  - Target: Usable trên tất cả target devices

#### NFR-USA-002: Error Messages
- **Scenario**: User gặp lỗi
- **Requirement**: 
  - Error messages phải rõ ràng và dễ hiểu
  - Error messages phải hướng dẫn user cách fix
  - Validation errors phải hiển thị ở field tương ứng
- **Constraints**: 
  - Error messages không expose technical details
  - Error messages phải friendly
- **Verification**: 
  - Review error messages
  - User testing
  - Target: Clear và helpful error messages

### 7.2 Accessibility

#### NFR-USA-003: Web Accessibility
- **Scenario**: User với disabilities sử dụng website
- **Requirement**: 
  - Website phải tuân thủ WCAG 2.1 Level AA (nếu có thể)
  - Images phải có alt text
  - Forms phải có labels
  - Keyboard navigation phải hoạt động
- **Constraints**: 
  - Accessibility là nice-to-have cho MVP
- **Verification**: 
  - Accessibility testing tools
  - Target: Basic accessibility support

---

## 8. Portability Requirements

### 8.1 Platform Independence

#### NFR-PORT-001: Operating System
- **Scenario**: Application được deploy trên các OS khác nhau
- **Requirement**: 
  - Application phải chạy được trên Linux và Windows
  - Dependencies phải được quản lý qua requirements.txt
- **Constraints**: 
  - Python 3.10+ required
  - PostgreSQL required
- **Verification**: 
  - Test trên Linux và Windows
  - Target: Cross-platform compatibility

---

## 9. Compatibility Requirements

### 9.1 Browser Compatibility

#### NFR-COMP-001: Web Browser Support
- **Scenario**: User truy cập website từ các browsers khác nhau
- **Requirement**: 
  - Support các browsers: Chrome (latest 2 versions), Firefox (latest 2 versions), Safari (latest 2 versions), Edge (latest 2 versions)
  - Website phải hoạt động trên mobile browsers (Chrome Mobile, Safari Mobile)
- **Constraints**: 
  - Không support IE11 và các browsers cũ
- **Verification**: 
  - Test trên các browsers khác nhau
  - Target: Support modern browsers

### 9.2 API Compatibility

#### NFR-COMP-002: API Versioning
- **Scenario**: API được update với breaking changes
- **Requirement**: 
  - API phải có versioning strategy (nếu cần trong tương lai)
  - Backward compatibility được maintain trong cùng version
- **Constraints**: 
  - Versioning không bắt buộc cho MVP
- **Verification**: 
  - API versioning strategy (nếu có)
  - Target: Versioning strategy defined

---

## 10. Measurement & Verification

### 10.1 Performance Metrics
- API response time: Monitor qua APM tools hoặc logging
- Search performance: Monitor query execution time
- WebSocket latency: Monitor message delivery time

### 10.2 Security Metrics
- Password hash verification: Check database
- JWT token validation: Test với invalid tokens
- Input validation: Test với malicious inputs

### 10.3 Reliability Metrics
- Uptime: Monitor qua uptime monitoring tools
- Error rate: Monitor error logs
- Data consistency: Test transactions

### 10.4 Maintainability Metrics
- Code coverage: Run coverage.py
- Linting errors: Run flake8/pylint
- Documentation coverage: Review docs

---

**End of Document**

# Project Plan
## OldGoods Marketplace

**Version**: 1.0  
**Date**: 2024  
**Project Manager**: Development Team  
**Duration**: 8-10 weeks (4 Sprints)

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Project Overview](#2-project-overview)
3. [Work Breakdown Structure (WBS)](#3-work-breakdown-structure-wbs)
4. [Timeline & Sprints](#4-timeline--sprints)
5. [Resource Allocation](#5-resource-allocation)
6. [Risk Management](#6-risk-management)
7. [Dependencies](#7-dependencies)
8. [Milestones](#8-milestones)
9. [Quality Assurance](#9-quality-assurance)

---

## 1. Introduction

### 1.1 Purpose
Tài liệu này mô tả kế hoạch dự án chi tiết cho hệ thống OldGoods Marketplace, bao gồm timeline, resources, risks, và milestones.

### 1.2 Project Scope
Xây dựng hệ thống marketplace đồ cũ hoàn chỉnh với:
- Authentication & User Management
- Product Listings CRUD
- Search & Filter
- Real-time Chat (WebSocket)
- Offers & Deals
- Moderation & Reporting

### 1.3 Success Criteria
- Tất cả 9 use cases chính hoạt động end-to-end
- Test coverage > 60%
- API response time < 500ms
- Documentation đầy đủ
- Deployment guide hoàn chỉnh

---

## 2. Project Overview

### 2.1 Project Information
- **Project Name**: OldGoods Marketplace
- **Technology Stack**: FastAPI, SQLAlchemy, Alembic, PostgreSQL, (Redis optional), WebSocket
- **Team Size**: 3-5 members
- **Project Duration**: 8-10 weeks
- **Development Methodology**: Agile/Scrum (4 Sprints)

### 2.2 Team Roles
- **Backend Developer(s)**: Django development, API, WebSocket
- **Database Developer**: Database design, migrations, optimization
- **DevOps/Deployment**: Server setup, deployment, CI/CD
- **QA/Tester**: Testing, test cases, bug tracking
- **Project Manager**: Coordination, planning, documentation

---

## 3. Work Breakdown Structure (WBS)

### 3.1 Level 1: Project Phases

```
OldGoods Marketplace Project
├── Phase 1: Planning & Design (Week 1)
├── Phase 2: Sprint 1 - Foundation (Week 2-3)
├── Phase 3: Sprint 2 - Search & Media (Week 4-5)
├── Phase 4: Sprint 3 - Real-time Chat (Week 6-8)
├── Phase 5: Sprint 4 - Deals & Moderation (Week 9-10)
└── Phase 6: Testing & Deployment (Week 10)
```

### 3.2 Level 2: Major Deliverables

#### Phase 1: Planning & Design
- Vision & Scope Document
- SRS Document
- NFR Document
- SAD Document (4+1 Views)
- UML Diagrams
- Database Design
- API Specification
- Project Plan

#### Phase 2: Sprint 1 - Foundation
- FastAPI Project Setup
- Database Models (User, Profile, Category, Listing)
- Authentication API (Register, Login, Logout)
- Listing CRUD API
- Basic Tests

#### Phase 3: Sprint 2 - Search & Media
- Search & Filter Functionality
- Image Upload & Storage
- Favorite Functionality
- API Improvements
- Integration Tests

#### Phase 4: Sprint 3 - Real-time Chat
- FastAPI WebSocket Setup
- WebSocket Implementation
- Chat Models & WebSocket handlers
- Message History
- WebSocket Tests

#### Phase 5: Sprint 4 - Deals & Moderation
- Offers & Deals Functionality
- Meetup Scheduling
- Reports & Blocks
- Admin Moderation Panel
- E2E Tests

#### Phase 6: Testing & Deployment
- Comprehensive Testing
- Bug Fixes
- Performance Optimization
- Deployment Setup
- Documentation Finalization

---

## 4. Timeline & Sprints

### 4.1 Sprint 1: Foundation (2-3 weeks)

#### Week 1: Setup & Core Models
**Days 1-2**: Project Setup
- [ ] Initialize FastAPI project
- [ ] Setup PostgreSQL database
- [ ] Configure app settings (Pydantic Settings)
- [ ] Setup Git repository
- [ ] Create project structure

**Days 3-5**: Database Design & Models
- [ ] Create User và Profile models
- [ ] Create Category model
- [ ] Create Listing và ListingImage models
- [ ] Create Alembic migrations
- [ ] Test models và relationships

**Days 6-7**: Authentication
- [ ] Implement Register API
- [ ] Implement Login API (JWT - python-jose)
- [ ] Implement Logout API
- [ ] Write unit tests
- [ ] Write integration tests

#### Week 2: Listing CRUD
**Days 8-10**: Listing API
- [ ] Implement Create Listing API
- [ ] Implement Get Listing Detail API
- [ ] Implement Update Listing API
- [ ] Implement Delete Listing API
- [ ] Implement List Listings API (basic)
- [ ] Write tests

**Days 11-12**: Category API
- [ ] Implement List Categories API
- [ ] Implement Get Category Detail API
- [ ] Seed categories data
- [ ] Write tests

**Day 13**: Sprint 1 Review & Retrospective
- [ ] Code review
- [ ] Demo
- [ ] Retrospective
- [ ] Plan Sprint 2

**Deliverables**:
- ✅ FastAPI project setup
- ✅ Database models và migrations
- ✅ Authentication API
- ✅ Listing CRUD API
- ✅ Basic test suite (50% coverage target)

---

### 4.2 Sprint 2: Search & Media (2 weeks)

#### Week 3: Search & Filter
**Days 14-16**: Search Implementation
- [ ] Implement search by keyword
- [ ] Implement filter by category
- [ ] Implement filter by price range
- [ ] Implement filter by location
- [ ] Implement filter by condition
- [ ] Implement sorting (date, price)
- [ ] Add database indexes
- [ ] Write tests

**Days 17-18**: Image Upload
- [ ] Setup file storage (local/S3)
- [ ] Implement image upload
- [ ] Implement image validation
- [ ] Implement image deletion
- [ ] Write tests

#### Week 4: Favorites & Polish
**Days 19-20**: Favorite Functionality
- [ ] Create Favorite model
- [ ] Implement Add Favorite API
- [ ] Implement Remove Favorite API
- [ ] Implement List Favorites API
- [ ] Write tests

**Days 21**: API Improvements
- [ ] Improve error handling
- [ ] Add pagination
- [ ] Add response formatting
- [ ] Update API documentation

**Day 22**: Sprint 2 Review & Retrospective
- [ ] Code review
- [ ] Demo
- [ ] Retrospective
- [ ] Plan Sprint 3

**Deliverables**:
- ✅ Search & Filter functionality
- ✅ Image upload & storage
- ✅ Favorite functionality
- ✅ Improved API với pagination
- ✅ Test coverage 60%+

---

### 4.3 Sprint 3: Real-time Chat (2-3 weeks)

#### Week 5: FastAPI WebSocket Setup
**Days 23-25**: WebSocket Configuration
- [ ] Implement FastAPI WebSocket endpoint (`/ws/chat`)
- [ ] WebSocket authentication (JWT)
- [ ] Broadcast strategy (Redis pubsub optional)
- [ ] Test WebSocket connection

**Days 26-27**: Chat Models
- [ ] Create Conversation model
- [ ] Create ConversationMember model
- [ ] Create Message model
 - [ ] Create database migrations (Alembic)
- [ ] Write model tests

#### Week 6: WebSocket Implementation
**Days 28-30**: Message Functionality
- [ ] Implement send message
- [ ] Implement receive message
- [ ] Implement message persistence
- [ ] Implement join conversation
- [ ] Write WebSocket tests

**Days 31-32**: Chat API
- [ ] Implement List Conversations API
- [ ] Implement Get Messages API
- [ ] Implement Create Conversation API
- [ ] Write integration tests

#### Week 7: Chat Features & Testing
**Days 33-34**: Additional Features
- [ ] Implement typing indicator (optional)
- [ ] Implement read receipt (optional)
- [ ] Implement message notifications
- [ ] Write E2E tests cho chat workflow

**Day 35**: Sprint 3 Review & Retrospective
- [ ] Code review
- [ ] Demo
- [ ] Retrospective
- [ ] Plan Sprint 4

**Deliverables**:
- ✅ FastAPI WebSocket setup
- ✅ WebSocket chat implementation
- ✅ Chat models và API
- ✅ Message history
- ✅ Test coverage 65%+

---

### 4.4 Sprint 4: Deals & Moderation (2 weeks)

#### Week 8: Offers & Deals
**Days 36-38**: Offer Functionality
- [ ] Create Offer model
- [ ] Implement Create Offer API
- [ ] Implement List Offers API
- [ ] Implement Accept Offer API
- [ ] Implement Reject Offer API
- [ ] Write tests

**Days 39-40**: Deal Functionality
- [ ] Create Deal model
- [ ] Create Meetup model
- [ ] Implement Create Deal (when offer accepted)
- [ ] Implement Create Meetup API
- [ ] Implement Update Deal Status API
- [ ] Write tests

#### Week 9: Moderation
**Days 41-43**: Reports & Blocks
- [ ] Create Report model
- [ ] Create Block model
- [ ] Implement Create Report API
- [ ] Implement Block User API
- [ ] Write tests

**Days 44-45**: Admin Panel
- [ ] Implement List Reports API (admin)
- [ ] Implement Resolve Report API
- [ ] Implement Ban User API
- [ ] Implement Admin permissions
- [ ] Write tests

#### Week 10: Testing & Deployment
**Days 46-47**: Comprehensive Testing
- [ ] Run full test suite
- [ ] Fix bugs
- [ ] E2E tests cho complete workflows
- [ ] Performance testing
- [ ] Security testing

**Days 48-49**: Deployment & Documentation
- [ ] Setup production server
- [ ] Deploy application
- [ ] Finalize documentation
- [ ] Create deployment guide
- [ ] Prepare demo

**Day 50**: Final Review & Presentation
- [ ] Final code review
- [ ] Demo preparation
- [ ] Project presentation
- [ ] Retrospective

**Deliverables**:
- ✅ Offers & Deals functionality
- ✅ Reports & Blocks
- ✅ Admin moderation panel
- ✅ Complete test suite (70%+ coverage)
- ✅ Deployed application
- ✅ Complete documentation

---

## 5. Resource Allocation

### 5.1 Team Allocation

| Role | Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4 |
|------|---------|----------|----------|----------|
| Backend Developer 1 | 100% | 100% | 100% | 100% |
| Backend Developer 2 | 100% | 100% | 100% | 100% |
| Database Developer | 50% | 25% | 25% | 25% |
| QA/Tester | 25% | 50% | 50% | 100% |
| DevOps | 25% | 25% | 25% | 100% |

### 5.2 Infrastructure Resources

#### Development
- Development servers (local hoặc cloud)
- PostgreSQL database
- Redis (for Channels)
- Git repository

#### Production (Optional)
- Production server
- Domain name
- SSL certificate
- Monitoring tools

---

## 6. Risk Management

### 6.1 Technical Risks

#### Risk 1: WebSocket Implementation Complexity
- **Probability**: Medium
- **Impact**: High
-- **Mitigation**: 
  - Research FastAPI WebSocket patterns early
  - Start with simple WebSocket implementation
  - Allocate extra time in Sprint 3
- **Contingency**: Use polling as fallback (less ideal)

#### Risk 2: Database Performance Issues
- **Probability**: Medium
- **Impact**: Medium
- **Mitigation**:
  - Design indexes early
  - Test với large datasets
  - Optimize queries
- **Contingency**: Add caching layer (Redis)

#### Risk 3: Team Members Not Familiar với FastAPI WebSocket
- **Probability**: High
- **Impact**: Medium
-- **Mitigation**:
  - Training session before Sprint 3 (async/WebSocket)
  - Pair programming
  - Code reviews
- **Contingency**: Allocate more time, seek external help

### 6.2 Project Risks

#### Risk 4: Timeline Overrun
- **Probability**: Medium
- **Impact**: High
- **Mitigation**:
  - Regular sprint reviews
  - Prioritize MVP features
  - Remove nice-to-have features if needed
- **Contingency**: Extend timeline hoặc reduce scope

#### Risk 5: Insufficient Testing
- **Probability**: Medium
- **Impact**: High
- **Mitigation**:
  - Write tests cùng với code
  - Set coverage targets
  - Regular test reviews
- **Contingency**: Dedicate Sprint 4 time cho testing

### 6.3 Risk Register

| Risk ID | Description | Probability | Impact | Mitigation | Owner |
|---------|------------|-------------|--------|------------|-------|
| R1 | WebSocket complexity | Medium | High | Early research, extra time | Backend Team |
| R2 | DB performance | Medium | Medium | Indexes, optimization | DB Developer |
| R3 | Team learning curve | High | Medium | Training, pair programming | PM |
| R4 | Timeline overrun | Medium | High | Regular reviews, prioritize | PM |
| R5 | Insufficient testing | Medium | High | Test cùng code, coverage | QA |

---

## 7. Dependencies

### 7.1 Internal Dependencies

#### Sprint 1 → Sprint 2
- Authentication phải hoàn thành trước khi test các features khác
- Listing CRUD phải hoàn thành trước Search

#### Sprint 2 → Sprint 3
- Search phải hoàn thành trước Chat (chat có thể link với listings)
- Image upload phải hoàn thành (có thể cần cho chat)

#### Sprint 3 → Sprint 4
- Chat phải hoàn thành trước Deals (users chat trước khi deal)
- Conversation model có thể được sử dụng trong Deals

### 7.2 External Dependencies

- **PostgreSQL**: Phải được setup trước Sprint 1
- **Redis**: Phải được setup trước Sprint 3
- **FastAPI WebSocket**: Phải được research trước Sprint 3
- **Deployment Server**: Phải được setup trước Sprint 4

---

## 8. Milestones

### Milestone 1: Project Kickoff (End of Week 1)
- ✅ All documentation completed
- ✅ Project plan approved
- ✅ Team aligned on goals

### Milestone 2: Foundation Complete (End of Sprint 1)
- ✅ Authentication working
- ✅ Listing CRUD working
- ✅ Basic tests passing

### Milestone 3: Core Features Complete (End of Sprint 2)
- ✅ Search & Filter working
- ✅ Image upload working
- ✅ Favorites working

### Milestone 4: Realtime Features Complete (End of Sprint 3)
- ✅ WebSocket chat working
- ✅ Message history working
- ✅ Chat API complete

### Milestone 5: MVP Complete (End of Sprint 4)
- ✅ All features working
- ✅ Tests passing (70%+ coverage)
- ✅ Application deployed
- ✅ Documentation complete

---

## 9. Quality Assurance

### 9.1 Code Quality

#### Standards
- PEP 8 compliance
- Code reviews cho tất cả PRs
- Documentation (docstrings) cho public APIs

#### Tools
- Black (code formatting)
- Flake8 (linting)
- Pylint (optional)

### 9.2 Testing

#### Coverage Targets
- Sprint 1: 50%
- Sprint 2: 60%
- Sprint 3: 65%
- Sprint 4: 70%+

#### Test Types
- Unit tests (60% of tests)
- Integration tests (30% of tests)
- E2E tests (10% of tests)

### 9.3 Documentation

#### Required Documents
- Vision & Scope ✅
- SRS ✅
- NFR ✅
- SAD ✅
- UML Diagrams ✅
- DB Design ✅
- API Spec ✅
- Test Plan ✅
- Deployment Guide ✅
- Project Plan ✅

---

## 10. Communication Plan

### 10.1 Regular Meetings

#### Daily Standup (15 minutes)
- What did you do yesterday?
- What will you do today?
- Any blockers?

#### Sprint Planning (2 hours)
- Review backlog
- Plan sprint tasks
- Estimate effort

#### Sprint Review (1 hour)
- Demo completed work
- Gather feedback

#### Sprint Retrospective (1 hour)
- What went well?
- What could be improved?
- Action items

### 10.2 Communication Channels

- **Slack/Teams**: Daily communication
- **GitHub/GitLab**: Code reviews, issues
- **Documentation**: Shared drive hoặc wiki

---

## 11. Change Management

### 11.1 Change Request Process

1. **Request**: Submit change request với rationale
2. **Review**: Team reviews impact
3. **Decision**: Approve/reject
4. **Update Plan**: Update project plan nếu approved
5. **Communicate**: Notify team

### 11.2 Scope Changes

- **Minor changes**: Can be accommodated trong current sprint
- **Major changes**: Require sprint replanning
- **Critical changes**: May require timeline extension

---

## 12. Success Metrics

### 12.1 Technical Metrics

- **Test Coverage**: > 70%
- **API Response Time**: < 500ms (95th percentile)
- **Search Performance**: < 1s với 5000 listings
- **WebSocket Latency**: < 100ms
- **Bug Count**: < 10 critical bugs

### 12.2 Project Metrics

- **On-time Delivery**: All sprints completed on time
- **Scope Completion**: 100% MVP features
- **Documentation**: 100% required documents
- **Team Satisfaction**: > 80% (survey)

---

## 13. References

- Django Project Structure: https://docs.djangoproject.com/
- Agile/Scrum Guide: https://www.scrum.org/
- Project Management Best Practices

---

**End of Document**

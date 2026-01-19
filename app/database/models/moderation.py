"""
Moderation models - Report, Block.
Moderation Aggregate trong Domain-Driven Design.
"""
from sqlalchemy import Column, String, Text, Enum as SQLEnum, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.database.base import BaseModel


class ReportType(str, enum.Enum):
    """Report type enumeration."""
    SPAM = 'SPAM'
    INAPPROPRIATE = 'INAPPROPRIATE'
    SCAM = 'SCAM'
    OTHER = 'OTHER'


class ReportStatus(str, enum.Enum):
    """Report status enumeration."""
    PENDING = 'PENDING'
    RESOLVED = 'RESOLVED'
    DISMISSED = 'DISMISSED'


class Report(BaseModel):
    """
    Report model - Entity trong Moderation Aggregate.
    """
    __tablename__ = 'reports'
    
    reporter_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    reported_listing_id = Column(UUID(as_uuid=True), ForeignKey('listings.id', ondelete='CASCADE'), nullable=True, index=True)
    reported_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=True, index=True)
    report_type = Column(SQLEnum(ReportType), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(ReportStatus), nullable=False, default=ReportStatus.PENDING, index=True)
    resolved_by_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    reporter = relationship('User', foreign_keys=[reporter_id], back_populates='reports_made')
    reported_listing = relationship('Listing', back_populates='reports')
    reported_user = relationship('User', foreign_keys=[reported_user_id], back_populates='reports_against')
    resolved_by = relationship('User', foreign_keys=[resolved_by_id])
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            '(reported_listing_id IS NOT NULL) OR (reported_user_id IS NOT NULL)',
            name='check_report_target'
        ),
        # Composite index sẽ được tạo trong migration
    )
    
    def __repr__(self):
        return f"<Report(id={self.id}, report_type={self.report_type.value}, status={self.status.value})>"


class Block(BaseModel):
    """
    Block model - Association entity giữa User và User (self-referential).
    """
    __tablename__ = 'blocks'
    
    blocker_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    blocked_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Relationships
    blocker = relationship('User', foreign_keys=[blocker_id], back_populates='blocks_made')
    blocked_user = relationship('User', foreign_keys=[blocked_user_id], back_populates='blocked_by')
    
    # Unique constraint
    __table_args__ = (
        # Unique constraint sẽ được tạo trong migration
    )
    
    def __repr__(self):
        return f"<Block(blocker_id={self.blocker_id}, blocked_user_id={self.blocked_user_id})>"

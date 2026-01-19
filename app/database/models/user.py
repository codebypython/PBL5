"""
User and Profile models.
User Aggregate trong Domain-Driven Design.
"""
from sqlalchemy import Column, String, Boolean, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.database.base import BaseModel


class UserRole(str, enum.Enum):
    """User role enumeration."""
    USER = 'USER'
    ADMIN = 'ADMIN'


class UserStatus(str, enum.Enum):
    """User status enumeration."""
    ACTIVE = 'ACTIVE'
    BANNED = 'BANNED'


class User(BaseModel):
    """
    User model - Root entity của User Aggregate.
    """
    __tablename__ = 'users'
    
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)  # Will store hashed password
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.USER, index=True)
    status = Column(SQLEnum(UserStatus), nullable=False, default=UserStatus.ACTIVE, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    profile = relationship('Profile', back_populates='user', uselist=False, cascade='all, delete-orphan')
    listings = relationship('Listing', back_populates='seller', cascade='all, delete-orphan')
    favorites = relationship('Favorite', back_populates='user', cascade='all, delete-orphan')
    offers = relationship('Offer', back_populates='buyer', cascade='all, delete-orphan')
    deals_as_buyer = relationship('Deal', foreign_keys='Deal.buyer_id', back_populates='buyer')
    deals_as_seller = relationship('Deal', foreign_keys='Deal.seller_id', back_populates='seller')
    conversation_memberships = relationship('ConversationMember', back_populates='user', cascade='all, delete-orphan')
    sent_messages = relationship('Message', back_populates='sender', cascade='all, delete-orphan')
    reports_made = relationship('Report', foreign_keys='Report.reporter_id', back_populates='reporter', cascade='all, delete-orphan')
    reports_against = relationship('Report', foreign_keys='Report.reported_user_id', back_populates='reported_user', cascade='all, delete-orphan')
    blocks_made = relationship('Block', foreign_keys='Block.blocker_id', back_populates='blocker', cascade='all, delete-orphan')
    blocked_by = relationship('Block', foreign_keys='Block.blocked_user_id', back_populates='blocked_user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<User(email={self.email}, role={self.role.value}, status={self.status.value})>"
    
    def is_banned(self) -> bool:
        """Check if user is banned."""
        return self.status == UserStatus.BANNED


class Profile(BaseModel):
    """
    Profile model - Value object/Entity trong User Aggregate.
    """
    __tablename__ = 'profiles'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    location = Column(String(255), nullable=True)
    avatar = Column(String(500), nullable=True)  # Store file path
    bio = Column(String(1000), nullable=True)
    
    # Relationships
    user = relationship('User', back_populates='profile')
    
    def __repr__(self):
        return f"<Profile(user_id={self.user_id}, full_name={self.full_name})>"

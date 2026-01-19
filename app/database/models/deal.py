"""
Deal models - Offer, Deal, Meetup.
Deal Aggregate trong Domain-Driven Design.
"""
from sqlalchemy import Column, String, Text, Numeric, Enum as SQLEnum, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.database.base import BaseModel


class OfferStatus(str, enum.Enum):
    """Offer status enumeration."""
    PENDING = 'PENDING'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    CANCELLED = 'CANCELLED'


class DealStatus(str, enum.Enum):
    """Deal status enumeration."""
    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'


class Offer(BaseModel):
    """
    Offer model - Entity trong Deal Aggregate.
    """
    __tablename__ = 'offers'
    
    listing_id = Column(UUID(as_uuid=True), ForeignKey('listings.id', ondelete='CASCADE'), nullable=False, index=True)
    buyer_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    price = Column(Numeric(12, 2), nullable=False)
    message = Column(Text, nullable=True)
    status = Column(SQLEnum(OfferStatus), nullable=False, default=OfferStatus.PENDING, index=True)
    
    # Relationships
    listing = relationship('Listing', back_populates='offers')
    buyer = relationship('User', back_populates='offers')
    deal = relationship('Deal', back_populates='offer', uselist=False, cascade='all, delete-orphan')
    
    # Constraints
    __table_args__ = (
        CheckConstraint('price > 0', name='check_offer_price_positive'),
    )
    
    def __repr__(self):
        return f"<Offer(id={self.id}, listing_id={self.listing_id}, price={self.price}, status={self.status.value})>"


class Deal(BaseModel):
    """
    Deal model - Root entity của Deal Aggregate.
    """
    __tablename__ = 'deals'
    
    listing_id = Column(UUID(as_uuid=True), ForeignKey('listings.id', ondelete='CASCADE'), nullable=False, index=True)
    buyer_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    seller_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    offer_id = Column(UUID(as_uuid=True), ForeignKey('offers.id', ondelete='RESTRICT'), unique=True, nullable=False, index=True)
    status = Column(SQLEnum(DealStatus), nullable=False, default=DealStatus.PENDING, index=True)
    
    # Relationships
    listing = relationship('Listing', back_populates='deal')
    buyer = relationship('User', foreign_keys=[buyer_id], back_populates='deals_as_buyer')
    seller = relationship('User', foreign_keys=[seller_id], back_populates='deals_as_seller')
    offer = relationship('Offer', back_populates='deal')
    meetups = relationship('Meetup', back_populates='deal', cascade='all, delete-orphan', order_by='Meetup.scheduled_at')
    
    def __repr__(self):
        return f"<Deal(id={self.id}, listing_id={self.listing_id}, status={self.status.value})>"


class Meetup(BaseModel):
    """
    Meetup model - Entity trong Deal Aggregate.
    """
    __tablename__ = 'meetups'
    
    deal_id = Column(UUID(as_uuid=True), ForeignKey('deals.id', ondelete='CASCADE'), nullable=False, index=True)
    scheduled_at = Column(DateTime(timezone=True), nullable=False, index=True)
    location = Column(String(255), nullable=False)
    notes = Column(Text, nullable=True)
    
    # Relationships
    deal = relationship('Deal', back_populates='meetups')
    
    def __repr__(self):
        return f"<Meetup(id={self.id}, deal_id={self.deal_id}, scheduled_at={self.scheduled_at})>"

"""
Listing models - Category, Listing, ListingImage, Favorite.
Listing Aggregate trong Domain-Driven Design.
"""
from sqlalchemy import Column, String, Text, Numeric, Enum as SQLEnum, ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.database.base import BaseModel


class ListingCondition(str, enum.Enum):
    """Listing condition enumeration."""
    NEW = 'NEW'
    LIKE_NEW = 'LIKE_NEW'
    USED = 'USED'
    POOR = 'POOR'


class ListingStatus(str, enum.Enum):
    """Listing status enumeration."""
    AVAILABLE = 'AVAILABLE'
    RESERVED = 'RESERVED'
    SOLD = 'SOLD'
    EXPIRED = 'EXPIRED'


class Category(BaseModel):
    """
    Category model for product categorization.
    """
    __tablename__ = 'categories'
    
    name = Column(String(100), unique=True, nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey('categories.id', ondelete='SET NULL'), nullable=True, index=True)
    
    # Relationships
    parent = relationship('Category', remote_side='Category.id', backref='children')
    listings = relationship('Listing', back_populates='category', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Category(name={self.name}, slug={self.slug})>"


class Listing(BaseModel):
    """
    Listing model - Root entity của Listing Aggregate.
    """
    __tablename__ = 'listings'
    
    seller_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id', ondelete='RESTRICT'), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Numeric(12, 2), nullable=False, index=True)
    condition = Column(SQLEnum(ListingCondition), nullable=False)
    location = Column(String(255), nullable=False)
    status = Column(SQLEnum(ListingStatus), nullable=False, default=ListingStatus.AVAILABLE, index=True)
    
    # Relationships
    seller = relationship('User', back_populates='listings')
    category = relationship('Category', back_populates='listings')
    images = relationship('ListingImage', back_populates='listing', cascade='all, delete-orphan', order_by='ListingImage.order')
    favorites = relationship('Favorite', back_populates='listing', cascade='all, delete-orphan')
    offers = relationship('Offer', back_populates='listing', cascade='all, delete-orphan')
    conversations = relationship('Conversation', back_populates='listing', cascade='all, delete-orphan')
    reports = relationship('Report', back_populates='reported_listing', cascade='all, delete-orphan')
    deal = relationship('Deal', back_populates='listing', uselist=False, cascade='all, delete-orphan')
    
    # Indexes
    __table_args__ = (
        CheckConstraint('price > 0', name='check_price_positive'),
        # Composite indexes sẽ được tạo trong migration
    )
    
    def __repr__(self):
        return f"<Listing(title={self.title}, price={self.price}, status={self.status.value})>"
    
    def can_edit(self) -> bool:
        """Check if listing can be edited."""
        return self.status in [ListingStatus.AVAILABLE, ListingStatus.RESERVED]


class ListingImage(BaseModel):
    """
    ListingImage model - Entity trong Listing Aggregate.
    """
    __tablename__ = 'listing_images'
    
    listing_id = Column(UUID(as_uuid=True), ForeignKey('listings.id', ondelete='CASCADE'), nullable=False, index=True)
    image = Column(String(500), nullable=False)  # Store file path
    order = Column(Integer, nullable=False, default=0)
    
    # Relationships
    listing = relationship('Listing', back_populates='images')
    
    # Constraints
    __table_args__ = (
        CheckConstraint('order >= 0 AND order <= 4', name='check_order_range'),
    )
    
    def __repr__(self):
        return f"<ListingImage(listing_id={self.listing_id}, order={self.order})>"


class Favorite(BaseModel):
    """
    Favorite model - Association entity giữa User và Listing.
    """
    __tablename__ = 'favorites'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    listing_id = Column(UUID(as_uuid=True), ForeignKey('listings.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Relationships
    user = relationship('User', back_populates='favorites')
    listing = relationship('Listing', back_populates='favorites')
    
    # Unique constraint
    __table_args__ = (
        # Unique constraint sẽ được tạo trong migration
    )
    
    def __repr__(self):
        return f"<Favorite(user_id={self.user_id}, listing_id={self.listing_id})>"

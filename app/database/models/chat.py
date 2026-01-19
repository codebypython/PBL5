"""
Chat models - Conversation, ConversationMember, Message.
Conversation Aggregate trong Domain-Driven Design.
"""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import BaseModel


class Conversation(BaseModel):
    """
    Conversation model - Root entity của Conversation Aggregate.
    """
    __tablename__ = 'conversations'
    
    listing_id = Column(UUID(as_uuid=True), ForeignKey('listings.id', ondelete='SET NULL'), nullable=True, index=True)
    
    # Relationships
    listing = relationship('Listing', back_populates='conversations')
    members = relationship('ConversationMember', back_populates='conversation', cascade='all, delete-orphan')
    messages = relationship('Message', back_populates='conversation', cascade='all, delete-orphan', order_by='Message.sent_at')
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, listing_id={self.listing_id})>"


class ConversationMember(BaseModel):
    """
    ConversationMember model - Association entity giữa User và Conversation.
    """
    __tablename__ = 'conversation_members'
    
    conversation_id = Column(UUID(as_uuid=True), ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    joined_at = Column(DateTime(timezone=True), nullable=False, server_default='now()')
    
    # Relationships
    conversation = relationship('Conversation', back_populates='members')
    user = relationship('User', back_populates='conversation_memberships')
    
    # Unique constraint
    __table_args__ = (
        # Unique constraint sẽ được tạo trong migration
    )
    
    def __repr__(self):
        return f"<ConversationMember(conversation_id={self.conversation_id}, user_id={self.user_id})>"


class Message(BaseModel):
    """
    Message model - Entity trong Conversation Aggregate.
    """
    __tablename__ = 'messages'
    
    conversation_id = Column(UUID(as_uuid=True), ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False, index=True)
    sender_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    content = Column(Text, nullable=False)
    read_at = Column(DateTime(timezone=True), nullable=True, index=True)
    sent_at = Column(DateTime(timezone=True), nullable=False, server_default='now()')
    
    # Relationships
    conversation = relationship('Conversation', back_populates='messages')
    sender = relationship('User', back_populates='sent_messages')
    
    # Indexes
    __table_args__ = (
        # Composite index sẽ được tạo trong migration
    )
    
    def __repr__(self):
        return f"<Message(id={self.id}, conversation_id={self.conversation_id}, sender_id={self.sender_id})>"

"""
Models for chat app.
"""
import uuid
from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """Conversation model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey('listings.Listing', on_delete=models.SET_NULL, null=True, blank=True, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'conversations'
        indexes = [
            models.Index(fields=['updated_at']),
        ]
    
    def __str__(self):
        return f"Conversation {self.id}"


class ConversationMember(models.Model):
    """Conversation member model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversation_memberships')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'conversation_members'
        unique_together = ['conversation', 'user']
        indexes = [
            models.Index(fields=['conversation']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.conversation.id}"


class Message(models.Model):
    """Message model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    read_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'messages'
        ordering = ['sent_at']
        indexes = [
            models.Index(fields=['conversation', '-sent_at']),
            models.Index(fields=['sender']),
            models.Index(fields=['read_at']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender.email}"

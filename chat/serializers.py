"""
Serializers for chat app.
"""
from rest_framework import serializers
from .models import Conversation, Message
from accounts.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ('id', 'conversation', 'sender', 'content', 'read_at', 'sent_at')
        read_only_fields = ('id', 'sender', 'sent_at')


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model."""
    members = UserSerializer(many=True, read_only=True, source='members.user')
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ('id', 'listing', 'members', 'last_message', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_last_message(self, obj):
        """Get last message in conversation."""
        last_message = obj.messages.last()
        if last_message:
            return MessageSerializer(last_message).data
        return None

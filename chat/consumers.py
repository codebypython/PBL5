"""
WebSocket consumers for chat app.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Conversation, ConversationMember, Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for chat."""
    
    async def connect(self):
        """Handle WebSocket connection."""
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        else:
            self.conversation_id = None
            await self.accept()
            await self.send(text_data=json.dumps({
                'type': 'connection_established',
                'user_id': str(self.user.id),
            }))
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        if hasattr(self, 'conversation_id') and self.conversation_id:
            await self.channel_layer.group_discard(
                self.conversation_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """Handle received message."""
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'join_conversation':
            await self.join_conversation(data.get('conversation_id'))
        elif message_type == 'send_message':
            await self.send_message(data.get('conversation_id'), data.get('content'))
        elif message_type == 'mark_read':
            await self.mark_read(data.get('conversation_id'), data.get('message_id'))
    
    async def join_conversation(self, conversation_id):
        """Join a conversation."""
        conversation = await self.get_conversation(conversation_id)
        if conversation and await self.is_member(conversation_id):
            self.conversation_id = conversation_id
            self.conversation_group_name = f'conversation_{conversation_id}'
            await self.channel_layer.group_add(
                self.conversation_group_name,
                self.channel_name
            )
            await self.send(text_data=json.dumps({
                'type': 'conversation_joined',
                'conversation_id': str(conversation_id),
            }))
    
    async def send_message(self, conversation_id, content):
        """Send a message."""
        if not conversation_id or not content:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'error': 'Invalid message data',
            }))
            return
        
        conversation = await self.get_conversation(conversation_id)
        if not conversation or not await self.is_member(conversation_id):
            await self.send(text_data=json.dumps({
                'type': 'error',
                'error': 'Invalid conversation',
            }))
            return
        
        message = await self.create_message(conversation_id, content)
        
        # Send to sender
        await self.send(text_data=json.dumps({
            'type': 'message_sent',
            'message': {
                'id': str(message.id),
                'conversation_id': str(conversation_id),
                'sender': {
                    'id': str(self.user.id),
                    'email': self.user.email,
                },
                'content': content,
                'sent_at': message.sent_at.isoformat(),
            },
        }))
        
        # Broadcast to conversation group
        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type': 'message_received',
                'message': {
                    'id': str(message.id),
                    'conversation_id': str(conversation_id),
                    'sender': {
                        'id': str(self.user.id),
                        'email': self.user.email,
                    },
                    'content': content,
                    'sent_at': message.sent_at.isoformat(),
                },
            }
        )
    
    async def message_received(self, event):
        """Receive message from group."""
        await self.send(text_data=json.dumps(event))
    
    async def mark_read(self, conversation_id, message_id):
        """Mark message as read."""
        await self.update_read_status(message_id)
        await self.send(text_data=json.dumps({
            'type': 'read_receipt',
            'conversation_id': str(conversation_id),
            'message_id': str(message_id),
        }))
    
    @database_sync_to_async
    def get_conversation(self, conversation_id):
        """Get conversation from database."""
        try:
            return Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return None
    
    @database_sync_to_async
    def is_member(self, conversation_id):
        """Check if user is a member of conversation."""
        return ConversationMember.objects.filter(
            conversation_id=conversation_id,
            user=self.user
        ).exists()
    
    @database_sync_to_async
    def create_message(self, conversation_id, content):
        """Create message in database."""
        conversation = Conversation.objects.get(id=conversation_id)
        message = Message.objects.create(
            conversation=conversation,
            sender=self.user,
            content=content
        )
        conversation.save()  # Update updated_at
        return message
    
    @database_sync_to_async
    def update_read_status(self, message_id):
        """Update message read status."""
        from django.utils import timezone
        Message.objects.filter(id=message_id).update(read_at=timezone.now())

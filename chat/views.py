"""
Views for chat app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for Conversation model."""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        """Filter conversations for current user."""
        return Conversation.objects.filter(
            members__user=self.request.user
        ).distinct().order_by('-updated_at')
    
    @action(detail=True, methods=['get'])
    def messages(self, request, id=None):
        """Get messages for a conversation."""
        conversation = self.get_object()
        messages = Message.objects.filter(conversation=conversation).order_by('sent_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

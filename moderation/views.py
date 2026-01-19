"""
Views for moderation app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Report, Block
from .serializers import ReportSerializer, BlockSerializer


class ReportViewSet(viewsets.ModelViewSet):
    """ViewSet for Report model."""
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)


class BlockViewSet(viewsets.ModelViewSet):
    """ViewSet for Block model."""
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def perform_create(self, serializer):
        serializer.save(blocker=self.request.user)

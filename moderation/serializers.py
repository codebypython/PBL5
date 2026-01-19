"""
Serializers for moderation app.
"""
from rest_framework import serializers
from .models import Report, Block
from accounts.serializers import UserSerializer


class ReportSerializer(serializers.ModelSerializer):
    """Serializer for Report model."""
    reporter = UserSerializer(read_only=True)
    
    class Meta:
        model = Report
        fields = (
            'id', 'reporter', 'reported_listing', 'reported_user',
            'report_type', 'description', 'status', 'resolved_by',
            'resolved_at', 'created_at'
        )
        read_only_fields = ('id', 'reporter', 'status', 'resolved_by', 'resolved_at', 'created_at')


class BlockSerializer(serializers.ModelSerializer):
    """Serializer for Block model."""
    blocker = UserSerializer(read_only=True)
    blocked_user = UserSerializer(read_only=True)
    
    class Meta:
        model = Block
        fields = ('id', 'blocker', 'blocked_user', 'created_at')
        read_only_fields = ('id', 'blocker', 'created_at')

"""
Serializers for admin panel app.
"""
from rest_framework import serializers
from moderation.models import Report


class ReportListSerializer(serializers.ModelSerializer):
    """Serializer for listing reports."""
    
    class Meta:
        model = Report
        fields = (
            'id', 'reporter', 'reported_listing', 'reported_user',
            'report_type', 'description', 'status', 'resolved_by',
            'resolved_at', 'created_at'
        )


class ResolveReportSerializer(serializers.Serializer):
    """Serializer for resolving reports."""
    action = serializers.ChoiceField(choices=['DISMISS', 'WARN_USER', 'BAN_USER', 'REMOVE_LISTING'])
    reason = serializers.CharField(required=False, allow_blank=True)

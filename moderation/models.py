"""
Models for moderation app.
"""
import uuid
from django.db import models
from django.conf import settings


class Report(models.Model):
    """Report model."""
    
    class ReportType(models.TextChoices):
        SPAM = 'SPAM', 'Spam'
        INAPPROPRIATE = 'INAPPROPRIATE', 'Inappropriate Content'
        SCAM = 'SCAM', 'Scam'
        OTHER = 'OTHER', 'Other'
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        RESOLVED = 'RESOLVED', 'Resolved'
        DISMISSED = 'DISMISSED', 'Dismissed'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_made')
    reported_listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, null=True, blank=True, related_name='reports')
    reported_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='reports_against')
    report_type = models.CharField(max_length=50, choices=ReportType.choices)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_reports')
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reports'
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['reporter']),
            models.Index(fields=['reported_listing']),
            models.Index(fields=['reported_user']),
        ]
    
    def __str__(self):
        return f"Report {self.report_type} by {self.reporter.email}"


class Block(models.Model):
    """Block model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blocker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blocks_made')
    blocked_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blocked_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'blocks'
        unique_together = ['blocker', 'blocked_user']
        indexes = [
            models.Index(fields=['blocker']),
            models.Index(fields=['blocked_user']),
        ]
    
    def __str__(self):
        return f"{self.blocker.email} blocked {self.blocked_user.email}"

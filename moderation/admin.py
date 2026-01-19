"""
Admin configuration for moderation app.
"""
from django.contrib import admin
from .models import Report, Block


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'reporter', 'report_type', 'status', 'created_at')
    list_filter = ('status', 'report_type', 'created_at')
    search_fields = ('reporter__email', 'description')
    raw_id_fields = ('reporter', 'reported_listing', 'reported_user', 'resolved_by')


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'blocker', 'blocked_user', 'created_at')
    list_filter = ('created_at',)
    raw_id_fields = ('blocker', 'blocked_user')

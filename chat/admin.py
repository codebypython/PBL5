"""
Admin configuration for chat app.
"""
from django.contrib import admin
from .models import Conversation, ConversationMember, Message


class ConversationMemberInline(admin.TabularInline):
    model = ConversationMember
    extra = 1


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    inlines = [ConversationMemberInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'content', 'sent_at', 'read_at')
    list_filter = ('sent_at', 'read_at')
    search_fields = ('content',)
    raw_id_fields = ('conversation', 'sender')

"""
Admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model."""
    list_display = ('email', 'full_name', 'role', 'status', 'is_active', 'created_at')
    list_filter = ('role', 'status', 'is_active', 'created_at')
    search_fields = ('email',)
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('role', 'status', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role'),
        }),
    )
    
    def full_name(self, obj):
        """Get user's full name from profile."""
        return obj.profile.full_name if hasattr(obj, 'profile') else '-'
    full_name.short_description = 'Full Name'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin interface for Profile model."""
    list_display = ('full_name', 'user', 'phone', 'location', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'user__email', 'phone')
    raw_id_fields = ('user',)

"""
Custom permissions.
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permission to only allow owners to edit their objects."""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only to owner
        return obj.seller == request.user


class IsAdmin(permissions.BasePermission):
    """Permission to only allow admin users."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'ADMIN'

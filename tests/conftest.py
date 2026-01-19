"""
Pytest configuration and fixtures.
"""
import pytest
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()


@pytest.fixture
def user(db):
    """Create a test user."""
    user = User.objects.create_user(
        email='test@example.com',
        password='testpass123'
    )
    Profile.objects.create(user=user, full_name='Test User')
    return user


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    user = User.objects.create_user(
        email='admin@example.com',
        password='adminpass123',
        role=User.Role.ADMIN
    )
    Profile.objects.create(user=user, full_name='Admin User')
    return user

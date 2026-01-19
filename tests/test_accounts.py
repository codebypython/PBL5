"""
Tests for accounts app.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from accounts.models import Profile

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistration:
    """Test user registration."""
    
    def test_register_user_success(self):
        """Test successful user registration."""
        client = APIClient()
        data = {
            'email': 'newuser@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123',
            'full_name': 'New User'
        }
        response = client.post('/api/v1/auth/register/', data)
        assert response.status_code == 201
        assert User.objects.filter(email='newuser@example.com').exists()
        assert Profile.objects.filter(user__email='newuser@example.com').exists()
    
    def test_register_user_duplicate_email(self):
        """Test registration with duplicate email."""
        User.objects.create_user(email='existing@example.com', password='pass123')
        client = APIClient()
        data = {
            'email': 'existing@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123',
            'full_name': 'New User'
        }
        response = client.post('/api/v1/auth/register/', data)
        assert response.status_code == 400


@pytest.mark.django_db
class TestUserLogin:
    """Test user login."""
    
    def test_login_success(self, user):
        """Test successful login."""
        client = APIClient()
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = client.post('/api/v1/auth/login/', data)
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        client = APIClient()
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = client.post('/api/v1/auth/login/', data)
        assert response.status_code == 401

"""
Tests for listings app.
"""
import pytest
from rest_framework.test import APIClient
from listings.models import Category, Listing


@pytest.mark.django_db
class TestListings:
    """Test listings functionality."""
    
    def test_list_categories(self):
        """Test listing categories."""
        Category.objects.create(name='Electronics', slug='electronics')
        client = APIClient()
        response = client.get('/api/v1/categories/')
        assert response.status_code == 200
        assert len(response.data['results']) > 0
    
    def test_create_listing_authenticated(self, user):
        """Test creating listing when authenticated."""
        category = Category.objects.create(name='Electronics', slug='electronics')
        client = APIClient()
        client.force_authenticate(user=user)
        data = {
            'category_id': str(category.id),
            'title': 'Test Listing',
            'description': 'Test description',
            'price': '1000000',
            'condition': 'USED',
            'location': 'Ho Chi Minh City'
        }
        response = client.post('/api/v1/listings/', data)
        assert response.status_code == 201
        assert Listing.objects.filter(title='Test Listing').exists()

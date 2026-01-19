"""
URLs for listings app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'listings'

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'', views.ListingViewSet, basename='listing')

urlpatterns = [
    path('', include(router.urls)),
]

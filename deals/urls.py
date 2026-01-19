"""
URLs for deals app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'deals'

router = DefaultRouter()
router.register(r'offers', views.OfferViewSet, basename='offer')
router.register(r'', views.DealViewSet, basename='deal')

urlpatterns = [
    path('', include(router.urls)),
]

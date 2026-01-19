"""
URLs for moderation app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'moderation'

router = DefaultRouter()
router.register(r'', views.ReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
]

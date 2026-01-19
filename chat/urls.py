"""
URLs for chat app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'chat'

router = DefaultRouter()
router.register(r'', views.ConversationViewSet, basename='conversation')

urlpatterns = [
    path('', include(router.urls)),
]

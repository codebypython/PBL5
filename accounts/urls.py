"""
URLs for accounts app.
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('me/', views.CurrentUserView.as_view(), name='current-user'),
    path('me/profile/', views.ProfileUpdateView.as_view(), name='profile-update'),
]

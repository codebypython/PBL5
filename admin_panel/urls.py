"""
URLs for admin panel app.
"""
from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('reports/', views.ReportListView.as_view(), name='reports'),
    path('reports/<uuid:id>/resolve/', views.ResolveReportView.as_view(), name='resolve-report'),
    path('users/<uuid:id>/ban/', views.BanUserView.as_view(), name='ban-user'),
]

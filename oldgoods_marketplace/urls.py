"""
URL configuration for oldgoods_marketplace project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/users/', include('accounts.urls')),
    path('api/v1/categories/', include('listings.urls')),
    path('api/v1/listings/', include('listings.urls')),
    path('api/v1/conversations/', include('chat.urls')),
    path('api/v1/offers/', include('deals.urls')),
    path('api/v1/deals/', include('deals.urls')),
    path('api/v1/reports/', include('moderation.urls')),
    path('api/v1/admin/', include('admin_panel.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

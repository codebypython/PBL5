"""
WSGI config for oldgoods_marketplace project.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oldgoods_marketplace.settings')

application = get_wsgi_application()

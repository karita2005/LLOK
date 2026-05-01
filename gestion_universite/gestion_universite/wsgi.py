"""
Configuration WSGI pour le projet gestion_universite.

Expose l'application WSGI comme variable de module nommée ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_universite.settings')
application = get_wsgi_application()

"""
WSGI config for quitescan project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quitescan.settings')

application = get_wsgi_application()

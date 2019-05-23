"""
WSGI config for factchecker project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application
import dotenv

dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")

application = get_wsgi_application()
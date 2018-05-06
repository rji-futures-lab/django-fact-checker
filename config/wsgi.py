"""
WSGI config for factchecker project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# ^^^ Django's out-of-the-box configuration ^^^
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
# ^^^ customization ensures that deploys default to prod settings ^^^

application = get_wsgi_application()

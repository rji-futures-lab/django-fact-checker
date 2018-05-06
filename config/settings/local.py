"""
Custom factchecker Django project settings for developers' local environment.
"""
from .base import * # noqa


DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '0.0.0.0',
    '127.0.0.1',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'sqlite.db')
    }
}

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

STATIC_URL = '/factchecker/static/'

STATICFILES_DIRS = [
    BASE_DIR / "factchecker" / "static",
]

MEDIA_URL = '/factchecker/media/'
MEDIA_ROOT = BASE_DIR / "factchecker" / "media"

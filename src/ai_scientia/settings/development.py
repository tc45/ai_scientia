from .base import *

DEBUG = True
ALLOWED_HOSTS = ['www.ai-scientia.com', '0.0.0.0','localhost', '127.0.0.1']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Add any development-specific static file settings if needed
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

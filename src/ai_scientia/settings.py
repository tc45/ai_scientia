"""
Django settings for AI_Scientia project.
Import all settings from the modular settings files.
"""

from .settings.base import *

try:
    from .settings.development import *
except ImportError:
    pass

# Add these settings for email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development

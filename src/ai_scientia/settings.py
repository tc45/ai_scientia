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

import os
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    """Get the environment variable or return exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg)

# OpenAI Settings
try:
    OPENAI_API_KEY = get_env_variable('OPENAI_API_KEY')
except ImproperlyConfigured:
    OPENAI_API_KEY = None  # For development without OpenAI

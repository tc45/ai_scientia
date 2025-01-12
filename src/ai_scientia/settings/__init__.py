"""
Initialize settings module and load environment variables
"""
from dotenv import load_dotenv
import os

# Load environment variables at the very beginning
load_dotenv()

# Import all settings from the modular settings files
from .base import *

try:
    from .development import *
except ImportError:
    pass

# OpenAI Settings
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Add these settings for email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development

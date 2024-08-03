# production.py

from .settings import *  # Import all settings from settings.py

# Override or add production-specific settings here
DEBUG = False
ALLOWED_HOSTS = []
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Add more production-specific settings as needed

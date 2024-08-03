import os
import django
from pathlib import Path

# Set the Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory.inventory.settings')

# Initialize Django
django.setup()

# Import settings
from django.conf import settings

# Check the template directories
for template_dir in settings.TEMPLATES[0]['DIRS']:
    print(f"Checking template directory: {template_dir}")

    # Check if base.html exists
    base_html_path = Path(template_dir) / 'base.html'
    if base_html_path.exists():
        print(f"Found base.html at: {base_html_path}")
    else:
        print(f"base.html not found in: {template_dir}")

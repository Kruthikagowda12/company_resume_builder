import sys
import os
from pathlib import Path

# Add the project root directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Import Django and setup
import django
django.setup()

# Run migrations on startup if using production database
if os.getenv('DATABASE_URL'):
    from django.core.management import call_command
    try:
        call_command('migrate', verbosity=0, interactive=False)
    except Exception as e:
        print(f"Migration warning: {e}")

# Import and return the WSGI application
from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()


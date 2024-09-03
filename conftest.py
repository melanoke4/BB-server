import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bottomlessbox.settings')

def pytest_configure():
    django.setup()
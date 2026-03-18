import os
import sys

from django.core.management import execute_from_command_line

# Set DJANGO_SETTINGS_MODULE if not already set
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TrainerRegistry_site.settings")

# Disable Django auto-reloader for PyInstaller
argv = ["manage.py", "runserver", "127.0.0.1:8000", "--noreload"]

# Run Django management command
execute_from_command_line(argv)
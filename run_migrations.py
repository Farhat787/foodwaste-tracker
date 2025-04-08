# foodwaste_project/run_migrations.py
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodwaste_project.settings")
django.setup()

from django.core.management import call_command
call_command('migrate')

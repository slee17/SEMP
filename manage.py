#!/usr/bin/env PYTHONWARNINGS=ignore python
import os, sys, django

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SEMP.settings")

    from django.core.management import execute_from_command_line
    django.setup()

    execute_from_command_line(sys.argv)

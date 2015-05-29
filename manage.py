#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":

    
    sys.path.insert(0, '/var/app')
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.production")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

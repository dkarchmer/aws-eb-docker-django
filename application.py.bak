__author__ = 'David Karchmer'
'''
This file should not be needed, but trying this solution anyway as per
http://stackoverflow.com/questions/27141577/elastic-beanstalk-django-deployment-with-preconfigured-docker-container
'''

import os
import sys

sys.path.insert(0, '/var/app')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

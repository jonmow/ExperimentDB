import os
import sys

sys.path.append('/usr/lib/python2.6/site-packages/django/')
sys.path.append('/usr/src/django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'experimentdb.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


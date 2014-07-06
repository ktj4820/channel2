"""
WSGI config for channel2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os, sys
sys.path.append('/var/www/channel2/django')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "channel2.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

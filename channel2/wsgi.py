import os, sys

sys.path.append('/var/www/channel2/django')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "channel2.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

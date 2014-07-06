import os
import datetime

DEBUG = False
DEBUG_TOOLBAR = False
DEBUG_TOOLBAR_PATCH_SETTINGS = False
TEMPLATE_DEBUG = DEBUG

RESOURCE_VERSION = 'fabric:resource-version'

ALLOWED_HOSTS = ['channel2.derekkwok.net']
SESSION_COOKIE_DOMAIN = 'channel2.derekkwok.net'

MEDIA_ROOT = '/var/www/channel2/media'

STATIC_ROOT = '/var/www/channel2/static/{}'.format(RESOURCE_VERSION)
STATIC_URL = '/static/{}/'.format(RESOURCE_VERSION)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'channel2',
        'USER': 'channel2_user',
        'PASSWORD': os.environ.get('CHANNEL2_DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    },
}

SITE_DOMAIN = 'channel2.derekkwok.net'
SITE_SCHEME = 'http'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'derek.kai.chun.kwok@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('CHANNEL2_EMAIL_PASSWORD')
EMAIL_USE_TLS = True

FFMPEG_PATH = '/usr/local/bin/ffmpeg'
VIDEO_DIR = '/var/www/channel2/downloads/'
X_ACCEL = True

#-------------------------------------------------------------------------------
# logging settings
#-------------------------------------------------------------------------------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    # formatters
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },

    # filters
    'filters': {},

    # handlers
    'handlers': {
        'email_admin': {
            'level': 'ERROR',
            'filters': [],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'channel2': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/var/www/channel2/logs/channel2-{}.log'.format(datetime.datetime.now().strftime('%Y%m%d')),
            'encoding': 'utf-8',
        },
    },

    # loggers
    'loggers': {
        '': {
            'handlers': ['channel2'],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': ['email_admin', 'channel2'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

import os

DEBUG = False
DEBUG_TOOLBAR = False
DEBUG_TOOLBAR_PATCH_SETTINGS = False
TEMPLATE_DEBUG = DEBUG

RESOURCE_VERSION = 'fabric:resource-version'

ALLOWED_HOSTS = ['channel2.derekkwok.net']
SESSION_COOKIE_DOMAIN = 'channel2.derekkwok.net'

MEDIA_ROOT = '/var/www/fufufuu/media'

STATIC_ROOT = '/var/www/fufufuu/static/{}'.format(RESOURCE_VERSION)
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
X_ACCEL = False

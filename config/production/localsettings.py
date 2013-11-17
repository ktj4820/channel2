import os

MEDIA_ROOT = '/var/www/channel2/media/'
STATIC_ROOT = '/var/www/channel2/static/'

DEBUG = False
DEBUG_TOOLBAR = False

TEMPLATE_DEBUG = DEBUG

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'derek.kai.chun.kwok@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('CHANNEL2_EMAIL_PASSWORD')
EMAIL_USE_TLS = True

X_ACCEL = True
FFMPEG_PATH = '/usr/bin/ffmpeg'

RESOURCE_VERSION = 'fabric:resource-version'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'channel2',
        'USER': 'channel2_user',
        'PASSWORD': os.environ.get('CHANNEL2_DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = [
    'channel2.derekkwok.net',
]

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

SITE_SCHEME = 'http'
SITE_DOMAIN = 'channel2.derekkwok.net'

SECRET_KEY = os.environ.get('CHANNEL2_SECRET_KEY')

ALLOWED_HOSTS = [
    'channel2.derekkwok.net',
    '63.141.249.146',
]

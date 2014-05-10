from getpass import getuser
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '+$^o1$rzm*a2(gx)g+!vx3j)(k!-$r&8joy^zkd361%pk*)mm9'

DEBUG = False
DEBUG_TOOLBAR = False
DEBUG_TOOLBAR_PATCH_SETTINGS = True
TEMPLATE_DEBUG = DEBUG

RESOURCE_VERSION = 'development'

ADMINS = (
    ('Derek Kwok', 'derek.kai.chun.kwok@gmail.com'),
)

ALLOWED_HOSTS = []
INTERNAL_IPS = ['127.0.0.1',]

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'channel2.urls'
WSGI_APPLICATION = 'channel2.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'channel2',
        'USER': getuser(),
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True

TIME_ZONE = 'UTC'
USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = ''
STATIC_URL = '/static/{}/'.format(RESOURCE_VERSION)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

#-------------------------------------------------------------------------------
# localsettings.py
#-------------------------------------------------------------------------------

try:
    from channel2.localsettings import *
except ImportError:
    pass


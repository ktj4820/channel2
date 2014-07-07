from getpass import getuser
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '+$^o1$rzm*a2(gx)g+!vx3j)(k!-$r&8joy^zkd361%pk*)mm9'

DEBUG = False
DEBUG_TOOLBAR = False
DEBUG_TOOLBAR_PATCH_SETTINGS = True
TEMPLATE_DEBUG = DEBUG

RESOURCE_VERSION = 'development'

ADMINS = []

ALLOWED_HOSTS = []
INTERNAL_IPS = ['127.0.0.1',]

INSTALLED_APPS = (
    'suit',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'haystack',

    'channel2.account',
    'channel2.blog',
    'channel2.core',
    'channel2.flat',
    'channel2.search',
    'channel2.staff',
    'channel2.tag',
    'channel2.video',
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
        'TEST_NAME': 'channel2_test',
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

AUTH_USER_MODEL = 'account.User'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

TEST_RUNNER = 'channel2.core.tests.Channel2TestSuiteRunner'

#-------------------------------------------------------------------------------
# template settings
#-------------------------------------------------------------------------------

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',
    'django.contrib.messages.context_processors.messages',
    'channel2.core.context_processors.resource_version',
    'channel2.tag.context_processors.pinned_tags',
)

#-------------------------------------------------------------------------------
# local site settings
#-------------------------------------------------------------------------------

SITE_DOMAIN = 'localhost:8000'
SITE_SCHEME = 'http'

EMAIL_HOST = ''
EMAIL_PORT = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True

FFMPEG_PATH = ''
VIDEO_DIR = ''
VIDEO_LINK_EXPIRE = 6 * 60 * 60
X_ACCEL = False

#-------------------------------------------------------------------------------
# search settings
#-------------------------------------------------------------------------------

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'channel2',
    },
}

#-------------------------------------------------------------------------------
# localsettings.py
#-------------------------------------------------------------------------------

try:
    from channel2.localsettings import *
except ImportError:
    pass

#-------------------------------------------------------------------------------
# see if we need to import debug toolbar
#-------------------------------------------------------------------------------

if DEBUG_TOOLBAR:
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    DISABLE_PANELS = {
        'INTERCEPT_REDIRECTS': False,
    }

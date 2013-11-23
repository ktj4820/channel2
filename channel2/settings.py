import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = False
DEBUG_TOOLBAR = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Derek Kwok', 'derek.kai.chun.kwok@gmail.com'),
)

INTERNAL_IPS = (
    '127.0.0.1',
)

ALLOWED_HOSTS = [
    '127.0.0.1',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'channel2.sqlite3'),
        'TEST_NAME': os.path.join(BASE_DIR, 'data/test.sqlite3'),
    }
}

TIME_ZONE = 'UTC'
USE_TZ = True

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'channel2.urls'

WSGI_APPLICATION = 'channel2.wsgi.application'

SECRET_KEY = '@dv6m-7frx&c9ie5+&t2t4(1yy!z6p6562kjtuki_!n4iavo6#'

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
    'channel2.label.context_processors.pinned_labels',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',

    'haystack',
    'south',

    'channel2.account',
    'channel2.core',
    'channel2.flat',
    'channel2.label',
    'channel2.search',
    'channel2.video',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

AUTH_USER_MODEL = 'account.User'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'

TEST_RUNNER = 'channel2.core.tests.Channel2TestSuiteRunner'

#-------------------------------------------------------------------------------
# logging configuration
#-------------------------------------------------------------------------------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'channel2.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 9,
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

#-------------------------------------------------------------------------------
# search configuration
#-------------------------------------------------------------------------------

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh'),
    },
}

#-------------------------------------------------------------------------------
# local site settings
#-------------------------------------------------------------------------------

FFMPEG_PATH = ''

# The length for which the video link is valid for
VIDEO_LINK_EXPIRE = 6 * 60 * 60

X_ACCEL = False

SITE_DOMAIN = 'localhost:8000'
SITE_SCHEME = 'http'

EMAIL_HOST = ''
EMAIL_PORT = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True

RESOURCE_VERSION = ''

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
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

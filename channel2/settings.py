import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

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
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'channel2.urls'

WSGI_APPLICATION = 'channel2.wsgi.application'

SECRET_KEY = '@dv6m-7frx&c9ie5+&t2t4(1yy!z6p6562kjtuki_!n4iavo6#'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'channel2.sqlite3'),
    }
}

TIME_ZONE = 'UTC'
USE_TZ = True

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

STATIC_URL = '/static/'

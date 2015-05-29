"""
Django settings for MySite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import socket

SITE_ID = 1

# Assumes
# - base
# --- myproject
# -------- urls.py
# -------- etc.
# --- server
# -------- settings
# ------------- prod.py
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_PROJECT_DIR = os.path.join(BASE_DIR, 'myproject')
print('BASE_PROJECT_DIR = ' + BASE_PROJECT_DIR)

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('admin', 'admin@mysite.com'),
)
ADMIN_USERNAME = 'admin'
ADMIN_EMAIL = 'admin@mysite.com'
ADMIN_INITIAL_PASSWORD = 'admin' # To be changed after first login by admin


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gp-kui+1mi6d!^u$*wvfoo^ostr1+(pns*=q3p%=fsoppe5123'

FIXTURE_DIRS = (
    #os.path.join(BASE_PROJECT_DIR, 'fixtures'),
)


# Application definition

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Admin panel and documentation:
    'django.contrib.admin',
    # 'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    'bootstrap3',
    'rest_framework',
    'rest_framework.authtoken',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'myproject.main',
)

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'myproject.urls'

#WSGI_APPLICATION = 'myproject.wsgi.application'
WSGI_APPLICATION = 'application.application'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

local_ip = str(socket.gethostbyname(socket.gethostname()))

print ('hostname: ' + socket.gethostname())
print ('hostbyname: ' + local_ip)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

template_path = os.path.join(BASE_PROJECT_DIR, 'templates')
print('template_path = ' + template_path)

TEMPLATE_DIRS = (
    template_path,
)




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

static_path = os.path.join(BASE_PROJECT_DIR, 'static')
print('static_path = ' + static_path)
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ('images', os.path.join(static_path, 'images')),
    ('js', os.path.join(static_path, 'js')),
    ('css', os.path.join(static_path, 'css')),
)
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# Boto S3 Configuration
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'


REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),

    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),

    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 100,
}

# one email per XX seconds
LOGLIMIT_RATE = 10

# uses keys to detect which errors are the same
LOGLIMIT_MAX_KEYS = 100

# uses cache if it's available
LOGLIMIT_CACHE_PREFIX = 'LOGLIMIT'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'null': {
            'level': 'ERROR',
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django.request':{
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security.DisallowedHost': {
             'handlers': ['null'],
             'propagate': False,
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

BOOTSTRAP3 = {

    # The URL to the jQuery JavaScript file
    'jquery_url': '//ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js',

    # The Bootstrap base URL
    'base_url': '//netdna.bootstrapcdn.com/bootstrap/3.3.1/',

    # The complete URL to the Bootstrap CSS file (None means derive it from base_url)
    'css_url': None,

    # The complete URL to the Bootstrap CSS file (None means no theme)
    'theme_url': '//maxcdn.bootstrapcdn.com/bootswatch/3.3.1/flatly/bootstrap.min.css',

    # The complete URL to the Bootstrap JavaScript file (None means derive it from base_url)
    'javascript_url': None,

    # Put JavaScript in the HEAD section of the HTML document (only relevant if you use bootstrap3.html)
    'javascript_in_head': False,

    # Include jQuery with Bootstrap JavaScript (affects django-bootstrap3 template tags)
    'include_jquery': True,

    # Label class to use in horizontal forms
    'horizontal_label_class': 'col-md-2',

    # Field class to use in horiozntal forms
    'horizontal_field_class': 'col-md-4',

    # Set HTML required attribute on required fields
    'set_required': True,

    # Set placeholder attributes to label if no placeholder is provided
    'set_placeholder': True,

    # Class to indicate required (better to set this in your Django form)
    'required_css_class': '',

    # Class to indicate error (better to set this in your Django form)
    'error_css_class': 'has-error',

    # Class to indicate success, meaning the field has valid input (better to set this in your Django form)
    'success_css_class': 'has-success',

    # Renderers (only set these if you have studied the source and understand the inner workings)
    'formset_renderers':{
        'default': 'bootstrap3.renderers.FormsetRenderer',
    },
    'form_renderers': {
        'default': 'bootstrap3.renderers.FormRenderer',
    },
    'field_renderers': {
        'default': 'bootstrap3.renderers.FieldRenderer',
        'inline': 'bootstrap3.renderers.InlineFieldRenderer',
    },
}



# Overwrite User Model with 'Authentication.Account'
#
INSTALLED_APPS += ('authentication',)
AUTH_USER_MODEL = 'authentication.Account'
LOGIN_URL          = '/account/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/account/login-error/'


"""
Django settings for STATsite project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$n%#cfmwx#10^n&+w9t)p^6(xo@@)07um7$ywak7s%uc^d$20&'

# SECURITY WARNING: don't run with debug turned on in production!
# When switching to False, properly set the ALLOWED_HOSTS setting!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

DEFAULT_APPS = ( # the names of all Django applications that are activated in
                 # this Django instance
    'django.contrib.admin', # the admin site
    'django.contrib.auth', # an authentication system
    'django.contrib.contenttypes', # a framework for content types
                                   # used by the authentication application to
                                   # track models installed in your database
    'django.contrib.sessions', # a session framework
    'django.contrib.messages', # a messaging framework
    'django.contrib.staticfiles', # a framework for managing static files
)

ACCOUNT_ACTIVATION_DAYS = 7 # For registration configuration.

THIRD_PARTY_APPS = (
    # nothing yet
)

LOCAL_APPS = (
    'registration',
    'registration.supplements.default' # Or set REGISTRATION_SUPPLEMENT_CLASS
                                       # to None (no registration supplemental
                                       # information will be used).
    # 'mailer', # Using django-mailer instead of Django's default email system.
)

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'STATsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # A list of filesystem directories to check for loading Django templates.
        # Secret path.
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'STATsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'SLee17',
        'USER': 'SLee17',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': 5432,
    },
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# Emails
# Configuring so that the console backend writes the emails that would be sent.
# Uses stdout by default; can use a different stream-like object by providing the
# stream keyword argument when constructing the connection.
# NOT TO BE USED FOR PRODUCTION
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
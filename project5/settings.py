"""
Django settings for project5 project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qC2sb5`5~zC^Obe4T"e}8vg]e%$xt5T#MoF_8t?i]{eGp=U!$U';
PAYPAL_CLIENTID = 'AeTA5VvJCXRO12TNyR9QEhumUo0M-SFkmzgHYEIdkFecxmNM5xySi62FVCjlZPqzcTddKsGWI1veSCoD'
PAYPAL_SECRET = 'EFu-IHq2Q9eVH9wolU4Pme_Aqyq-HekyO0uGVwBY6Bg7aKqmE7nbpy_ny2vV3_RySo2NJHIqSR-NAgty'
PAYPAL_URLTOKEN = 'https://api.sandbox.paypal.com/v1/oauth2/token'
PAYPAL_URLORDER = 'https://api.sandbox.paypal.com/v2/checkout/orders'
PAYPAL_URLSHOW = 'https://api.sandbox.paypal.com/v2/checkout/orders/<ORDERID>'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','127.0.0.1']

# APPLICATION CONSTANTS
FILTER_INITIAL_NAME = "All categories"

# Application definition

INSTALLED_APPS = [
    'courses',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project5.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "courses.context_processors.settings",
            ],
        },
    },
]

WSGI_APPLICATION = 'project5.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'new.sqlite3'),
    },
    'test': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_tests.sqlite3'),
    },
}

AUTH_USER_MODEL = "courses.User"

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# For media files uploades by user
MEDIA_ROOT = os.path.join(BASE_DIR, 'courses/media')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'


DEFAULT_AUTO_FIELD='django.db.models.AutoField' 

TEST_RUNNER = "redgreenunittest.django.runner.RedGreenDiscoverRunner"

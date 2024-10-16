"""
Django settings for ecommerceproject project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
# import environ

# import environ

# env = environ.Env()
# environ.Env.read_env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mt@dn%)vf_#@excx*omgv-6%t$kb2=$8+r+ol54k8=6l7ej_%r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = [/..]
# ALLOWED_HOSTS = ['ecommerceapp.onrender.com', 'localhost']
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'project-6-f9hu.onrender.com',
    '.onrender.com',
    
    #'project-4-r6l3.onrender.com',
    # You can add more domains if needed
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ecommerceapp',
    'django_bootstrap5',
    
]

# Settings for serving static files on Render
if not DEBUG:
    # Configure these only for production
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'ecommerceproject.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerceproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Use MySQL database backend
        'NAME': 'ecommerceproject',              # Your database name
        'USER': 'root',           # Your MySQL username
        'PASSWORD': 'Mikaelson@12.',      # Your MySQL password
        'HOST': 'localhost',                      # Database host (usually localhost)
        'PORT': '3306',                          # Default MySQL por
        # 'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# Parse database configuration from the environment variable for Render deployment
DATABASES['default'] = dj_database_url.config(
    default=os.getenv('DATABASE_URL', 'mysql://root:Mikaelson@12.@localhost:3306/ecommerceproject')
)


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL =  '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
LOGIN_REDIRECT_URL = '/profile/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'ecommerceapp', 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Configure static file storage to use Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Ensure your STATICFILES_DIRS is set correctly
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', 'sk_test_51Q4kgtE7JEpDvfCUlQ5g9X8JIHCqhoN0Hz7oD5r2G7V7PeCDgVJv8UnO89A5wpITq9w4hahLayk40DodZUhbZCgD00cJYDYJgT')
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', 'pk_test_51Q4kgtE7JEpDvfCUJuSA5RXIibRFFx0VHePxEftQvsNeKLP3sywZEBoByulhKur2bLahV5sWwK0JsBgjrwU8t6Zy00Dh2xIg3E')
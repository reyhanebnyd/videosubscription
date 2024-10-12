"""
Django settings for videosubscription project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os  
from decouple import config 

# Specify the path to the .env file  



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
#print(BASE_DIR)
MEDIA_URL = '/media/'  
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 

GOOGLE_OAUTH2_CLIENT_ID = config("DJANGO_GOOGLE_OAUTH2_CLIENT_ID")  
GOOGLE_OAUTH2_CLIENT_SECRET = config("DJANGO_GOOGLE_OAUTH2_CLIENT_SECRET")  
GOOGLE_OAUTH2_PROJECT_ID = config("DJANGO_GOOGLE_OAUTH2_PROJECT_ID")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-sv^azmuh--rknv68u@9ia6szb)g2tcjf)2)$^j4p%qwk@-2-+w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
AUTH_USER_MODEL = 'User.CustomUser'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  
    'allauth',  
    'allauth.account',  
    'allauth.socialaccount',  
    'allauth.socialaccount.providers.google', 
    'dj_rest_auth',
    'rest_framework',
    'rest_framework.authtoken',
    'User',
    'Video',
    'subscription',
    'django_celery_beat',
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    # 'allauth.account.auth_backends.AuthenticationBackend',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'videosubscription.urls'

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

WSGI_APPLICATION = 'videosubscription.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

SITE_ID = 1  
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

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': (  
        'rest_framework.authentication.TokenAuthentication',  # Ensure correct import  
        'rest_framework.authentication.SessionAuthentication',  # Optional  
        'rest_framework_simplejwt.authentication.JWTAuthentication', 
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.IsAuthenticated',
    ]
}

AUTHENTICATION_BACKENDS = (  
    #'User.backend.EmailOrPhoneOrUsernameBackend',  
    'django.contrib.auth.backends.ModelBackend', 
    'allauth.account.auth_backends.AuthenticationBackend',  
)  

ACCOUNT_EMAIL_REQUIRED = True  
ACCOUNT_EMAIL_VERIFICATION = "none" 
ACCOUNT_AUTHENTICATION_METHOD = 'username' # To skip email verification during development  
LOGIN_URL = "account_login"  
LOGIN_REDIRECT_URL = "/"  
ACCOUNT_LOGOUT_REDIRECT_URL = '/' 

# from datetime import timedelta  
# from rest_framework_simplejwt.authentication import JWTAuthentication  

# SIMPLE_JWT = {  
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),  
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  
#     'AUTH_HEADER_TYPES': ('Bearer',),  
# }  
CELERY_BROKER_URL = 'redis://localhost:6379/0'   
CELERY_ACCEPT_CONTENT = ['json']  
CELERY_TASK_SERIALIZER = 'json' 

ASGI_APPLICATION = 'videosubscription.asgi.application'
  
CHANNEL_LAYERS = {  
    'default': {  
        'BACKEND': 'channels_redis.core.RedisChannelLayer',  
        'CONFIG': {  
            "hosts": [('127.0.0.1', 6379)],  
        },  
    },  
}
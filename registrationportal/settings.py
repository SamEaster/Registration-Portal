from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
import sys
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

if os.environ.get('prod_key'):
    SECRET_KEY =os.environ.get('prod_key')
else:
    SECRET_KEY = 'django-insecure-_+hx!lw-eln-tyl1)baz)^g6tjq$m-9t3---va#jziklcg+xl*'
PROD= not os.environ.get('prod_key')
DEBUG = not os.environ.get('prod')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    #django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #apps
    'apps.users',
    'apps.competitions',
    'apps.offlinePortal',
    # 'apps.data',
     #utililty
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
            'prompt': 'select_account',
        },
        'CLIENT_ID': '',
        'SECRET': '',
    }
}

# In settings.py
SOCIALACCOUNT_ADAPTER = 'users.adapter.MySocialAccountAdapter'  # Replace 'yourapp' with your actual app name

ROOT_URLCONF = 'registrationportal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'registrationportal.wsgi.application'

if PROD:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('db_name'),
            'USER': os.environ.get('db_user'),
            'PASSWORD': os.environ.get('db_password'),
            'HOST': os.environ.get('db_host'),
            'PORT': os.environ.get('db_port')
        }
    }

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'users.NewUser'

# Setup Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
# EMAIL_HOST_USER = os.environ.get('email')
# EMAIL_HOST_PASSWORD = os.environ.get('password')
EMAIL_HOST_USER = 'sarveshmurkute@gmail.com'
EMAIL_HOST_PASSWORD = 'pmhyuzoxxsjuibgb'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SITE_ID = 1

# Setup Static
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Setup Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Minio Storage
if not PROD:
    DEFAULT_FILE_STORAGE = "minio_storage.storage.MinioMediaStorage"
    STATICFILES_STORAGE = "minio_storage.storage.MinioStaticStorage"
    MINIO_STORAGE_ENDPOINT = os.environ.get('minio_endpoint')
    MINIO_STORAGE_ACCESS_KEY = os.environ.get('minio_access')
    MINIO_STORAGE_SECRET_KEY = os.environ.get('minio_secret')
    MINIO_STORAGE_USE_HTTPS = True
    MINIO_STORAGE_MEDIA_BUCKET_NAME = 'alcherregmedia'
    MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True
    MINIO_STORAGE_STATIC_BUCKET_NAME = 'alcherregstatic'
    MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CSRF_TRUSTED_ORIGINS = ['https://registrations.alcheringa.in','https://registration.alcheringa.in', 'https://reg.alcheringa.in']

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
SOCIALACCOUNT_LOGIN_ON_GET = True

LOGIN_REDIRECT_URL = '/auth/profile_set/'  # Redirect after login
LOGOUT_REDIRECT_URL = '/'       # Redirect after logout

# settings.py
TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_PHONE_NUMBER = ""

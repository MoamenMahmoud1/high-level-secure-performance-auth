"""
Base settings shared between development & production.
"""

from pathlib import Path
import os
from decouple import config
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 SECURITY
SECRET_KEY = config("SECRET_KEY")
JWE_KEY = config("JWE_KEY")



# 🧩 INSTALLED APPS
DJANGO_APPS = [
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_celery_beat",
]

THIRD_PARTY_APPS = [

    'storages',
    "corsheaders",
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'phonenumber_field',
    'silk',
]

PROJECT_APPS = [
    'accounts.apps.AccountsConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

# 🧵 MIDDLEWARE
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'middleware.DecryptRefreshMiddleware',
    'silk.middleware.SilkyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 🔗 URL / WSGI
ROOT_URLCONF = 'prod.urls'
WSGI_APPLICATION = 'prod.wsgi.application'

# 🎨 TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 🗄 DATABASE DEFAULT (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🔐 PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌍 INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
#USE_I18N = True
#USE_TZ = True

# 📁 STATIC & MEDIA
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# 🔐 AUTH
AUTH_USER_MODEL = 'accounts.CustomUserModel'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'accounts.authentication_email.EmailAuthBackend',
]

# 🔥 DRF + JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'authentication.CookieJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'common.permissions.RoleBasePermission',
    ),
        "DEFAULT_THROTTLE_RATES": {
        "user": "50/min",  
        "anon": "20/min",  
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# 📧 EMAIL (من ENV)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', cast=int, default=25)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@example.com')

FRONTEND_URL = config('FRONTEND_URL', default="http://localhost:3000")

# 🌐 GOOGLE LOGIN
GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID", default="")
GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET", default="")
GOOGLE_REDIRECT_URI = config("GOOGLE_REDIRECT_URI", default="")





# Caching
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("REDIS_URL", default="redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
        }
    }
}

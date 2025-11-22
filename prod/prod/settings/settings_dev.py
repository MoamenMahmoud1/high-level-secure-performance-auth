from .settings_base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",  
    }
}
# Local Static & Media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# Dev Cookies
#SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 يوم
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
#SESSION_COOKIE_DOMAIN = "127.0.0.1"  # optional


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CELERY_BROKER_URL = config("CELERY_BROKER_URL", default="amqp://myuser:mypassword@localhost:5672/")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default="rpc://")
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30



# 🌐 CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "https://127.0.0.1:5500",
    'https://localhost:5500',
]
CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-requested-with",
    "accept",
    "origin",
    "user-agent",
    "access-control-allow-origin",
    "access-control-request-method",
    "access-control-request-headers",
]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",  
    },
}


SESSION_ENGINE = 'django.contrib.sessions.backends.db'

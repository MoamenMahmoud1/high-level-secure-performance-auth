from .settings_base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# PostgreSQL dev (يمكن استخدام SQLite إذا أردت)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='mydb'),
        'USER': config('DB_USER', default='myuser'),
        'PASSWORD': config('DB_PASSWORD', default='mypassword'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Local Static & Media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# Dev Cookies
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = 'Lax'

# Email backend console (يمكن تغييره إذا أردت)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CELERY_BROKER_URL = config("CELERY_BROKER_URL", default="amqp://myuser:mypassword@localhost:5672/")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default="rpc://")
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30

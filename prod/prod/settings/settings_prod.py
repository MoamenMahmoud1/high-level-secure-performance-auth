from .settings_base import *

DEBUG = False
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")])

# PostgreSQL Production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Static & Media (S3)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Secure Cookies
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'lax'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'lax'



SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000  # سنة
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# Email SMTP from ENV
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Celery settings
CELERY_BROKER_URL = config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND")
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30


# ☁️ AWS defaults
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", default="")
AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME", default="eu-central-1")
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
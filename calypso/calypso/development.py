
import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = True

ALLOWED_HOSTS = ['*']

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.ionos.co.uk'
EMAIL_HOST_USER = 'info@calypsosun.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'Calypso Sun <info@calypsosun.com>'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DRF_RECAPTCHA_TESTING = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

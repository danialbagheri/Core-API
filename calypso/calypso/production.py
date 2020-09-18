

# Save the following environment variable in your environment
# export DB_USER = "my_db_user"
# export DB_PASS = "my_db_password"

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = False

ALLOWED_HOSTS = ['*']

EMAIL_USE_TLS = True
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.ionos.co.uk'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'Calypso Sun <info@calypsosun.com>'
CSRF_COOKIE_DOMAIN = '.calypsosun.com'
SESSION_COOKIE_SAMESITE = None
# Whether the session cookie should be secure (https:// only).
SESSION_COOKIE_SECURE = True
MYSQL_DB_NAME= os.environ.get('MYSQL_DB_NAME', "")
MYSQL_USER_NAME= os.environ.get('MYSQL_USER_NAME', "")
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', "")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_DB_NAME,
        'USER': MYSQL_USER_NAME,
        'PASSWORD': MYSQL_PASSWORD,
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
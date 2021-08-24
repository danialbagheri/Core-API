

# Save the following environment variable in your environment
# export DB_USER = "my_db_user"
# export DB_PASS = "my_db_password"

from pathlib import Path
import environ
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env()
CSRF_COOKIE_DOMAIN = '.calypsosun.com'
SESSION_COOKIE_SAMESITE = None
# Whether the session cookie should be secure (https:// only).
SESSION_COOKIE_SECURE = False
MYSQL_DB_NAME= env('MYSQL_DB_NAME')
MYSQL_USER_NAME= env('MYSQL_USER_NAME')
MYSQL_PASSWORD = env('MYSQL_PASSWORD')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
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
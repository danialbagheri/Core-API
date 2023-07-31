# Save the following environment variable in your environment
# export DB_USER = "my_db_user"
# export DB_PASS = "my_db_password"

from pathlib import Path
import environ
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env()
CSRF_COOKIE_DOMAIN = env('CSRF_COOKIE_DOMAIN')
SESSION_COOKIE_SAMESITE = None
# Whether the session cookie should be secure (https:// only).
SESSION_COOKIE_SECURE = False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'OPTIONS': env.json('DB_OPTIONS'),
    }
}

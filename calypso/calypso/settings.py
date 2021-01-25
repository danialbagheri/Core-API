"""
Django settings for calypso project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()
DEBUG = env.bool('DEBUG')
PRODUCTION_ENVIRONMENT = env.bool('PRODUCTION_ENVIRONMENT')
if PRODUCTION_ENVIRONMENT:
    try:
        # this production_settings.py is kept off github to keep the secret key secret
        from .production import *
    except ImportError:
        pass
else:
    # it's development

    try:
        from .development import *
    except ImportError:
        pass
# Email configs
EMAIL_USE_TLS = True
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'Calypso Sun <info@calypsosun.com>'
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
SHOPIFY_API_KEY = env('SHOPIFY_API_KEY')
SHOPIFY_PASSWORD = env('SHOPIFY_PASSWORD')
API_VERSION = "2020-10"
SHOPIFY_URL = "https://%s:%s@lincocare.myshopify.com/admin/api/%s" % (
    SHOPIFY_API_KEY, SHOPIFY_PASSWORD, API_VERSION)
DRF_RECAPTCHA_SECRET_KEY = env('DRF_RECAPTCHA_SECRET_KEY')
# DRF_RECAPTCHA_DOMAIN = "127.0.0.1:8000"
DRF_RECAPTCHA_PROXY = env.dict("DRF_RECAPTCHA_PROXY")
# Instagram API keys
INSTAGRAM_INSTANT_TOKEN_API = env('INSTAGRAM_INSTANT_TOKEN_API')
INSTAGRAM_USER_ID = env('INSTAGRAM_USER_ID')
# product = shopify.Product.find( title = "Scalp protection" )
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
    'django_grapesjs',
    'user',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'phonenumber_field',
    'django_summernote',
    'corsheaders',
    'crispy_forms',
    'web',
    'product',
    'blog',
    'page',
    'review',
    'dashboard',
    'django.contrib.sitemaps',
    'rest_framework',
    'drf_recaptcha',
    'ordered_model',
    'django.contrib.sites',
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'calypso.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'calypso.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases



# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'user.User'
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


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DATETIME_FORMAT': '%d %b %y',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        # 'calypso.throttling.PostAnonymousRateThrottle',
        'calypso.throttling.PutAnonymousRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10000/day',
        'user': '1000000/day',
        # 'post_anon':'3/minute',
        'put_anon':'2/minute',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'GB'

USE_I18N = True

USE_L10N = True

USE_TZ = True

X_FRAME_OPTIONS = 'SAMEORIGIN'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static_root",
    # '/var/www/static/',
]
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = '/media/'
MEDIA_ROOT = str(BASE_DIR / "media")
#MEDIA_ROO#T = os.path.join(BASE_DIR, 'media')
print(MEDIA_ROOT)
ADMINS = [x.split(':') for x in env.list('DJANGO_ADMINS')]
MANAGERS = [x.split(':') for x in env.list('DJANGO_MANAGERS')]
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

CORS_ORIGIN_ALLOW_ALL = True
# TODO: to be deleted on the live server
CORS_ALLOWED_ORIGINS = (
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8000',
    'http://localhost:3000',
)
CRISPY_TEMPLATE_PACK = 'bootstrap4'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
DATA_UPLOAD_MAX_MEMORY_SIZE = 9437184
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
EMAIL_SUBJECT_PREFIX = "Calypso Sun - "
DEFAULT_FROM_EMAIL = "info@calypsosun.com"
SERVER_EMAIL = "info@calypsosun.com"
SITE_ID = 1
PHONENUMBER_DB_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_REGION = "GB"
SUMMERNOTE_THEME = 'bs4'  # Show summernote with Bootstrap4
SUMMERNOTE_CONFIG = {
    'iframe': True,
    'summernote': {
        'focus': True,
        'fontSizes': ['8', '9', '10', '11', '12', '14', '18', '22', '24', '36', '48', '64', '82', '150'],
        'width': '100%',
        'height': '400px',
        'prettifyHtml': True,
        'toolbar': [
            ['undo', ['undo', ]],
            ['redo', ['redo', ]],
            ['style', ['style']],
            ['fontsize', ['fontsize']],
            ['font', ['bold', 'italic', 'clear', 'strikethrough', 'underline', ]],
            ['fontname', ['fontname']],
            ['color', ['forecolor', 'backcolor', 'color']],
            ['misc', ['link', 'picture', 'print', 'help', ]],
            ['para', ['ul', 'ol', 'paragraph']],
            ['view', ['fullscreen', 'codeview']],
            ['cleaner', ['cleaner']],
        ],
        'codemirror': {  # codemirror options
            'mode': 'htmlmixed',
            'lineNumbers': 'true',
            'theme': 'monokai',
            'smartIndent': True,
            'lineWrapping': True,
            'spellcheck': True,
        },
        'cleaner': {
            'action': 'button',
            'newline': '<br>',  # Summernote's default is to use '<p><br></p>'
            'notStyle': 'position:absolute;top:0;left:0;right:0',  # Position of Notification
            'icon': '<i class="note-icon">CLEAN STYLE</i>',
            'keepHtml': True,  # Remove all Html formats
            # If keepHtml is true, remove all tags except these
            'keepOnlyTags': ['<p>', '<br>', '<ul>', '<li>', '<b>', '<strong>', '<i>', '<a>', '<span>', '</br>', '<style>', '<ol>'],
            'keepClasses': True,  # Remove Classes
            # Remove full tags with contents
            'badTags': ['script', 'applet', 'embed', 'noframes', 'noscript', 'html'],
            # Remove attributes from remaining tags
            'badAttributes': ['start'],
            'limitChars': False,  # 0/false|# 0/false disables option
            'limitDisplay': 'both',  # text|html|both
            'limitStop': False  # true/false
        }
    },
    'css': (
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.29.0/theme/monokai.min.css',
    ),
    # 'js_for_code_highlight': (  # Also for SummernoteInplaceWidget
    #     os.path.join(STATIC_URL, '/summernote/summernote-ext-highlight.js'),
    # ),
}

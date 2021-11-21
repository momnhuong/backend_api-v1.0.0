import os
from . import get_os_env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ALLOWED_HOSTS = ['0.0.0.0']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'alfrrd&i-e6_z6843=v^09=wo((r1r_1x#!fsalvtgbfer_t@7'

JWT_SECRET_KEY = 'oN5lZehup7txRSWV1bIY2msLfeynB5asHQg76js6PR8y4J9SrkB36WFmo6ZA2u1bBL8CR'
TOKEN_EXPIRATION_DURATION = 2592000

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = get_os_env('DEBUG')
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1',
                 'portal-api.usdc.vn', '14.241.226.192', '0.0.0.0','api-usdc.wedigipro.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'api',
    'djoser',
    'django_filters',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'storages'
]


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Default': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS':
        'backend.pagination.CustomPagination'
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'backend.urls'

# AUTH_USER_MODEL = 'account.Account'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_os_env('MYSQL_DATABASE'),
        'USER': get_os_env('MYSQL_USER'),
        'PASSWORD': get_os_env('MYSQL_PASSWORD'),
        'HOST': get_os_env('MYSQL_HOST'),
        'PORT': get_os_env('MYSQL_PORT'),
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}

ALERT_API_KEY = get_os_env('ALERT_API_KEY')
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'new',
#         'USER': 'root',
#         'PASSWORD': 'muadongyeuthuong',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#         'OPTIONS': {'charset': 'utf8mb4'}
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Define constants

TENANT_STATUS = (
    ('Active', 1),
    ('Deactive', 0)
)
TENANT_STATUS_DEFAULT = 1

TENANT_ACCOUNT_ROLE = (
    ('SUPPER ADMIN', 'SUPPER ADMIN'),
    ('ADMIN', 'ADMIN'),
    ('TECHNICAL', 'TECHNICAL'),
    ('ACCOUNTANT', 'ACCOUNTANT')
)
TENANT_ACCOUNT_ROLE_DEFAULT = 1

# CUSTOMER_STATUS = (
#     ('Active', 1),
#     ('Deactive', 0)
# )
# CUSTOMER_STATUS_DEFAULT = 1

CUSTOMER_STATUS = (
    ('Active', 1),
    ('Deactive', 0)
)
CUSTOMER_STATUS_DEFAULT = 1

CUSTOMER_LEVEL = (
    ('Standard', 1),
    ('Vip', 2)
)
CUSTOMER_LEVEL_DEFAULT = 1

CONTRACT_STATUS = (
    ('Active', 1),
    ('Deactive', 0)
)
CONTRACT_STATUS_DEFAULT = 1

PRODUCT_STATUS = (
    ('Active', 1),
    ('Deactive', 0)
)
PRODUCT_STATUS_DEFAULT = 1

TICKET_STATUS = (
    ('Opened', 1),
    ('Pending', 2),
    ('Stuck', 3),
    ('Closed', 0)
)
TICKET_STATUS_DEFAULT = 1

TICKET_PRIORITY = (
    ('Thấp', 1),
    ('Trung bình', 2),
    ('Cao', 3),
    ('Rất cao', 4)
)
TICKET_PRIORITY_DEFAULT = 1

TICKET_TYPE = (
    ('Hỗ trợ sản phẩm', 1),
    ('Hỗ trợ từ xa', 2),
    ('Đặt lịch tương tác', 3)
)
TICKET_TYPE_DEFAULT = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'hotmail.pix@gmail.com'
EMAIL_HOST_PASSWORD = 'Muadongyeuthuong1'

HOST_RESET_PASSWORD = 'http://14.241.226.192:2035/reset-password'


# STATICFILES_DIRS = [
#     'staticfiles',
# ]

MEDIA_URL = '/media/'
MEDIA_ROOT = get_os_env('MEDIA_ROOT', 'media')
# MEDIA_HOST = get_os_env('MEDIA_HOST', 'http://127.0.0.1')
MEDIA_HOST = os.path.join(BASE_DIR)


# # s3 Storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = 'pix'
AWS_SECRET_ACCESS_KEY = '6UL7fHixKleJyXxc8eytGIIDjkQNLbdGDd7eZN8d'
AWS_STORAGE_BUCKET_NAME = 'pix'
AWS_S3_ENDPOINT_URL = 'https://s3.admon.com.vn'

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

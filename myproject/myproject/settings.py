
import os
import re
from decouple import config

AWS_EC2_HOST = config('C_AWS_EC2_HOST')
AWS_EC2_IP = re.search('^ec2-(\d{1,3}-\d{1,3}-\d{1,3}-\d{1,3})(.+)',AWS_EC2_HOST).group(1).replace('-','.')

AWS_DEV_EC2 = config('C_AWS_DEV_EC2',default=AWS_EC2_HOST)
AWS_DEV_EC2_IP = re.search('^ec2-(\d{1,3}-\d{1,3}-\d{1,3}-\d{1,3})(.+)',AWS_DEV_EC2).group(1).replace('-','.')
AWS_DEV_DOMAIN = config('C_AWS_DEV_DOMAIN',default='www.fastsimplesocial.com')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

###
if DEBUG:
    pass
else:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

###

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR,'static/js','serviceworker.js')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

IPSTACK_API_ACCESS_KEY = config('C_ipstack_API_ACCESS_KEY')
GOOGLE_MAPS_API_KEY = config('Google_Maps_API_Key')

#ALLOWED_HOSTS = [AWS_EC2_HOST,AWS_EC2_IP,'www.fastsimplesocial.com']
ALLOWED_HOSTS = ['www.fastsimplesocial.com','fastsimplesocial.com','localhost']
ALLOWED_HOSTS += [AWS_EC2_HOST,AWS_EC2_IP,AWS_DEV_EC2,AWS_DEV_EC2_IP,AWS_DEV_DOMAIN,]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.postgres',
    'admin_honeypot',
    'pwa',
#    'django_warrant',
    'datetimepicker',
    'widget_tweaks',
    'django_misaka',
    'crispy_forms' ,
    'bootstrap3',
    'storages',
    'accounts',
    'questions',
    'groups',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'myproject.TimezoneMiddleware.TimezoneMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',    
]

##  A project can have many urls.py distributed among the apps. But Django needs a url.py to use 
## as a starting point. This special urls.py is called root URLconf. 
## It is defined in the settings.py file.
ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),os.path.join(BASE_DIR, 'templates', 'allauth')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
        		'django.template.context_processors.media',                
###                'django.core.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

################################################################################################
AUTH_USER_MODEL = 'accounts.User'

################################################################################################
## Django-Allauth setup
AUTHENTICATION_BACKENDS = [
  # Default backend -- used to login by username in Django admin
#    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
    ]
INSTALLED_APPS += (
    # The Django sites framework is required
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # Login via Google
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
   'allauth.socialaccount.providers.facebook',
    

)
 
SITE_ID = 3

ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_QUERY_EMAIL = True

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

LOGIN_REDIRECT_URL = 'home'
###################################
##Facebook 
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', ],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.12',
    }
}


################################################################################################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('AWS_RDS_DB_NAME'),
        'USER': config('AWS_RDS_DB_USER'),
        'PASSWORD': config('AWS_RDS_DB_PASS'),
        'HOST': config('AWS_RDS_DB_HOST'),
        'PORT': config('AWS_RDS_DB_PORT'),

    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = 'home'


LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'accounts:login'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

########################## E M A I L ##########################################################
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

DEFAULT_FROM_EMAIL = 'FastSimpleSocial <noreply@fastsimplesocial.com>'
EMAIL_SUBJECT_PREFIX = '[FastSimpleSocial] '

SERVER_EMAIL = 'fastsimplesocial@gmail.com'

ADMINS = [
    ('Admin1', SERVER_EMAIL),
]
 
MANAGERS = ADMINS

FEEDBACK_MAIL = 'fastsimplesocial@gmail.com'
####################################################################################

########################## A W S ##########################################################
AWS_S3_OBJECT_PARAMETERS = {
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'CacheControl': 'max-age=94608000',
}
AWS_DEFAULT_ACL = None
###
AWS_S3_REGION_NAME = 'eu-west-1'  
AWS_STORAGE_BUCKET_NAME = config('C_AWS_STORAGE_BUCKET_NAME')
###
AWS_ACCESS_KEY_ID = config('C_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('C_AWS_SECRET_ACCESS_KEY')
AWS_LOCATION = config('C_AWS_LOCATION') 

####AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_CUSTOM_DOMAIN = 's3-{}.amazonaws.com/{}'.format(AWS_S3_REGION_NAME , AWS_STORAGE_BUCKET_NAME) 

###
# Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# you run `collectstatic`).
#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STATIC_LOCATION = 's3-{}.amazonaws.com/{}'.format(AWS_S3_REGION_NAME , AWS_STORAGE_BUCKET_NAME)  
#https://s3-eu-west-1.amazonaws.com/simplesocialproject/static/js/scripts/script_delete_answer.js

# CLOUDFRONT_DOMAIN = config('CLOUDFRONT_DOMAIN')
# CLOUDFRONT_ID = config('CLOUDFRONT_ID')
# AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN')
##############################
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
####################################################################################


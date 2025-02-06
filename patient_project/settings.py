"""
Django settings for lms_project project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv # type: ignore
from datetime import timedelta

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DOMAIN = os.getenv("DOMAIN")
MEDIA_FULL_URL = f"{DOMAIN}"

DEFAULT_PAGE_SIZE = 5
MAXIMUM_PAGE_SIZE = 50
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')
JWT_AUDIENCE = os.environ.get('JWT_AUDIENCE')
JWT_ISSUER = os.environ.get('JWT_ISSUER')



# EMAIL settings
# EMAIL service credentials
EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")
EMAIL_SENDER_ID = os.getenv("EMAIL_SENDER_ID")
EMAIL_API_URL = os.getenv("EMAIL_API_URL")


JWT_EXPIRATION_MINUTES = os.environ.get("JWT_EXPIRATION_MINUTES")
DEFAULT_PASSWORD_POLICY = os.environ.get("DEFAULT_PASSWORD_POLICY")
DEFAULT_PASSWORD = os.environ.get("DEFAULT_PASSWORD")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
    'corsheaders',
	'drf_yasg',
	'core', 
    'users',
	'auth_service',
    'custom_admin'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'patient_project.urls'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
	"https://patient-care-pied.vercel.app"
]


CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]


CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]



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

WSGI_APPLICATION = 'patient_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': os.environ.get('DB_NAME'),
		'HOST': os.environ.get('DB_HOST'),
		'USER': os.environ.get('DB_USERNAME'),
		'PASSWORD': os.environ.get('DB_PASSWORD'),
		'PORT': os.environ.get('DB_PORT'),
		'OPTIONS': {
			'sslmode':'require',
			'sslcert':os.environ.get('SSL_CERT')
		},
	}
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True

DATETIME_FORMAT = 'Y-m-d'

USE_L10N = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

FORCE_SCRIPT_NAME = '/api/v1'

REST_FRAMEWORK = {
	"EXCEPTION_HANDLER": "auth_service.exceptions.custom_exception_handler.custom_exception_handler",
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'auth_service.middlewares.JWTAuthentication',
	),
}


AUTH_USER_MODEL='users.User'

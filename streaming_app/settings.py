from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(+^=vr!m(7iqrpry-pk#(y9^b67$*ira2j2ds+vjcs9v!k9ek2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'data_ingress.apps.DataIngressConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'streaming_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
            ],
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

WSGI_APPLICATION = 'streaming_app.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'streaming_app',  # The name of the database you created
        'USER': 'myuser',  # The PostgreSQL user you created
        'PASSWORD': 'mypassword',  # The password you set for the user
        'HOST': 'localhost',  # Replace with WSL IP address
        'PORT': '5432',  # Default PostgreSQL port
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

########################################## LOGGER SETTINGS ##########################################
# Define the path to the file you want to clear
streaming_app_log_file_name = "streaming_app.log"
data_generation_log_file_name = "data_generation.log"
STREAMING_APP_LOG_FILE = os.path.join(BASE_DIR, streaming_app_log_file_name)
DATA_GENERATION_LOG_FILE = os.path.join(BASE_DIR, data_generation_log_file_name)


def clear_file(filename):
    with open(filename, 'w') as file:
        pass

clear_file(STREAMING_APP_LOG_FILE)
clear_file(DATA_GENERATION_LOG_FILE)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # 'django_file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'filename': os.path.join(BASE_DIR, 'django_debug.log'),
        #     'formatter': 'verbose',
        # },
        'streaming_app_log_file_name': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, streaming_app_log_file_name),  # Custom log file
            'formatter': 'verbose',
        },
        'data_generation_log_file_name': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, data_generation_log_file_name),  # Custom log file
            'formatter': 'verbose',
        },

    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'loggers': {
        # 'django': {
        #     'handlers': ['django_file'],
        #     'level': 'DEBUG',
        #     'propagate': False,
        # },
        'streaming_app': {
            'handlers': ['streaming_app_log_file_name'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'data_generation': {
            'handlers': ['data_generation_log_file_name'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
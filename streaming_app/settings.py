import subprocess
import time
from pathlib import Path
import os
from data_ingress.container_control.postgres_docker_service_controller import postgres_docker_service_controller

from django.conf import settings

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
    
    'data_ingress.apps.DataIngressConfig',
    'data_display.apps.DataDisplayConfig',
    'data_analysis.apps.DataAnalysisConfig',
    'rest_framework'
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
        'NAME': 'streaming_app',  # The name of the database_handling you created
        'USER': 'myuser',  # The PostgreSQL user you created
        'PASSWORD': 'mypassword',  # The password you set for the user
        'HOST': '127.0.0.1',  # Replace with WSL IP address
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

streaming_app_log_file_name = "streaming_app.log"
STREAMING_APP_LOG_FILE = os.path.join(BASE_DIR, streaming_app_log_file_name)


def clear_file(filename):
    with open(filename, 'w') as file:
        pass

clear_file(STREAMING_APP_LOG_FILE)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'streaming_app_log_file_name': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, streaming_app_log_file_name),  # Custom log file
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
        'streaming_app': {
            'handlers': ['streaming_app_log_file_name'],
            'level': 'DEBUG',
            'propagate': False,
        }
    },
}

### ELK ###

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'
    },
}


def is_wsl_running():
    result = subprocess.run(['tasklist'], stdout=subprocess.PIPE, text=True)
    if 'vmmem' in result.stdout or 'wslhost.exe' in result.stdout:
        return True
    else:
        return False

def start_db():
    is_postgres_docker_service_running: bool = postgres_docker_service_controller.get_postgres_docker_service_status()
    if not is_postgres_docker_service_running:
        print("PostrgeSQL docker container is not running - starting...")
        postgres_docker_service_controller.start_postgres_docker_service()


def wait_for_docker(timeout=300, interval=3):
    start_time = time.time()
    while True:
        try:
            print('Waiting for Docker!')
            command = ['wsl', '-e', 'bash', '-c', 'docker']
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                print("Docker is UP!")
                return True
            else:
                print(f"Waiting for Docker... Error: {stderr.decode('utf-8')}")
        except FileNotFoundError:
            print("Docker command not found. Make sure Docker is installed and added to PATH.")
            return False
        if time.time() - start_time > timeout:
            print("Timeout reached. Docker did not become operational.")
            return False
        print("...and waiting...")
        time.sleep(interval)


def start_wsl_background():
    print("Checking whether WSL is running...")
    if is_wsl_running:
        print("Not running - starting...")
        try:
            subprocess.Popen("wsl", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("WSL started in the background.")
        except Exception as e:
            print(f"Failed to start WSL: {e}")
    else:
        print("WSL is running...")

start_wsl_background()
wait_for_docker()
start_db()
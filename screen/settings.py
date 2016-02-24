import dj_database_url
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = os.environ.get('ENV', 'debug') != 'live'
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django_rq',
    'storages',
    'opbeat.contrib.django',
    'screen.wall'
)

MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware'
)

ROOT_URLCONF = 'screen.urls'
SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.tz'
            ],
            'debug': True
        }
    }
]

WSGI_APPLICATION = 'screen.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
# Parse database configuration from $DATABASE_URL
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///%s' % os.path.join(BASE_DIR, 'db.sqlite')
    )
}

if not DEBUG:
    DATABASES['default']['ENGINE'] = 'django_postgrespool'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static asset configuration
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET')
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')
AWS_PRELOAD_METADATA = True
S3DIRECT_REGION = 'eu-west-1'
STORE_ASSETS_ROOT = 'storefiles'

if not DEBUG:
    DEFAULT_FILE_STORAGE = 'screen.s3.MediaRootS3BotoStorage'
    STATICFILES_STORAGE = 'screen.s3.StaticRootS3BotoStorage'

MEDIA_URL = DEBUG and '/media/' or '//%s/media/' % AWS_S3_CUSTOM_DOMAIN
STATIC_URL = DEBUG and '/static/' or ('//%s/static/' % AWS_S3_CUSTOM_DOMAIN)

# S3 direct upload
S3DIRECT_DESTINATIONS = {
    'podcast_episodes': (
        'media/podcasts/episodes',
        lambda u: u.is_staff,
        ('audio/mp3', 'audio/mpeg', 'video/mp4')
    )
}

# Thumbnails
THUMBNAIL_FORMAT = 'PNG'
THUMBNAIL_DEBUG = DEBUG

# Domain
DOMAIN = os.environ.get('DOMAIN', 'localhost')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'rq_console': {
            'format': '%(asctime)s %(message)s',
            'datefmt': '%H:%M:%S'
        }
    },
    'handlers': {
        'rq_console': {
            'level': 'DEBUG',
            'class': 'rq.utils.ColorizingStreamHandler',
            'formatter': 'rq_console',
            'exclude': ['%(asctime)s']
        },
    },
    'loggers': {
        'rq.worker': {
            'handlers': ['rq_console'],
            'level': 'DEBUG'
        }
    }
}

# Opbeat
OPBEAT = {
    'ORGANIZATION_ID': os.environ.get('OPBEAT_ORGANIZATION_ID'),
    'APP_ID': os.environ.get('OPBEAT_APP_ID'),
    'SECRET_TOKEN': os.environ.get('OPBEAT_SECRET_TOKEN')
}

# Caching
def get_cache():
    try:
        os.environ['MEMCACHE_SERVERS'] = \
            os.environ['MEMCACHEDCLOUD_SERVERS'].replace(',', ';')

        os.environ['MEMCACHE_USERNAME'] = os.environ['MEMCACHEDCLOUD_USERNAME']
        os.environ['MEMCACHE_PASSWORD'] = os.environ['MEMCACHEDCLOUD_PASSWORD']

        return {
            'default': {
                'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
                'TIMEOUT': 500,
                'BINARY': True,
                'OPTIONS': {
                    'tcp_nodelay': True
                }
            }
        }
    except:
        return {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
            }
        }

CACHES = get_cache()

# Twitter
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')

# Instagram
INSTAGRAM_ACCESS_TOKEN = os.environ.get('INSTAGRAM_ACCESS_TOKEN')
INSTAGRAM_CLIENT_SECRET = os.environ.get('INSTAGRAM_CLIENT_SECRET')

# Redis queue
RQ_QUEUES = {
    'default': {
        'URL': os.getenv('REDIS_URL', 'redis://localhost:6379'),
        'DB': 0,
        'DEFAULT_TIMEOUT': 500
    }
}

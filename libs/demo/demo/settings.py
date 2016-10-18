"""
Django settings for demo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 子系统使用自己的channel conf
from any_config.channels import ChannelConf as CHANNEL_CONF

# logger config: from commonlibs
from djangos.config.logger_conf import *
# 重新更新所有handlers的filename，因为LOGGING是个DICT，在logger_conf内已经创建成功，需要再次更新
LOG_ROOT = BASE_DIR
for key, handler in LOGGING['handlers'].items():
    if handler.get('filename', None):
        handler['filename'] = os.path.join(LOG_ROOT, "logs", os.path.basename(handler['filename']))

# email config: from commonlibs
from djangos.config.sender_conf import (EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER,
                                        EMAIL_HOST_PASSWORD, DEFAULT_FROM_EMAIL,
                                        EMAIL_USE_SSL, EMAIL_USE_TLS, EMAIL_TIMEOUT)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n8&qb9o88(c__56*h4(fm5+c9d2h%0ese625@r9kz694b^f-_@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []
from config.version import VERSION as VER, BUILD

VERSION = "%s-%s" % (VER, BUILD)

# Application definition

INSTALLED_APPS = (
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'djangos.middleware.request_init.RequestInitMiddleware',
    'djangos.middleware.accesslog.AccessLogMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'demo.urls'

WSGI_APPLICATION = 'demo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# DATABASES = {
# 'default': {
# 'ENGINE': 'django.db.backends.sqlite3',
# 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
# }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


CACHES = {
    "default": {
        "BACKEND": "libs.djangos.cache.sentinel_backend.SentinelRedisCache",
        "LOCATION": SENTINEL_LOCATION,
        "TIMEOUT": 300,
        "KEY_PREFIX": KEY_PREFIX,
        'OPTIONS': {
            'MASTER_NAME': 'mymaster',
            'DB': 0,
            'POOL_KWARGS': {
                'socket_timeout': 0.3,
                'socket_connect_timeout': 0.3
            },
        }
    },
    "session": {
        "BACKEND": "libs.djangos.cache.sentinel_backend.SentinelRedisCache",
        "LOCATION": SENTINEL_LOCATION,
        "TIMEOUT": SESSION_COOKIE_AGE,
        "KEY_PREFIX": '%s:%s' % (KEY_PREFIX, 'session'),
        'OPTIONS': {
            'MASTER_NAME': 'mymaster',
            'DB': 1,
            'SERIALIZER': 'libs.djangos.misc.JsonSerializer',  # 默认pickle
            'POOL_KWARGS': {
                'socket_timeout': 0.3,
                'socket_connect_timeout': 0.3
            },
        }
    },
    'systemconfig': {
        "BACKEND": "libs.djangos.cache.combo_backend.ComboCache",
        "LOCATION": SENTINEL_LOCATION,
        'LOCAL_CACHE': 'systemconfig-local',
        "TIMEOUT": 3600,
        "KEY_PREFIX": '%s:%s' % (KEY_PREFIX, 'sysconf'),
        'OPTIONS': {
            'MASTER_NAME': 'mymaster',
            'DB': 2,
            'POOL_KWARGS': {
                'socket_timeout': 0.3,
                'socket_connect_timeout': 0.3
            },
        }
    },
    'systemconfig-local': {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "systemconfig-local",
        "TIMEOUT": 60 * 2,  # local cache timetout
        "KEY_PREFIX": '%s:%s' % (KEY_PREFIX, 'sysconf'),
        'OPTIONS': {
            'MAX_ENTRIES': 30000,  # local cache max entries
        }
    },
    'account': {
        "BACKEND": "libs.djangos.cache.sentinel_backend.SentinelRedisCache",
        "LOCATION": SENTINEL_LOCATION,
        "TIMEOUT": 3600 * 24,
        "KEY_PREFIX": '%s:%s' % (KEY_PREFIX, 'account'),
        'OPTIONS': {
            'MASTER_NAME': 'mymaster',
            'DB': 3,
            'POOL_KWARGS': {
                'socket_timeout': 0.3,
                'socket_connect_timeout': 0.3
            },
        }
    },
    'httpclient_protect': {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "httpclient_protect",
        "TIMEOUT": 60 * 2,  # local cache timetout
        "KEY_PREFIX": '%s:%s' % (KEY_PREFIX, 'httpclient'),
        'OPTIONS': {
            'MAX_ENTRIES': 30000,  # local cache max entries
        }
    },
}

HTTPCLIENT_PROTECT_RATE = (60, 100, 3)  # RequestClient使用，表示#60#s时间内错误达到#100#次，就再接下来#3#s时间内不访问
# raven配置，兼容没有装raven的情况
try:
    import raven
    import logging
    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)
    RAVEN_CONFIG = {
        #'dsn': 'http://public:secret@example.com/1',  # TODO
    }

    class SkipProjectRelatedFilter(logging.Filter):
        '''sentry处理ERROR级别以上日志，过滤项目内记录的syslogger.error，只保留syslogger.exception
        '''
        def filter(self, record):
            if record.name in (PROJECT_INFO_LOG, PROJECT_ERROR_LOG):
                return False
            else:
                return True

    LOGGING['filters'].setdefault('skip_project_related', {
        '()': SkipProjectRelatedFilter
    })
    LOGGING['handlers'].setdefault('sentry', {
        'level': 'ERROR',
        'filters': ['skip_project_related'],
        'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
    })
    LOGGING['loggers'].setdefault('', {
        'handlers': ['sentry'],
        'level': 'ERROR',
        'propagate': False,
    })
except ImportError:
    pass


# import local settings
try:
    from .local_settings import *
except ImportError:
    pass

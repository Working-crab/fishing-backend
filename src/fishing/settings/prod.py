from fishing.settings.base import *

DEBUG = False

ALLOWED_HOSTS = [
    "91.200.146.5",
    "13.48.31.237",
    "diwos.ru",
    "www.diwos.ru",
]
CSRF_TRUSTED_ORIGINS = [
    "http://diwos.ru",
    "http://www.diwos.ru",
    "https://diwos.ru",
    "https://www.diwos.ru",
]

STATIC_ROOT = '/var/www/fishing/django/'

MEDIA_ROOT = '/var/www/fishing/uploads/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'service': 'my_postgres',
            'passfile': '/home/ubuntu/.pgpass',
        },
    }
}

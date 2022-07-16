from fishing.settings.base import *

DEBUG = False

ALLOWED_HOSTS = [
    "13.48.31.237",
    "diwos.ru",
]

STATIC_ROOT = '/var/www/fishing/django/'

MEDIA_ROOT = '/var/www/fishing/uploads/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/data/mysql.cnf',
        },
    }
}

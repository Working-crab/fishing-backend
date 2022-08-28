from fishing.settings.base import *

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

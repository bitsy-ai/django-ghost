from .test import *

DATABASES = {"default": {
    "USER": "debug",
    "ENGINE": "django.db.backends.postgresql",
    "PASSWORD": "debug",
    "HOST": "localhost",
    "PORT": 5432,
    "NAME": "django"
}}

GHOST_API_URL = "http://localhost:2368"

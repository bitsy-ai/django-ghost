import os
import environ

env = environ.Env()


# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "django_ghost.tests.apps.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
# WSGI_APPLICATION = "config.wsgi.application"
# ASGI_APPLICATION = "config.asgi.application"

DEBUG = True
TIME_ZONE = "UTC"
USE_TZ = True
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

DATABASES = {
    "default": {
        "USER": "debug",
        "ENGINE": "django.db.backends.postgresql",
        "PASSWORD": "debug",
        "HOST": "postgres",
        "PORT": 5432,
        "NAME": "django",
    }
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ]
        },
    }
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django_ghost.tests.apps.testapp",
    "django_ghost",
]

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SECRET_KEY = "unGPquS03pKnzfQblEpV9KQtFRwgkGaNyS5Ijra7JkM56P9xbE"

AUTH_USER_MODEL = "testapp.CustomUser"


# the following values are stored in .ghost/data/ghost-test.db (sqlite3) and are intended for test purposes only
GHOST_ADMIN_EMAIL = "admin@test.com"
GHOST_ADMIN_PASSWORD = "testing1234"
GHOST_NEWSLETTER_IDS = ["63768218d04dac0001bfc2e0"]
GHOST_CONTENT_API_KEY = "61c3677e599df7938eccab219b"
GHOST_ADMIN_API_APP_ID = "63768243d04dac0001bfc4e3"
GHOST_ADMIN_API_APP_SECRET = (
    "b823dbdaa262620f9f94f026298873d03534fed5ae39024019479519471b37e3"
)
GHOST_API_URL = "http://ghost:2368"

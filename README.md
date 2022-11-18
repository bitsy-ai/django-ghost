# Django Ghost

[![image](https://img.shields.io/pypi/v/django-ghost)](https://pypi.org/project/django-ghost/) [![image](https://img.shields.io/pypi/pyversions/django-ghost)](https://pypi.org/project/django-ghost/) [![image](https://img.shields.io/pypi/djversions/django-ghost)](https://pypi.org/project/django-ghost/) [![image](https://img.shields.io/pypi/wheel/django-ghost)](https://pypi.org/project/django-ghost/) [![image](https://img.shields.io/discord/773452324692688956)](https://discord.gg/Y848Hq9xKh) [![image](https://img.shields.io/github/workflow/status/bitsy-ai/django-ghost/Test)](https://github.com/bitsy-ai/django-ghost) [![image](https://img.shields.io/codecov/c/github/bitsy-ai/django-ghost)](https://github.com/bitsy-ai/django-ghost) [![image](https://img.shields.io/github/release-date-pre/bitsy-ai/django-ghost)](https://github.com/bitsy-ai/django-ghost)

Automatically sync a Django model with Ghost's member model. [Ghost is a CMS for content creators.](https://ghost.org/)

1. `pip install django-ghost` 

2.  Add to your INSTALLED_APPS settings:

        INSTALLED_APPS = [
            "django_ghost",
        ]

3.  Run `python manage.py migrate` to create the NATS organizationals
    models

Contributor's Guide
====================

1.  Create a development environment (requires docker & docker-compose):

        make docker-up

2.  Run tests and generate a coverage report:

        make pytest

3.  Run `black` linter:

        make lint


Settings
===========

### Basic Settings
`GHOST_MEMBER_MODEL` (default: return value of `django.contrib.auth.get_user_model()` )
`GHOST_NEWSLETTER_IDS` (default: []) - newsletter ids to subscribe to
`GHOST_ADMIN_API_APP_ID`
`GHOST_ADMIN_API_APP_SECRET`
`GHOST_API_URL` (default: `"http://localhost` or `$GHOST_API_URL` environment var)

from django.apps import AppConfig


class DjangoGhostConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_ghost"

    def ready(self):
        try:
            import django_ghost.signals  # noqa F401
        except ImportError:
            pass

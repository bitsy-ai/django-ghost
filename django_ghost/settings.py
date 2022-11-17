from django.db.models import Model
from django.conf import settings
from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured


class DjangoGhostSettings:
    def member_model_string(self) -> str:
        return getattr(settings, "GHOST_MEMBER_MODEL", settings.AUTH_USER_MODE)

    def member_model(self) -> Model:
        model_name = self.get_model_member_string()
        try:
            model = django_apps.get_model(model_name)
            return model
        except LookupError:
            raise ImproperlyConfigured(
                "GHOST_MEMBER_MODEL refers to model '{model}' "
                "that has not been installed.".format(model=model_name)
            )


django_ghost_settings = DjangoGhostSettings()

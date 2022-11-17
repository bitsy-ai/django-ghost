from datetime import datetime as date

from django.db.models import Model
from django.conf import settings
from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured


class DjangoGhostSettings:
    def get_member_model_string(self) -> str:
        return getattr(settings, "GHOST_MEMBER_MODEL", settings.AUTH_USER_MODEL)

    def get_member_model(self) -> Model:
        model_name = self.get_member_model_string()
        try:
            model = django_apps.get_model(model_name)
            return model
        except LookupError:
            raise ImproperlyConfigured(
                "GHOST_MEMBER_MODEL refers to model '{model}' "
                "that has not been installed.".format(model=model_name)
            )

    def get_ghost_admin_app_id(self) -> str:
        return getattr(settings, "GHOST_ADMIN_APP_ID")

    def get_ghost_admin_app_secret(self) -> str:
        return getattr(settings, "GHOST_ADMIN_APP_SECRET")

    def get_ghost_admin_api_auth_header(self) -> str:

        app_id = self.get_ghost_admin_app_id()
        secret = self.get_ghost_admin_app_secret()

        # Prepare header and payload
        iat = int(date.now().timestamp())
        header = {"alg": "HS256", "typ": "JWT", "kid": app_id}
        payload = {"iat": iat, "exp": iat + 5 * 60, "aud": "/admin/"}

        # Create the token (including decoding secret)
        key = bytes.fromhex(secret)
        token = jwt.encode(payload, key, algorithm="HS256", headers=header)  # type: ignore


django_ghost_settings = DjangoGhostSettings()

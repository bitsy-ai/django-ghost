from typing import List, TypedDict

from datetime import datetime as date
import jwt

from django.db.models import Model
from django.conf import settings
from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured


class GhostLabel(TypedDict):
    name: str
    slug: str


DEFAULT_GHOST_LABEL = GhostLabel(name="django_ghost", slug="django_ghost")


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

    def get_ghost_newsletter_ids(self) -> List[str]:
        return getattr(settings, "GHOST_NEWSLETTER_IDs", [])

    def get_ghost_member_labels(self) -> List[GhostLabel]:
        return getattr(settings, "GHOST_MEMBER_LABELS", [DEFAULT_GHOST_LABEL])

    def get_ghost_admin_app_id(self) -> str:
        try:
            result = getattr(settings, "GHOST_ADMIN_API_APP_ID")
            if result is None:
                raise AttributeError
            return result
        except AttributeError:
            raise ImproperlyConfigured(
                "GHOST_ADMIN_API_APP_ID setting is required to use django-ghost. Please add GHOST_ADMIN_API_APP_ID to settings.py"
            )

    def get_ghost_admin_app_secret(self) -> str:
        try:
            result = getattr(settings, "GHOST_ADMIN_API_APP_SECRET")
            if result is None:
                raise AttributeError
            return result
        except AttributeError:
            raise ImproperlyConfigured(
                "GHOST_ADMIN_API_APP_SECRET setting is required to use django-ghost. Please add GHOST_ADMIN_API_APP_SECRET to settings.py"
            )

    def get_ghost_url(self) -> str:
        try:
            return getattr(settings, "GHOST_API_URL")
        except AttributeError:
            raise ImproperlyConfigured(
                "GHOST_API_URL setting is required to use django-ghost. Please add GHOST_API_URL to settings.py"
            )

    def get_ghost_admin_api_auth_header(self) -> str:

        app_id = self.get_ghost_admin_app_id()
        secret = self.get_ghost_admin_app_secret()

        # Prepare header and payload
        iat = int(date.now().timestamp())
        header = {"alg": "HS256", "typ": "JWT", "kid": app_id}
        payload = {"iat": iat, "exp": iat + 5 * 60, "aud": "/admin/"}

        # Create the token (including decoding secret)
        key = bytes.fromhex(secret)

        token = jwt.encode(payload, key, algorithm="HS256", headers=header)
        headers = {"Authorization": "Ghost {}".format(token)}
        return headers

    def get_ghost_admin_members_api_url(self):
        return f"{self.get_ghost_url()}/ghost/api/admin/members/"


django_ghost_settings = DjangoGhostSettings()

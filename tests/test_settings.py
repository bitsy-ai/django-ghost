"""
dj-stripe Migrations Tests
"""
import pytest

import requests
from django.test import TestCase, override_settings
from django.core.exceptions import ImproperlyConfigured
from django_ghost.settings import django_ghost_settings


class TestSettings(TestCase):
    def setUp(self):
        return super().setUp()

    @override_settings(GHOST_MEMBER_MODEL="invalid.foo")
    def test_invalid_ghost_member_model(self):
        with pytest.raises(ImproperlyConfigured):
            django_ghost_settings.get_member_model()

    def test_missing_ghost_api_key(self):
        with pytest.raises(ImproperlyConfigured):
            django_ghost_settings.get_ghost_admin_api_auth_header()

    @override_settings(
        GHOST_ADMIN_API_APP_ID="app_id", GHOST_ADMIN_API_APP_SECRET="secret"
    )
    def test_ghost_admin_api_auth_header(self):
        header = django_ghost_settings.get_ghost_admin_api_auth_header()
        url = django_ghost_settings.get_ghost_admin_members_api_url()
        res = requests.get(url)

        assert res.status_code == 403

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

    @override_settings(GHOST_SYNC_MODEL="invalid.foo")
    def test_invalid_GHOST_SYNC_MODEL(self):
        with pytest.raises(ImproperlyConfigured):
            django_ghost_settings.get_member_model()

    @override_settings(GHOST_ADMIN_API_APP_ID=None, GHOST_ADMIN_API_APP_SECRET=None)
    def test_missing_ghost_api_key(self):
        with pytest.raises(ImproperlyConfigured):
            django_ghost_settings.get_ghost_admin_app_secret()

    @override_settings(
        # test are invalid keys
        GHOST_ADMIN_API_APP_ID="13768243d04dac0001bfc4e3",
        GHOST_ADMIN_API_APP_SECRET="a823dbdaa262620f9f94f026298873d03534fed5ae39024019479519471b37e3",
    )
    def test_invalid_ghost_admin_api_auth_header(self):
        headers = django_ghost_settings.get_ghost_admin_api_auth_header()
        url = django_ghost_settings.get_ghost_admin_members_api_url()
        res = requests.get(url, headers=headers)

        assert res.status_code == 401

    def test_valid_ghost_admin_api_auth_header(self):
        headers = django_ghost_settings.get_ghost_admin_api_auth_header()
        url = django_ghost_settings.get_ghost_admin_members_api_url()
        res = requests.get(url, headers=headers)

        assert res.status_code == 200

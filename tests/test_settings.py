"""
dj-stripe Migrations Tests
"""
import pytest
from django.test import TestCase, override_settings
from django.core.exceptions import ImproperlyConfigured
from django_ghost.settings import django_ghost_settings


class TestSettings(TestCase):
    def setUp(self):
        return super().setUp()

    @override_settings(GHOST_MEMBER_MODELL="invalid")
    def test_invalid_ghost_member_model(self):
        with pytest.raises(ImproperlyConfigured):
            django_ghost_settings.get_member_model()

    # @override_settings(NATS_ROBOT_APP_MODEL="invalid")
    # def test_invalid_robot_app_model(self):
    #     with pytest.raises(ImproperlyConfigured):
    #         nats_nkeys_settings.get_nats_robot_app_model()

    # def test_defaults_valid(self):
    #     from django_nats_nkeys.models import (
    #         NatsOrganization,
    #         NatsOrganizationUser,
    #         NatsOrganizationOwner,
    #         NatsOrganizationApp,
    #         NatsRobotApp,
    #     )

    #     assert nats_nkeys_settings.get_nats_user_model() is NatsOrganizationUser
    #     assert nats_nkeys_settings.get_nats_account_model() is NatsOrganization
    #     assert (
    #         nats_nkeys_settings.get_nats_organization_owner_model()
    #         is NatsOrganizationOwner
    #     )
    #     assert (
    #         nats_nkeys_settings.get_nats_organization_app_model() is NatsOrganizationApp
    #     )

    #     assert nats_nkeys_settings.get_nats_app_models() == [
    #         NatsOrganizationApp,
    #         NatsRobotApp,
    #     ]

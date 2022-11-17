from uuid import uuid4
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django_ghost.settings import django_ghost_settings
from django_ghost.models import GhostMember

UserModel = get_user_model()


class TestSignals(TestCase):
    def setUp(self):
        return super().setUp()

    def test_new_member_create(self):
        email = f"{uuid4()}@test.com"
        user = UserModel.objects.create(email=email)
        ghost_member = GhostMember.objects.get(email=email)
        assert user.email == ghost_member.email

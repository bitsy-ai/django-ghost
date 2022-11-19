from uuid import uuid4
from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model
from django_ghost.models import GhostMember


User = get_user_model()


class TestCommand(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.email = f"{uuid4()}@test.com"
        self.user = User.objects.create(
            email=self.email, password="testing1234", is_superuser=True
        )

    def test_sync_by_email(self):
        call_command("django_ghost_sync", "--email", self.user.email)
        ghost_member = GhostMember.objects.get(email=self.user.email)
        assert ghost_member is not None

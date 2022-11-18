from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model
from django_ghost.models import GhostMember


User = get_user_model()


class TestCommand(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create(
            email="admin@test.com", password="testing1234", is_superuser=True
        )

    def test_sync(self):
        call_command("django_ghost_sync")
        ghost_member = GhostMember.objects.get(email=self.user.email)
        assert ghost_member is not None

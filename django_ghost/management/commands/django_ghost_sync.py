from click import BaseCommand
from django.core.management.base import BaseCommand

from django_ghost.services import update_or_create_ghost_member
from django_ghost.settings import django_ghost_settings

GhostMemberModel = django_ghost_settings.get_sync_model()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        members_to_sync = GhostMemberModel.objects.all()

        for member in members_to_sync:
            update_or_create_ghost_member(member)

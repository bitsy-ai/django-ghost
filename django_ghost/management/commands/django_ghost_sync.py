from click import BaseCommand
from django.core.management.base import BaseCommand, CommandParser

from django_ghost.services import update_or_create_ghost_member
from django_ghost.settings import django_ghost_settings

GhostSyncModel = django_ghost_settings.get_sync_model()


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:

        parser.add_argument(
            "--email",
            type=str,
            required=False,
            help="Limit to a specific email address",
        )
        parser.add_argument(
            "--limit",
            type=int,
            required=False,
            help="Limit number of matched emails",
        )

    def handle(self, *args, **kwargs):

        email = kwargs.get("email")
        limit = kwargs.get("limit")
        members_to_sync = GhostSyncModel.objects.all()

        if email is not None:
            return update_or_create_ghost_member(email)

        members_to_sync = GhostSyncModel.objects.filter(email=email).all()
        if limit is not None:
            members_to_sync = members_to_sync[:limit]

        for member in members_to_sync:
            update_or_create_ghost_member(member.email)

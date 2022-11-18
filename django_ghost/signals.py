import logging
import requests
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from .settings import django_ghost_settings
from .models import GhostMember
from .services import update_or_create_ghost_member

GhostMemberModel = django_ghost_settings.get_sync_model()

logger = logging.getLogger(__name__)


@receiver(post_save, sender=GhostMemberModel)
def ghost_member_create_or_update(
    sender, instance, created, update_fields=None, **kwargs
):

    update_or_create_ghost_member(instance)

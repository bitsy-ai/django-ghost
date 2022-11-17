import logging

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from .settings import django_ghost_settings

GhostMemberModel = django_ghost_settings.get_member_model()

logger = logging.getLogger(__name__)


@receiver(post_save, sender=GhostMemberModel)
def ghost_member_update(sender, instance, created, update_fields=None, **kwargs):
    pass

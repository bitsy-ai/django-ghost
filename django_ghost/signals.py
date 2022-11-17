import logging
import requests
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from .settings import django_ghost_settings
from .models import GhostMember

GhostMemberModel = django_ghost_settings.get_member_model()

logger = logging.getLogger(__name__)


@receiver(post_save, sender=GhostMemberModel)
def ghost_member_update(sender, instance, created, update_fields=None, **kwargs):
    # get authorization headers
    headers = django_ghost_settings.get_ghost_admin_api_auth_header()
    url = django_ghost_settings.get_ghost_admin_members_api_url()

    labels = django_ghost_settings.get_ghost_member_labels()
    newsletters = django_ghost_settings.get_ghost_newsletter_ids()

    body = {"email": instance.email, "labels": labels, "newsletters": newsletters}
    r = requests.post(url, json=body, headers=headers)
    try:
        r.raise_for_status()
    except Exception as e:
        logger.warning(
            {
                "msg": "POST /ghost/api/admin/members/ failed with error",
                "error": e,
            }
        )
    data = r.json()

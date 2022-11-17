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

    body = {
        "members": [
            {"email": instance.email, "labels": labels, "newsletters": newsletters}
        ]
    }
    res = requests.post(url, json=body, headers=headers)
    try:
        res.raise_for_status()
    except Exception as e:
        logger.error(
            {
                "msg": "POST /ghost/api/admin/members/ failed with error",
                "error": e,
            }
        )
        return
    data = res.json()
    for member in data.get("members"):
        try:
            obj = GhostMember.objects.filter(email=member["email"]).first()

            if obj is not None:
                obj.email = member["email"]
                obj.uuid = member["uuid"]
                obj.user = instance
                obj.email_count = member["email_count"]
                obj.email_open_rate = member["email_open_rate"]
                obj.email_opened_count = member["email_opened_count"]
                obj.id = member["id"]
                obj.note = member["note"]
                obj.geolocation = member["geolocation"]
                obj.last_seen_at = member["last_seen_at"]
                obj.created_at = member["created_at"]
                obj.updated_at = member["updated_at"]
                obj.email_count = member["email_count"]
                obj.email_opened_count = member["email_opened_count"]
                obj.email_open_rate = member["email_open_rate"]
                obj.status = member["status"]
                obj.labels = member["labels"]
                obj.subscriptions = member["subscriptions"]
                obj.tiers = member["tiers"]
                obj.newsletters = member["newsletters"]
                obj.save()
            else:
                obj = GhostMember.objects.create(
                    email=member["email"],
                    uuid=member["uuid"],
                    user=instance,
                    email_count=member["email_count"],
                    email_open_rate=member["email_open_rate"],
                    email_opened_count=member["email_opened_count"],
                    id=member["id"],
                    note=member["note"],
                    geolocation=member["geolocation"],
                    last_seen_at=member["last_seen_at"],
                    created_at=member["created_at"],
                    updated_at=member["updated_at"],
                    status=member["status"],
                    subscriptions=member["subscriptions"],
                    tiers=member["tiers"],
                    newsletters=member["newsletters"],
                )
                logger.info(f"Created GhostMember id={obj.id}")
        except Exception as e:
            logger.error(e)
    return data

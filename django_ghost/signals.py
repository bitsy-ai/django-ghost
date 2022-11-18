import logging
import requests
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from .settings import django_ghost_settings
from .models import GhostMember

GhostMemberModel = django_ghost_settings.get_member_model()

logger = logging.getLogger(__name__)


def create_ghost_member(instance: GhostMemberModel):
    """
    instance - instance of model configured in settings.GHOST_MEMBER_MODEL (default: settings.AUTH_USER_MODEL)
    """
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
        GhostMember.objects.create(
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


def update_ghost_member(instance: GhostMemberModel, ghost_member: GhostMember):
    """
    instance - instance of model configured in settings.GHOST_MEMBER_MODEL (default: settings.AUTH_USER_MODEL)
    ghost_member - instance of GhostMember, a different model.

    in retrospect, this naming could be more clear. @todo
    """
    # get authorization headers
    headers = django_ghost_settings.get_ghost_admin_api_auth_header()
    url = f"{django_ghost_settings.get_ghost_admin_members_api_url()}/{ghost_member.id}"

    labels = django_ghost_settings.get_ghost_member_labels()
    newsletters = django_ghost_settings.get_ghost_newsletter_ids()

    needs_update = (
        ghost_member.labels != labels or ghost_member.newsletters != newsletters
    )
    if needs_update is True:
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
            ghost_member.email = member["email"]
            ghost_member.note = member["note"]
            ghost_member.geolocation = member["geolocation"]
            ghost_member.last_seen_at = member["last_seen_at"]
            ghost_member.created_at = member["created_at"]
            ghost_member.updated_at = member["updated_at"]
            ghost_member.labels = member["labels"]
            ghost_member.subscriptions = member["subscriptions"]
            ghost_member.tiers = member["tiers"]
            ghost_member.newsletters = member["newsletters"]
            ghost_member.save()


@receiver(post_save, sender=GhostMemberModel)
def ghost_member_create_or_update(
    sender, instance, created, update_fields=None, **kwargs
):

    # try to get get ghost member by email
    ghost_member = GhostMember.objects.filter(email=instance.email).first()
    if ghost_member is None:
        create_ghost_member(instance)
    else:
        update_ghost_member(instance, ghost_member)

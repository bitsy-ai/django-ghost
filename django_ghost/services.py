from typing import Optional, Dict, Any
import logging
import requests
from .settings import django_ghost_settings
from .models import GhostMember


logger = logging.getLogger(__name__)

GhostSyncModel = django_ghost_settings.get_sync_model()


def get_ghost_member_by_email(email: str) -> Optional[Dict[str, Any]]:
    # get authorization headers
    headers = django_ghost_settings.get_ghost_admin_api_auth_header()
    url = django_ghost_settings.get_ghost_admin_members_api_url()
    filter = f"?filter=email:{email}"
    url = f"{url}{filter}"
    logger.info("Attempting GET %s", url)
    res = requests.get(url, headers=headers)
    logger.info("Received response: %s", res.json())
    data = res.json()
    try:
        res.raise_for_status()
    except Exception as e:
        logger.error(
            {
                "msg": "POST /ghost/api/admin/members/ failed with error",
                "error": e,
                "data": data,
            }
        )
        return
    if len(data.get("members")) > 1:
        logger.warning(
            "Ghost Member API returned more than 1 member matching email=%s data: %s",
            email,
            data,
        )
    elif len(data.get("members")) == 0:
        logger.warning("Ghost Member API returned 0 results for query: %s", url)
        return
    return data.get("members")[0]


def create_ghost_member(email: str):
    # get authorization headers
    headers = django_ghost_settings.get_ghost_admin_api_auth_header()
    url = django_ghost_settings.get_ghost_admin_members_api_url()

    labels = django_ghost_settings.get_ghost_member_labels()
    newsletters = django_ghost_settings.get_ghost_newsletter_ids()

    body = {"members": [{"email": email, "labels": labels, "newsletters": newsletters}]}
    logger.info("Attempting POST %s with body %s", url, body)
    res = requests.post(url, json=body, headers=headers)
    logger.info("Received response: %s", res.json())
    data = res.json()
    try:
        res.raise_for_status()
    except Exception as e:
        logger.error(
            {
                "msg": "POST /ghost/api/admin/members/ failed with error",
                "error": e,
                "data": data,
                "body": body,
            }
        )
        return
    for member in data.get("members"):
        obj = GhostMember.objects.create(
            email=member["email"],
            uuid=member["uuid"],
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
        logger.info("Created %s for %s", obj, member["email"])


def update_ghost_member(email: str, ghost_member: GhostMember, force_update=False):
    """
    instance - instance of model configured in settings.GHOST_SYNC_MODEL (default: settings.AUTH_USER_MODEL)
    ghost_member - instance of GhostMember, a different model.

    in retrospect, this naming could be more clear. @todo
    """
    # get authorization headers
    headers = django_ghost_settings.get_ghost_admin_api_auth_header()
    url = f"{django_ghost_settings.get_ghost_admin_members_api_url()}{ghost_member.id}"

    labels = django_ghost_settings.get_ghost_member_labels()
    newsletters = django_ghost_settings.get_ghost_newsletter_ids()

    needs_update = (
        ghost_member.labels != labels
        or ghost_member.newsletters != newsletters
        or force_update
    )
    if needs_update is True:
        body = {
            "members": [{"email": email, "labels": labels, "newsletters": newsletters}]
        }
        logger.info("Attempting POST %s with body %s", url, body)
        res = requests.post(url, json=body, headers=headers)
        logger.info("Received response: %s", res.json())
        data = res.json()
        try:
            res.raise_for_status()
        except Exception as e:
            logger.error(
                {
                    "msg": "POST /ghost/api/admin/members/ failed with error",
                    "error": e,
                    "data": data,
                    "body": body,
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
            logger.info("Updated %s for %s", ghost_member, member["email"])


def update_or_create_ghost_member(email: str):
    """
    instance - instance of model configured in settings.GHOST_SYNC_MODEL (default: settings.AUTH_USER_MODEL)
    """
    # try to get get django ghost member model by email
    django_ghost_member = GhostMember.objects.filter(email=email).first()

    # try to get ghost member data by email
    ghost_member = get_ghost_member_by_email(email)

    # create both models
    if ghost_member is None and django_ghost_member is None:
        create_ghost_member(email)
    # create Ghost model (force_update=True), update Django model
    elif django_ghost_member is not None and ghost_member is None:
        update_ghost_member(email, django_ghost_member, force_update=True)
    else:
        update_ghost_member(email, django_ghost_member)

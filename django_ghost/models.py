from django.db import models
from .settings import django_ghost_settings


class GhostMember(models.Model):
    user = models.ForeignKey(
        django_ghost_settings.get_member_model_string(), on_delete=models.CASCADE
    )
    email = models.EmailField()
    id = models.CharField(max_length=255, primary_key=True)
    uuid = models.UUIDField()
    name = models.CharField(max_length=255, null=True)
    note = models.CharField(max_length=255, null=True)
    geolocation = models.CharField(max_length=255, null=True)

    last_seen_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    email_count = models.IntegerField()
    email_opened_count = models.IntegerField()
    email_open_rate = models.CharField(null=True, max_length=128)
    status = models.CharField(max_length=128)

    labels = models.JSONField(default=list)
    subscriptions = models.JSONField(default=list)
    tiers = models.JSONField(default=list)
    newsletters = models.JSONField(default=list)

from django.db import models
from django.conf import settings


class GhostMember(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField()
    id = models.CharField(max_length=255, primary_key=True)
    uuid = models.UUIDField()
    name = models.CharField(max_length=255)
    note = models.CharField(max_length=255)
    geolocation = models.CharField(max_length=255)

    last_seen_at = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    email_count = models.IntegerField()
    email_opened_count = models.IntegerField()
    email_open_rate = models.CharField(null=True, max_length=128)
    status = models.CharField(max_length=128)

    labels = models.JSONField()
    subscriptions = models.JSONField()
    tiers = models.JSONField()
    newsletters = models.JSONField()

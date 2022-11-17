# Generated by Django 3.2.16 on 2022-11-17 23:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="GhostMember",
            fields=[
                ("email", models.EmailField(max_length=254)),
                (
                    "id",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                ("uuid", models.UUIDField()),
                ("name", models.CharField(max_length=255, null=True)),
                ("note", models.CharField(max_length=255, null=True)),
                ("geolocation", models.CharField(max_length=255, null=True)),
                ("last_seen_at", models.DateTimeField(null=True)),
                ("created_at", models.DateTimeField()),
                ("updated_at", models.DateTimeField()),
                ("email_count", models.IntegerField()),
                ("email_opened_count", models.IntegerField()),
                ("email_open_rate", models.CharField(max_length=128, null=True)),
                ("status", models.CharField(max_length=128)),
                ("labels", models.JSONField(default=list)),
                ("subscriptions", models.JSONField(default=list)),
                ("tiers", models.JSONField(default=list)),
                ("newsletters", models.JSONField(default=list)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

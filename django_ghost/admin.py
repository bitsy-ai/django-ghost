from django.contrib import admin

from .models import GhostMember


@admin.register(GhostMember)
class GhostMemberAdmin(admin.ModelAdmin):
    pass

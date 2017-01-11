from django.contrib import admin

from apps.announcements.models import AnnouncementView
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    fields = (('title', 'created'), ('body',), ('views'))
    readonly_fields = ('views', 'created')


admin.site.register(AnnouncementView)
from django.contrib import admin

from .models import Link, LinkVisit


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'type', 'visit_count', 'enabled', 'login_required')
    list_filter = ('enabled', 'login_required', 'type')
    search_fields = ('title', 'slug', 'url')


@admin.register(LinkVisit)
class LinkVisitAdmin(admin.ModelAdmin):
    list_display = ('link', 'member')
    list_filter = ('link',)
    search_fields = ('link', 'member')

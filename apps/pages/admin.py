from django.contrib import admin

from .models import Link, LinkVisit


def make_enabled(modeladmin, request, queryset):
    queryset.update(enabled=True)


make_enabled.short_description = "Make all selected links enabled"


def make_disabled(modeladmin, request, queryset):
    queryset.update(enabled=False)


make_disabled.short_description = "Make all selected links disabled"


def make_login_req(modeladmin, request, queryset):
    queryset.update(login_required=True)


make_login_req.short_description = "Make all selected links Login Required"


def make_login_unreq(modeladmin, request, queryset):
    queryset.update(login_required=False)


make_login_unreq.short_description = "Make all selected links Login not Required"


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'type', 'visit_count', 'enabled', 'login_required')
    list_filter = ('enabled', 'login_required', 'type')
    search_fields = ('title', 'slug', 'url')
    actions = (make_enabled, make_disabled, make_login_req, make_login_unreq)


@admin.register(LinkVisit)
class LinkVisitAdmin(admin.ModelAdmin):
    list_display = ('link', 'member')
    list_filter = ('link',)
    search_fields = ('link', 'member')

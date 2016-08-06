# coding=utf-8
from django.contrib import admin

from .models import *


class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'active', 'get_count']


class EventRegisterAdmin(admin.ModelAdmin):
    list_display = ['std_id', 'get_member', 'event']
    list_filter = ['event__name']


class DonateAdmin(admin.ModelAdmin):
    list_display = ['id', 'value', 'is_success', 'event', 'user', 'name']
    list_filter = ['event__name']



admin.site.register(Event, EventAdmin)
admin.site.register(EventRegister, EventRegisterAdmin)
admin.site.register(Donate, DonateAdmin)

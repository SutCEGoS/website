# coding=utf-8
from django.contrib import admin

from event.models import *


class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'active', 'get_count']


class EventRegisterAdmin(admin.ModelAdmin):
    list_display = ['std_id', 'event']
    list_filter = ['event__name']


admin.site.register(Event, EventAdmin)
admin.site.register(EventRegister, EventRegisterAdmin)

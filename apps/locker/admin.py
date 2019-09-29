from django.contrib import admin

from .models import *


@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ['name', 'receiver', 'payment', 'receivie_date', 'archived']
    list_filter = ['receivie_date', 'archived']
    search_fields = ['name', 'receiver']


@admin.register(sell)
class SellAdmin(admin.ModelAdmin):
    list_display = ['user', 'locker', 'is_success']

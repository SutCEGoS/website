from django.contrib import admin

from .models import *


@admin.register(rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ['name', 'receiver', 'payment', 'receivie_date']


@admin.register(sell)
class SellAdmin(admin.ModelAdmin):
    list_display = ['user', 'locker', 'is_success']

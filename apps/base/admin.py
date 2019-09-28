from django.contrib import admin
from hijack_admin.admin import HijackUserAdminMixin

from .models import *


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin, HijackUserAdminMixin):
    list_display = ('get_full_name', 'username', 'email', 'is_active', 'is_superuser', 'std_id', 'hijack_field', 'cash')
    search_fields = ('first_name', 'last_name', 'username', 'std_id', 'email')
    list_filter = ('is_active', 'start_year', 'is_superuser', 'is_staff')
    list_display_links = ('get_full_name', 'username', 'email')
    readonly_fields = ('hijack_field', )


# @admin.register(Transaction)
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ['origin', 'destination', 'type', 'amount', 'is_successfully', 'data', 'time']
#     readonly_fields = ['origin', 'destination', 'type', 'amount', 'is_successfully']
#     list_display_links = ['origin', 'destination']
#     list_filter = ['type', 'is_successfully', 'time']
#     search_fields = ['origin', 'destination', 'data']

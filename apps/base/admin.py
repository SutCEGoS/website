from django.contrib import admin
from hijack_admin.admin import HijackUserAdminMixin

from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin, HijackUserAdminMixin):
    list_display = ('get_full_name', 'username', 'email', 'is_active', 'is_superuser', 'std_id', 'hijack_field')
    search_fields = ('first_name', 'last_name', 'username', 'std_id', 'email')
    list_filter = ('is_active', 'start_year', 'is_superuser', 'is_staff')
    list_display_links = ('get_full_name', 'username', 'email')
    readonly_fields = ('hijack_field',)

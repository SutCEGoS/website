from django.contrib import admin

from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'username', 'email', 'is_active', 'std_id', 'hijack_field')
    search_fields = ('first_name', 'last_name', 'username', 'std_id', 'email')
    list_filter = ('is_active', 'start_year')
    list_display_links = ('get_full_name', 'username', 'email')
    readonly_fields = ('hijack_field',)

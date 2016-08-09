from django.contrib import admin

from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'username', 'email', 'is_active', 'std_id')
    search_fields = ('first_name', 'last_name', 'username', 'std_id')
    list_filter = ('is_active', 'start_year')

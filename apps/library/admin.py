from django.contrib import admin

from apps.library.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'translator', 'publication']
    list_display_links = ['name', 'author', 'translator', 'publication']
    search_fields = ['name', 'author', 'translator', 'publication']
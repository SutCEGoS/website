# coding=utf-8
from django.contrib import admin

from objection.models import Objection


class ObjectionAdmin(admin.ModelAdmin):
    actions = ['mark_as_unconfirmed', 'mark_as_waiting']
    list_display = ['id', 'message', 'level', 'field', 'category', 'read', 'confirmed']
    fieldsets = (
        (u'پیام', {
            'fields':
                (
                    'read', 'confirmed', 'sender', 'level', 'sender_year', 'offered_course', 'second_course',
                    'course_name',
                    'field', 'category', 'message')
        }),
    )

    def mark_as_waiting(modeladmin, request, queryset):
        queryset.update(read=True)

    mark_as_waiting.short_description = u"علامت زدن موارد انتخابی به عنوان منتظر پاسخ"

    def mark_as_unconfirmed(modeladmin, request, queryset):
        queryset.update(read=False)

    mark_as_unconfirmed.short_description = u"علامت زدن موارد انتخابی به عنوان تایید نشده"

    list_filter = ['offered_course', 'category', 'status']
    search_fields = ['offered_course', 'category', 'message']


admin.site.register(Objection, ObjectionAdmin)
# coding=utf-8
from django.contrib import admin

from objection.models import Objection


class ObjectionAdmin(admin.ModelAdmin):
    actions = ['mark_as_unconfirmed', 'mark_as_waiting']
    list_display = ['id', 'sender', 'offered_course', 'message', 'category', 'status']
    fieldsets = (
        (u'پیام', {
            'fields':
                (
                    'status', 'sender', 'offered_course', 'second_course',
                    'course_name',
                    'category', 'message')
        }),
    )

    def mark_as_waiting(modeladmin, request, queryset):
        queryset.update(status=3)

    mark_as_waiting.short_description = u"علامت زدن موارد انتخابی به عنوان منتظر پاسخ"

    def mark_as_unconfirmed(modeladmin, request, queryset):
        queryset.update(status=2)

    mark_as_unconfirmed.short_description = u"علامت زدن موارد انتخابی به عنوان تایید نشده"

    list_filter = ['offered_course', 'category', 'status']
    search_fields = ['offered_course', 'category', 'message']


admin.site.register(Objection, ObjectionAdmin)
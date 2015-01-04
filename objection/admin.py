# coding=utf-8
from django.contrib import admin

from objection.models import Objection


class ObjectionAdmin(admin.ModelAdmin):
    actions = ['mark_as_read', 'mark_as_unread', 'mark_as_confirmed', 'mark_as_unconfirmed']
    list_display = ['id', 'message', 'category', 'status']
    fieldsets = (
        (u'پیام', {
            'fields':
                (
                    'status', 'sender',  'offered_course', 'second_course',
                    'course_name',
                    'category', 'message')
        }),
    )

    def mark_as_read(modeladmin, request, queryset):
        queryset.update(read=True)

    mark_as_read.short_description = u"علامت زدن موارد انتخابی به عنوان خوانده شده"

    def mark_as_unread(modeladmin, request, queryset):
        queryset.update(read=False)

    mark_as_unread.short_description = u"علامت زدن موارد انتخابی به عنوان خوانده نشده"

    def mark_as_confirmed(modeladmin, request, queryset):
        queryset.update(confirmed=True)

    mark_as_confirmed.short_description = u"علامت زدن موارد انتخابی به عنوان تایید شده"

    def mark_as_unconfirmed(modeladmin, request, queryset):
        queryset.update(confirmed=False)

    mark_as_unconfirmed.short_description = u"علامت زدن موارد انتخابی به عنوان تایید نشده"

    list_filter = ['offered_course', 'category', 'status']
    search_fields = ['offered_course', 'category', 'message']


admin.site.register(Objection, ObjectionAdmin)
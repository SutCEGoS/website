# coding=utf-8
from django.contrib import admin

from .models import Issue, IssueReply


class IssueReplyAdmin(admin.ModelAdmin):
    list_display = ['author', 'text']
    fieldsets = (
        (u'پیام', {
            'fields':
                ('text',)
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


class IssueAdmin(admin.ModelAdmin):
    actions = ['mark_as_unconfirmed', 'mark_as_waiting', 'mark_as_read']
    list_display = ['id', 'sender', 'requests', 'status', 'category', 'message', 'reply']
    fieldsets = (
        (u'پیام', {
            'fields':
                ('status',
                 'category',
                 'message')
        }),
        (u'پاسخ', {
            'fields':
                ('reply',)
        }),
    )

    def response_change(self, request, obj):
        if IssueReply.objects.filter(issue=obj).exists():
            obj.status = 5
        else:
            obj.status = 3
        obj.save()

        return super(IssueAdmin, self).response_change(request, obj)

    def queryset(self, request):
        qs = super(IssueAdmin, self).queryset(request)

        if request.user.groups.filter(name='مسئول رفاهی').exists() and not request.user.is_superuser:
            self.readonly_fields = ('status', 'category', 'message')

            return qs.filter(status__gte=3)
        return qs

    def get_list_display(self, request):
        dl = super(IssueAdmin, self).get_list_display(request)
        if request.user.groups.filter(name='مسئول رفاهی').exists() and not request.user.is_superuser:
            if 'sender' in dl:
                dl.remove('sender')
            return dl
        return dl


    def mark_as_waiting(modeladmin, request, queryset):
        queryset.update(status=3)

    mark_as_waiting.short_description = u"علامت زدن موارد انتخابی به عنوان منتظر پاسخ"

    def mark_as_unconfirmed(modeladmin, request, queryset):
        queryset.update(status=2)

    mark_as_unconfirmed.short_description = u"علامت زدن موارد انتخابی به عنوان تایید نشده"

    def mark_as_read(modeladmin, request, queryset):
        queryset.update(status=4)

    mark_as_read.short_description = u"علامت زدن موارد انتخابی به عنوان خوانده شده"

    list_filter = ['status', 'category']
    search_fields = ['category', 'message']


admin.site.register(Issue, IssueAdmin)
admin.site.register(IssueReply, IssueReplyAdmin)

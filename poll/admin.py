# coding=utf-8
from django.contrib import admin

from poll.models import PollChoice, Poll, Vote


class PollChoiceInline(admin.StackedInline):
    model = PollChoice
    extra = 4


class PollChoiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'poll']
    fieldsets = (
        (u'گزینه', {
            'fields':
                ('name',)
        }),
    )
    list_display_links = ('poll', 'name',)
    search_fields = ['name', 'poll__question']


class PollAdmin(admin.ModelAdmin):
    def mark_as_active(modeladmin, request, queryset):
        queryset.update(is_active=True)

    mark_as_active.short_description = u"علامت زدن موارد انتخابی به عنوان فعال"

    def mark_as_deactive(modeladmin, request, queryset):
        queryset.update(is_active=False)

    mark_as_deactive.short_description = u"علامت زدن موارد انتخابی به عنوان غیرفعال"

    actions = ['mark_as_active', 'mark_as_deactive']
    inlines = [PollChoiceInline, ]
    list_display = ['name', 'question', 'active']
    fieldsets = (
        (u'نظرسنجی', {
            'fields':
                ('name', 'question', 'details', 'end', 'is_active')
        }),
    )
    list_filter = ['is_active']
    search_fields = ['question']


class VoteAdmin(admin.ModelAdmin):
    fieldsets = (
        (u'نظر', {
            'fields':
                ('comment', 'choice', 'verified')
        }),
    )
    actions = ['mark_as_accepted', 'mark_as_not_accepted']
    list_display = ['choice', 'get_member', 'comment', 'verified']
    list_filter = ('choice__poll__name', 'verified')

    def queryset(self, request):
        qs = super(VoteAdmin, self).queryset(request)
        if request.user.groups.filter(name='Replier').exists() and not request.user.is_superuser:
            self.readonly_fields = ('comment', 'choice')
            self.fieldsets = (
                (u'نظر', {
                    'fields':
                        ('comment', 'choice',)
                }),
            )

            return qs.filter(verified=True)
        return qs

    def get_list_display(self, request):
        dl = super(VoteAdmin, self).get_list_display(request)
        if request.user.groups.filter(name='Replier').exists() and not request.user.is_superuser:
            if 'get_member' in dl:
                dl.remove('get_member')
            if 'verified' in dl:
                dl.remove('verified')
            return dl
        return dl

    def mark_as_accepted(modeladmin, request, queryset):
        queryset.update(verified=True)

    mark_as_accepted.short_description = u"علامت زدن موارد انتخابی به عنوان تایید شده"

    def mark_as_not_accepted(modeladmin, request, queryset):
        queryset.update(verified=False)

    mark_as_not_accepted.short_description = u"علامت زدن موارد انتخابی به عنوان تایید نشده"


admin.site.register(Vote, VoteAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(PollChoice, PollChoiceAdmin)

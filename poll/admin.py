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
                ('name', 'question', 'end', 'is_active')
        }),
    )
    list_filter = ['is_active']
    search_fields = ['question']


class VoteAdmin(admin.ModelAdmin):
    list_display = ['choice', 'get_member', 'comment']
    list_filter = ('choice__poll__name', )


admin.site.register(Vote, VoteAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(PollChoice, PollChoiceAdmin)

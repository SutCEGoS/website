# coding=utf-8
from django.contrib import admin
from django.db.models.signals import pre_save
from django.dispatch import receiver

from base.models import Member

from objection.models import Objection, Reply


@receiver(pre_save, sender=Reply, dispatch_uid='autocreate_author')
def create_username(sender, instance, *args, **kwargs):
    instance.author = Member.objects.filter(is_superuser=True).last()


class ReplyInline(admin.StackedInline):
    model = Reply
    fields = ('text',)
    max_num = 1


class ObjectionAdmin(admin.ModelAdmin):
    inlines = [ReplyInline]

    actions = ['mark_as_unconfirmed', 'mark_as_waiting', 'mark_as_read']
    list_display = ['id', 'status', 'category', 'message', 'offered_course', 'second_course', 'course_name']
    fieldsets = (
        (u'پیام', {
            'fields':
                (
                    'status', 'offered_course', 'second_course',
                    'course_name',
                    'category', 'message')
        }),
    )
    readonly_fields = ('status', 'offered_course', 'second_course',
                       'course_name',
                       'category', 'message')


    def response_change(self, request, obj):
        if Reply.objects.filter(objection=obj).exists():
            obj.status = 5
        else:
            obj.status = 3
        obj.save()

        return super(ObjectionAdmin, self).response_change(request, obj)

    def save_related(self, request, form, formsets, change):
        q = super(ObjectionAdmin, self).save_related(request, form, formsets, change)
        for item in formsets:
            item.instance.author = request.user
            item.instance.save()
        return q

    def queryset(self, request):
        qs = super(ObjectionAdmin, self).queryset(request)
        if request.user.groups.filter(name='Replier').exists():
            return qs.filter(status__gte=3)
        return qs


    def mark_as_waiting(modeladmin, request, queryset):
        queryset.update(status=3)


    mark_as_waiting.short_description = u"علامت زدن موارد انتخابی به عنوان منتظر پاسخ"


    def mark_as_unconfirmed(modeladmin, request, queryset):
        queryset.update(status=2)


    mark_as_unconfirmed.short_description = u"علامت زدن موارد انتخابی به عنوان تایید نشده"


    def mark_as_read(modeladmin, request, queryset):
        queryset.update(status=4)


    mark_as_read.short_description = u"علامت زدن موارد انتخابی به عنوان خوانده شده"

    list_filter = ['status', 'category', 'offered_course']
    search_fields = ['offered_course', 'category', 'message']

admin.site.register(Objection, ObjectionAdmin)
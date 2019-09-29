import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import *


@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ['name', 'receiver', 'payment', 'receivie_date', 'archived']
    list_filter = ['receivie_date', 'archived']
    search_fields = ['name', 'receiver']

    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "خروحی موارد انتخاب شده به صورت csv"


@admin.register(sell)
class SellAdmin(admin.ModelAdmin):
    list_display = ['user', 'locker', 'is_success']

from django.contrib import admin
from .models import rack,sell
# Register your models here...

class rackAdmin(admin.ModelAdmin):
    list_display = ['name','receiver','payment', 'receivie_date']

class sellAdmin(admin.ModelAdmin):
    list_display = ['user' , 'locker' , 'is_success']

admin.site.register(rack , rackAdmin)
admin.site.register(sell , sellAdmin)

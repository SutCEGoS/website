from django.contrib import admin
from .models import rack,sell
# Register your models here...

class sellAdmin(admin.ModelAdmin):
    list_display = ['user' , 'locker' , 'is_success']

admin.site.register(rack)
admin.site.register(sell , sellAdmin)

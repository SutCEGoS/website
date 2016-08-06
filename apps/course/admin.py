from django.contrib import admin

from .models import Course, OfferedCourse, Professor

admin.site.register(Course)
admin.site.register(OfferedCourse)
admin.site.register(Professor)
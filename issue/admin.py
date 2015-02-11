from django.contrib import admin

# Register your models here.
from issue.models import Issue

admin.site.register(Issue)
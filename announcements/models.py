from __future__ import unicode_literals

from django.db import models
from tinymce import models as tinymce_models


# Create your models here.

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    body = tinymce_models.HTMLField()
    date = models.DateTimeField(auto_now=True)

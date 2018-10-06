# Generated by Django 2.1.2 on 2018-10-04 17:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0004_auto_20170116_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='issue_liked_member', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 2.1.2 on 2019-09-20 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20190920_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

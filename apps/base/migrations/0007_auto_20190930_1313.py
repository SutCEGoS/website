# Generated by Django 2.1.2 on 2019-09-30 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20190928_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='card_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='sheba',
            field=models.CharField(blank=True, default='', max_length=30, null=True),
        ),
    ]
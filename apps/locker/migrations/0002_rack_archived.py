# Generated by Django 2.1.2 on 2019-09-28 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rack',
            name='archived',
            field=models.BooleanField(default=False, null=True, verbose_name='آرشیو شده'),
        ),
    ]
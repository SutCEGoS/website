# Generated by Django 2.1.2 on 2019-11-28 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_checkoutrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkoutrequest',
            name='status',
            field=models.IntegerField(choices=[(1, 'درخواست شده'), (2, 'انجام شده'), (3, 'لغو شده')], default=1, verbose_name='وضعیت'),
        ),
    ]
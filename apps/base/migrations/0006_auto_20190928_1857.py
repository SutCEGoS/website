# Generated by Django 2.1.2 on 2019-09-28 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_transaction_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='زمان'),
        ),
    ]

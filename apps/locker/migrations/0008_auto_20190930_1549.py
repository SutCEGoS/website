# Generated by Django 2.1.2 on 2019-09-30 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locker', '0007_auto_20190930_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sell',
            name='locker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locker.Rack'),
        ),
    ]

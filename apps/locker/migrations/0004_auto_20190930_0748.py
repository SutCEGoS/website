# Generated by Django 2.1.2 on 2019-09-30 04:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locker', '0003_auto_20190929_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sell',
            name='locker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locker.Rack'),
        ),
    ]
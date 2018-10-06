# Generated by Django 2.1.2 on 2018-10-06 19:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='rack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=3)),
                ('payment', models.BooleanField(default=False)),
                ('receivie_date', models.DateTimeField(auto_now_add=True)),
                ('condition', models.PositiveSmallIntegerField(choices=[(0, 'available'), (1, 'unavailable')], default=0)),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='sell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=20000)),
                ('is_success', models.NullBooleanField(default=True)),
                ('authority', models.CharField(max_length=63)),
                ('locker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locker.rack')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

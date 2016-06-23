# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-23 01:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
        ('course', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Objection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.PositiveSmallIntegerField(choices=[(0, '------------'), (1, 'تلاقی زمان کلاس'), (2, 'تاریخ امتحان نامناسب'), (3, 'عدم ارائه'), (4, 'تعداد گروه کم'), (6, 'غیره')])),
                ('course_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='درس ارائه نشده')),
                ('message', models.TextField(blank=True, null=True, verbose_name='متن')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'منتظر تایید'), (2, 'تایید نشده'), (3, 'منتظر پاسخ'), (4, 'مشاهده شده'), (5, 'پاسخ داده شده')])),
                ('term', models.PositiveSmallIntegerField(choices=[(1, 'پاییز'), (2, 'بهار'), (3, 'تابستان')])),
                ('like', models.ManyToManyField(blank=True, null=True, related_name='liked_member', to=settings.AUTH_USER_MODEL)),
                ('offered_course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.OfferedCourse', verbose_name='درس')),
                ('second_course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='second', to='course.OfferedCourse', verbose_name='تلاقی با')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.EducationalYear')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('objection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='objection.Objection')),
            ],
        ),
    ]

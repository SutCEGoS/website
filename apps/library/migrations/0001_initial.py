# Generated by Django 2.1.2 on 2019-09-19 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام')),
                ('author', models.CharField(blank=True, max_length=100, null=True, verbose_name='نویسنده')),
                ('translator', models.CharField(blank=True, max_length=100, null=True, verbose_name='مترجم')),
                ('publication', models.CharField(blank=True, max_length=100, null=True, verbose_name='ناشر')),
                ('image', models.ImageField(upload_to='', verbose_name='تصویر کتاب')),
                ('count', models.IntegerField(default=1, verbose_name='تعداد')),
            ],
            options={
                'verbose_name': 'کتاب',
                'verbose_name_plural': 'کتاب\u200cها',
            },
        ),
    ]

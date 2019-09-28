# Generated by Django 2.1.2 on 2019-09-19 11:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(verbose_name='آدرس در سایت')),
                ('url', models.URLField(verbose_name='آدرس لینک')),
                ('title', models.CharField(max_length=90, verbose_name='عنوان')),
                ('login_required', models.BooleanField(default=False, verbose_name='فقط افراد عضو')),
                ('enabled', models.BooleanField(default=True, verbose_name='فعال')),
                ('type', models.IntegerField(choices=[(0, 'نمایش در سایت'), (1, 'هدایت به آدرس')], verbose_name='نحوهٔ نمایش')),
            ],
        ),
        migrations.CreateModel(
            name='LinkVisit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='pages.Link', verbose_name='لینک')),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

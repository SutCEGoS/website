# Generated by Django 2.1.2 on 2019-09-20 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20190919_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='data',
            field=models.CharField(max_length=512, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.IntegerField(choices=[(1, 'شارژ نقدی'), (2, 'شارژ آنلاین'), (3, 'انتقال وجه'), (4, 'استفاده از خدمات شورا'), (5, 'تسویه حساب')], verbose_name='نوع تراکنش'),
        ),
    ]
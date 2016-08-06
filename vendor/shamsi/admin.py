# -*- coding: utf-8 -*-

__docformat__ = 'reStructuredText'

from django.contrib.admin.options import ModelAdmin

from django.db import models
from django.db.models.fields import DateTimeField, DateField

#noinspection PyUnresolvedReferences
from .date.shamsi_date import Shamsi
from .fields import ShamsiDateField, ShamsiAdminSplitDateTimeField


class ShamsiModelAdmin(ModelAdmin):
    """
    این کلاس، فیلدهای
    DateField , DateTimeField
    را در قسمت ادمین به صورت تاریخ شمسی در می‌آورد تا کاربر بتواند تاریخ را به صورت شمسی وارد نموده و مشاهده نماید.

    """
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(ShamsiModelAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if isinstance(db_field, models.DateTimeField):
            field = ShamsiAdminSplitDateTimeField()
            field.label = db_field.verbose_name
            field.required = not db_field.null
            field.help_text = db_field.help_text
        elif isinstance(db_field, models.DateField):
            field = ShamsiDateField()
            field.label = db_field.verbose_name
            field.required = not db_field.null
            field.help_text = db_field.help_text
        return field

    def __init__(self, *args, **kwargs):
        result = ()
        for i in range(len(self.list_display)):
            field = self.list_display[i]
            verbose_name = field
            tp = 0
            for model_field in args[0]._meta.fields:
                if model_field.name == field:
                    verbose_name = model_field.verbose_name
                    if isinstance(model_field, DateField):
                        tp = 1
                    if isinstance(model_field, DateTimeField):
                        tp = 2
                    break
            if tp == 1:
                exec ('def ' + field + '_shamsi (obj): return Shamsi(obj.' + field + \
                     ').strfshamsi(Shamsi.LONG_DATE) \n' + field + '_shamsi.short_description = u"' + verbose_name +\
                     '"\nself.' + field + '_shamsi = ' + field + '_shamsi')
            if tp == 2:
                exec ('def ' + field + '_shamsi (obj): return Shamsi(obj.' + field + \
                     ').strfshamsi(Shamsi.LONG_DATETIME_SEC) \n' + field + '_shamsi.short_description = u"' + \
                     verbose_name + '"\nself.' + field + '_shamsi = ' + field + '_shamsi')
            if tp:
                field += "_shamsi"
            result += (field, )
        self.list_display = result
        super(ShamsiModelAdmin, self).__init__(*args, **kwargs)

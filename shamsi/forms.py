#encoding:UTF-8

from django import forms
from .fields import ShamsiDateField


class ShamsiDateFieldModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ShamsiDateFieldModelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if isinstance(self.fields[field], forms.DateField):
                label = self.fields[field].label
                required = self.fields[field].required
                new_field = ShamsiDateField(label=label, required=required)
                self.fields[field] = new_field

#                self.fields[field].widget = ShamsiWidget()


class ShamsiDateFieldForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ShamsiDateFieldForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if isinstance(self.fields[field], forms.DateField):
                label = self.fields[field].label
                required = self.fields[field].required
                new_field = ShamsiDateField(label=label, required=required)
                self.fields[field] = new_field

#                self.fields[field].widget = ShamsiWidget()

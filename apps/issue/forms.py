# coding=utf-8
from django import forms

from .models import Issue


__author__ = 'mjafar'


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = {'sender', 'status', 'title', 'category', 'message'}

    def __init__(self, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.TypedChoiceField(choices=Issue.CATEGORY, empty_value="---")
        self.fields['category'].label = u"موضوع"
        self.fields['title'].label = u"عنوان"
        for field in self.fields:
            if field not in ['offered_course', 'second_course']:
                css_class = 'form-control'
            else:
                css_class = 'full-width'
            self.fields[field].widget.attrs.update({'class': css_class})

    def clean(self):
        cd = super(IssueForm, self).clean()
        category = int(cd.get('category'))
        cd['category'] = category

        return cd


class BotIssueForm(forms.Form):
    place = forms.CharField(max_length=60)
    title = forms.CharField(max_length=63)
    description = forms.CharField(required=False)

from django import forms
from .models import rack

class rackForm(forms.ModelForm):
    class Meta:
        model = rack
        fields = {'receiver', 'condition', 'name'}
    def __init__(self, *args, **kwargs):
        super(rackForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = u"نام و شماره"
        for field in self.fields:
            if field not in ['offered_course', 'second_course']:
                css_class = 'form-control'
            else:
                css_class = 'full-width'
            self.fields[field].widget.attrs.update({'class': css_class})

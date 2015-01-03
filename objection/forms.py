# coding=utf-8
from django import forms

from course.models import Course


__author__ = 'mjafar'

from objection.models import Objection


class MessageForm(forms.ModelForm):
    class Meta:
        model = Objection
        fields = {'sender', 'status', 'second_course', 'course_name', 'offered_course', 'category', 'message'}

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.TypedChoiceField(choices=Objection.CATEGORY, empty_value="---")
        for field in self.fields:
            if field not in ['offered_course', 'second_course']:
                css_class = 'form-control'
            else:
                css_class = 'full-width'
            self.fields[field].widget.attrs.update({'class': css_class})

    def clean(self):
        cd = super(MessageForm, self).clean()
        second_course = cd.get('second_course')
        course_name = cd.get('course_name')
        offered_course = cd.get('offered_course')
        category = cd.get('category')
        message = cd.get('message')
        if category:
            if category == 0:
                self.errors['category'] = self.error_class([u'انتخاب دسته ی مشکل لازم است'])
            if category == 3:
                if not course_name:
                    self.errors['course_name'] = self.error_class([u'پر کردن نام درس ارائه نشده اجباری است.'])
                elif course_name in Course.objects.all().values_list('name', flat=True):
                    self.errors['course_name'] = self.error_class([u'درسی با همین عنوان ارائه داده شده است :)'])
            elif category == 1:
                if not offered_course:
                    self.errors['offered_course'] = self.error_class([u'انتخاب درس اجباری است'])
                elif not second_course:
                    self.errors['second_course'] = self.error_class(
                        [u'در صورت تلاقی دروس وارد کردن نام درس دوم اجباری است.'])
                elif offered_course == second_course:
                    self.errors['second_course'] = self.error_class([
                        u'خب دوست خوبم، بدیهی است هر درسی با خودش تلاقی داره، ولی achievement آنلاک کردی راضیم ازت :)'])
            else:
                if not offered_course:
                    self.errors['offered_course'] = self.error_class([u'انتخاب درس اجباری است'])
            pass

        return cd



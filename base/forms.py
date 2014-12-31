# coding=utf-8
from django import forms
from django.contrib.auth import authenticate

from base.models import Member

__author__ = 'Amin'

"""
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = {'email', 'sender', 'level', 'sender_year', 'second_course', 'course_name', 'field', 'offered_course',
                  'category', 'message'}

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['offered_course', 'second_course']:
                css_class = 'form-control'
            else:
                css_class = 'full-width'
            self.fields[field].widget.attrs.update({'class': css_class})

    def clean(self):
        cd = super(MessageForm, self).clean()
        email = cd.get('email')
        sender = cd.get('sender')
        level = cd.get('level')
        sender_year = cd.get('sender_year')
        second_course = cd.get('second_course')
        course_name = cd.get('course_name')
        field = cd.get('field')
        offered_course = cd.get('offered_course')
        category = cd.get('category')
        message = cd.get('message')
        if category:
            if category.id == 3:
                if not course_name:
                    self.errors['course_name'] = self.error_class([u'پر کردن نام درس ارائه نشده اجباری است.'])
                elif course_name in Course.objects.all().values_list('name',flat=True):
                    self.errors['course_name'] = self.error_class([u'درسی با همین عنوان ارائه داده شده است :)'])
            elif category.id == 1:
                if not offered_course:
                    self.errors['offered_course'] = self.error_class([u'انتخاب درس اجباری است'])
                elif not second_course:
                    self.errors['second_course'] = self.error_class([u'در صورت تلاقی دروس وارد کردن نام درس دوم اجباری است.'])
                elif offered_course == second_course:
                    self.errors['second_course'] = self.error_class([u'خب دوست خوبم، بدیهی است هر درسی با خودش تلاقی داره، ولی achievement آنلاک کردی راضیم ازت :)'])
            else:
                if not offered_course:
                    self.errors['offered_course'] = self.error_class([u'انتخاب درس اجباری است'])

        return cd
"""


class SignInForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields[field].initial = ""
        self.fields.keyOrder = [
            'username', 'password'
        ]

    def clean(self):
        cd = super(SignInForm, self).clean()
        password = cd.get('password')
        username = cd.get('username').lower()
        if username:
            try:
                member = Member.objects.get(username=username)
                if not member.check_password(password):
                    self.errors['password'] = u'Incorrect username or password.'
                    return
            except (Member.DoesNotExist, Member.MultipleObjectsReturned):
                self.errors['password'] = u'Incorrect username or password.'
                return
            user = authenticate(username=member.username, password=password)
            if user is not None:
                if not user.is_active:
                    self.errors['username'] = u"Your account is not activate."
                    return
                self.user = user
            else:
                self.errors['password'] = u'Incorrect username or password.'
                return

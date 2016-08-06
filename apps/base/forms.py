# coding=utf-8
from django import forms
from django.contrib.auth import authenticate

from .models import Member

__author__ = 'Amin'


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
        username = cd.get('username')
        try:
            username = username.lower()
        except AttributeError:
            pass
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


class PasswordForm(forms.Form):
    password = forms.CharField(required=False, widget=forms.PasswordInput(), label=u'گذرواژه‌ی فعلی')
    password1 = forms.CharField(required=False, widget=forms.PasswordInput(), label=u'گذرواژه‌ی جدید')
    password2 = forms.CharField(required=False, widget=forms.PasswordInput(), label=u'تکرار گذرواژه')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = super(PasswordForm, self).clean()
        old_password = cd.get('password')
        new_password = cd.get('password1')
        confirm_new_password = cd.get('password2')
        if not old_password:
            self.errors['password'] = u'Password field must filled out.'
            return
        else:
            member = Member.objects.get(id=self.user.pk)
            if not member.check_password(old_password):
                self.errors['password'] = u'Incorrect password.'
                return
        if new_password:
            if new_password != confirm_new_password:
                self.errors['password2'] = u'Passwords are not same.'
                return
        else:
            self.errors['password1'] = u'New Password field must filled out.'
            return
        self.user.set_password(new_password)
        self.user.save()
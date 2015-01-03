# coding=utf-8
from django import forms
from django.contrib.auth import authenticate

from base.models import Member


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

from django.contrib.auth import login as dj_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from base.forms import *
from base.models import Member
from objection.views import requests


def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    else:
        return requests(request)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('requests'))
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            next = request.GET.get('next')
            user = form.user
            dj_login(request, user)
            if not next:
                next = reverse('requests')
            return HttpResponseRedirect(next)
    else:
        form = SignInForm()
    return render(request, 'login.html', {
        'form': form,
    })


def save_file(in_memory_file):
    import os
    from django.core.files.storage import default_storage
    from django.core.files.base import ContentFile
    from django.conf import settings

    path = default_storage.save('data_file/' + str(in_memory_file), ContentFile(in_memory_file.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    return tmp_file


@login_required
def create_accounts(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    message = ""
    if request.method == "POST":
        emails_file = request.FILES.get('emails')
        if not emails_file:
            message = "file is required"
        else:
            emails_file = save_file(emails_file)
            file_lines = open(emails_file, 'r').readlines()
            for i in range(len(file_lines)):
                line = file_lines[i]
                splitted_line = line.split('-')
                try:
                    new_email = splitted_line[0]
                except:
                    message += str(i)
                try:
                    new_std_id = splitted_line[1]
                except:
                    new_std_id = ""
                new_password = Member.objects.make_random_password(length=10)
                if '@' in new_email:
                    new_username = new_email[:new_email.find('@')]
                else:
                    new_username = new_email
                    new_email = new_username + "@ce.sharif.edu"
                try:
                    member = Member.objects.get(username=new_username)
                except:
                    new_member = Member.objects.create(username=new_username.lower(),
                                                       std_id=new_std_id,
                                                       email=new_email.lower(),
                                                       password=make_password(new_password))
            if message:
                message += "making account for this lines is not possible, please contact A\'min"
            else:
                message = "success"
    return render(request, 'create_account.html', {
        'message': message,
    })



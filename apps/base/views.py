from django.contrib.auth import login as dj_login
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from apps.announcements.models import Announcement
from .forms import *


def home(request):
    go_course = False
    try:
        x = request.get_host().split('.')
        x = x[0]
        if x.__eq__('course'):
            go_course = True
    except:
        pass
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    else:
        if go_course:
            return HttpResponseRedirect(reverse('requests'))
        return HttpResponseRedirect(reverse('issues'))

def under_construction(request):
    return render(request,'under-construction.html',{})

def index(request):
    announcements = Announcement.objects.all()[:3]

    return render(request, 'index.html', {
        'announcements': announcements,
    })


def logout(request):
    dj_logout(request)
    return redirect('home')

def profile(request):
    return render(request,'complete_profile.html',{})

def complete_profile(request):
    usingEmail = request.GET.get('email')
    fName = request.GET.get('firstName')
    lName = request.GET.get('lastName')
    user = request.user
    user.email = usingEmail
    user.first_name = fName
    user.last_name = lName
    user.save()
    return HttpResponseRedirect(reverse('home'))


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    next = request.GET.get('next', reverse('home'))

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = form.user
            dj_login(request, user)
            return HttpResponseRedirect(next)
    else:
        form = SignInForm()
    return render(request, 'login2.html', {
        'form': form,
        'next': next,
    })


@login_required
def password_reset_change(request):
    if request.method == 'POST':
        form = PasswordForm(user=request.user, data=request.POST)
        form.is_valid()
        sent = True
    else:
        form = PasswordForm(user=request.user)
        sent = False

    return render(request,
                  'password_reset/password_change.html',
                  {
                      'form': form,
                      'sent': sent,
                  })

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from base.forms import *

def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    pass

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('requests'))
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            next = request.GET.get('next')
            user = form.user
            login(request, user)
            if not next:
                next = reverse('requests')
            return HttpResponseRedirect(next)
    else:
        form = SignInForm()
    return render(request, 'login.html', {
        'form': form,
    })

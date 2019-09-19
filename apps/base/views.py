from django.contrib.auth import login as dj_login
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
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
    return render(request, 'under-construction.html', {})


def index(request):
    announcements = Announcement.objects.all()[:3]

    return render(request, 'index.html', {
        'announcements': announcements,
    })


def logout(request):
    dj_logout(request)
    return redirect('home')


def profile(request):
    return render(request, 'complete_profile.html', {})


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
    next = request.GET.get('next', reverse('home'))
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = form.user
            dj_login(request, user)
            next = request.POST.get('next')
            if next == None:
                next = request.GET.get('next', reverse('home'))
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
                  'password_reset/password_change.html', {
                      'form': form,
                      'sent': sent,
                  })


@login_required
def charge_menu(request):
    return render(request,
                  "charge.html", {

                  })


@login_required
def charge_cash(request):
    if not request.user.is_staff:
        return render(request, "charge_cash.html", {
            "error": "شما دسترسی به این قسمت ندارید.",
            "completed": True
        })

    amount = None
    student_number = None

    if request.POST:
        try:
            amount = int(request.POST.get("amount"))
            student_number = int(request.POST.get("student_number"))
        except:
            return render(request, "charge_cash.html", {
                "completed": False,
                "error": "فرمت اطلاعات فرستاده شده درست نیست."
            })

    if amount is not None and student_number is not None:
        member = Member.objects.filter(std_id=student_number)
        if len(member) > 0:
            member = member[0]
            member.cash += amount
            member.save()

            return render(request, "charge_cash.html", {
                "completed": False,
                "success": "اعتبار %s به میزان %d تومان افزایش یافت." % (member.get_full_name(), amount)
            })

        return render(request, "charge_cash.html", {
            "completed": False,
            "error": "دانشجو با شمارهٔ دانشجویی وارد شده یافت نشد."
        })

    return render(request, "charge_cash.html", {
        "completed": False
    })


@login_required
def charge_credit(request):
    amount = None

    if request.POST:
        try:
            amount = int(request.POST.get("amount"))
            trust_amounts = [10000, 20000, 30000, 40000, 50000, 100000]
            if not amount in trust_amounts:
                return render(request, "charge_online.html", {
                    "completed": False,
                    "error": "مبلغ وارد شده معتبر نمی‌باشد."
                })
        except:
            return render(request, "charge_online.html", {
                "completed": False,
                "error": "فرمت اطلاعات فرستاده شده درست نیست."
            })

    if amount is not None:
        member = Member.objects.filter(username=request.user.username)
        if len(member) > 0:
            member = member[0]
            # member.cash += amount
            # member.save()

            return render(request, "charge_confirmation.html", {
                "price": amount
            })

        return render(request, "charge_online.html", {
            "completed": False,
            "error": "اطلاعات شما در دیتابیس به درستی ثبت نشده است."
        })

    return render(request, "charge_online.html", {
        "completed": False
    })

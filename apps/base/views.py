from django.contrib.auth import login as dj_login
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect
from zeep import Client

from apps.announcements.models import Announcement
from apps.base.models import *
from .forms import *

url = "https://www.zarinpal.com/pg/services/WebGate/wsdl"
MERCHANT = '0f3e8346-d100-11e8-b90d-005056a205be'
client = "" #  Client(url)


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

            transaction = Transaction(origin=None, destination=member, amount=amount, is_successfully=True, type=1)
            transaction.save()

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
            trust_amounts = [1001, 10000, 20000, 30000, 40000, 50000, 100000]
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
            transaction = Transaction(destination=member, amount=amount, type=2, is_successfully=False)
            transaction.save()

            return render(request, "charge_confirmation.html", {
                "transaction": transaction
            })

        return render(request, "charge_online.html", {
            "completed": False,
            "error": "اطلاعات شما در دیتابیس به درستی ثبت نشده است."
        })

    return render(request, "charge_online.html", {
        "completed": False
    })


def payment(request, transaction_id):
    transaction = Transaction.objects.filter(id=int(transaction_id))
    if len(transaction) == 0:
        raise Http404
    transaction = transaction[0]
    if transaction.type != 2:
        raise Http404

    site_name = request.META.get('HTTP_HOST', 'shora.ce.sharif.edu')
    callback_url = "http://%s/charge/verify/" % site_name
    result = client.service.PaymentRequest(MERCHANT, transaction.amount, transaction, transaction.destination.email, "",
                                           callback_url)

    if result.Status == 100:
        transaction.Authority = result.Authority
        transaction.save()
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(transaction.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))


def verify(request):
    if request.GET.get('Status') == 'OK':
        authority = request.GET.get('Authority')
        transaction = Transaction.objects.filter(Authority=authority)
        if len(transaction) == 0:
            return render(request, "charge_online.html", {
                "completed": True,
                "error": "تراکنشی با اطلاعات فرستاده شده یافت نشد. برای رفع مشکل می‌توانید به دفتر شورای صنفی مراجعه "
                         "کنید. "
            })
        transaction = transaction[0]
        if transaction.type != 2:
            return render(request, "charge_online.html", {
                "completed": True,
                "error": "این تراکنش از نوع شارژ آنلاین نمی‌باشد."
            })
        if transaction.is_successfully:
            return render(request, "charge_online.html", {
                "completed": True,
                "error": "این تراکنش قبلا انجام و اعتبار سنجی شده است."
            })

        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], transaction.amount)
        if result.Status == 100:
            member = transaction.destination
            member.cash += transaction.amount
            member.save()
            transaction.is_successfully = True
            transaction.data = result.RefID
            transaction.save()
            return render(request, "charge_online.html", {
                "completed": True,
                "success": "حساب شما با موفقیت شارژ شد. برای جلوگیری از وقوع مشکل کد تراکنش را نزد خود نگه دارید: %s" % result.RefID
            })

        elif result.Status == 101:
            return render(request, "charge_online.html", {
                "completed": True,
                "error": "تراکنش هنوز به پایان نرسیده است. لطفا دوباره امتحان کنید و درصورت وجود مشکل به دفتر شورای "
                         "صنفی مراجعه کنید. "
            })

        else:
            return render(request, "charge_online.html", {
                "completed": True,
                "error": "تراکنش با خطا مواجه شد. درصورت کسر پول از حساب شما و عدم برگشت آن تا ۷۲ ساعت به دفتر شورای "
                         "صنفی مراجعه کنید. "
            })
    else:
        return render(request, "charge_online.html", {
            "completed": True,
            "error": "تراکنش انجام نشد یا توسط شما لغو گردید."
        })

from datetime import datetime, timedelta

from django.contrib.auth import login as dj_login
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils.safestring import mark_safe
from zeep import Client

from apps.announcements.models import Announcement
from apps.base.models import *
from .forms import *

url = "https://www.zarinpal.com/pg/services/WebGate/wsdl"
MERCHANT = '0f3e8346-d100-11e8-b90d-005056a205be'
client = Client(url)
CHECKOUT_REQUEST_DELTA = 7 * 60 * 60 * 24


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
    card_number = request.GET.get('card_number')
    sheba = request.GET.get('sheba')

    user = Member.objects.get(username=request.user.username)
    user.email = usingEmail
    user.first_name = fName
    user.last_name = lName
    user.card_number = card_number
    user.sheba = sheba

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


@user_passes_test(lambda u: u.is_staff)
def checkout_list_view(request):
    return render(request, "checkout_request_list.html", {
        "checkout_requests": CheckoutRequest.objects.filter(status=1)
    })


@user_passes_test(lambda u: u.is_staff)
def checkout_action(request, req_id, action):
    action = int(action)
    req_id = int(req_id)
    checkout_request = CheckoutRequest.objects.get(id=req_id)
    if not checkout_request:
        return HttpResponse("invalid request id")
    amount = checkout_request.user.cash
    checkout_request.status = action if action == 2 else 3
    checkout_request.save()

    if action == 2:
        checkout_request.user.cash = 0
        checkout_request.user.save()
        transaction = Transaction(origin=checkout_request.user, amount=amount, type=5, is_successfully=True)
        transaction.save()

    else:
        transaction = Transaction(origin=checkout_request.user, amount=amount, type=5, is_successfully=False)
        transaction.save()

    return redirect(checkout_list_view)


@login_required
def charge_menu(request):
    return render(request,
                  "charge.html", {

                  })


@login_required
def checkout_view(request):
    last_request = CheckoutRequest.objects.filter(user=request.user, status=1).last()
    if last_request:
        delta = datetime.now().timestamp() - last_request.date.timestamp()
        if delta < CHECKOUT_REQUEST_DELTA:
            return render(request, "checkout.html", {
                "error": "در فاصلهٔ کمتر از یک هفته امکان ثبت درخواست تسویهٔ حساب وجود ندارد.",
                "done": True
            })
    if request.user.cash == 0:
        return render(request, "checkout.html", {
            "error": "اعتبار شما صفر است و نمی‌توانید درخواست تسویه حساب دهید.",
            "done": True
        })

    if not request.POST:
        form = FormWithCaptcha()
        return render(request, "checkout.html", {
            "form": form
        })
    form = FormWithCaptcha(request.POST)
    if not form.is_valid():
        form = FormWithCaptcha()
        return render(request, "checkout.html", {
            "form": form,
            "error": "خطا. لطفا تیک من ربات نیستم را بزنید."
        })

    checkout_request = CheckoutRequest(user=request.user, status=1)
    checkout_request.save()

    return render(request, "checkout.html", {
        "success": mark_safe(
            "درخواست شما با موفقیت ثبت شد.<br/> درصورت عدم انجام تسویه حساب تا ۷۲ ساعت آینده با دفتر شورای صنفی تماس بگیرید."),
        "done": True
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def charge_cash(request):
    amount = None
    student_number = None
    if request.POST:
        form = FormWithCaptcha(request.POST)
        if not form.is_valid():
            return render(request, "charge_cash.html", {
                "completed": False,
                "error": "لطفا تیک من ربات نیستم را بزنید.",
                "form": FormWithCaptcha()
            })
        try:
            amount = int(request.POST.get("amount"))
            student_number = int(request.POST.get("student_number"))
        except:
            return render(request, "charge_cash.html", {
                "completed": False,
                "error": "فرمت اطلاعات فرستاده شده درست نیست.",
                "form": FormWithCaptcha()
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
                "success": "اعتبار %s به میزان %d تومان افزایش یافت." % (member.get_full_name(), amount),
                "form": FormWithCaptcha()
            })

        return render(request, "charge_cash.html", {
            "completed": False,
            "error": "دانشجو با شمارهٔ دانشجویی وارد شده یافت نشد.",
            "form": FormWithCaptcha(),
        })

    return render(request, "charge_cash.html", {
        "completed": False,
        "form": FormWithCaptcha()
    })


@login_required
def charge_credit(request):
    amount = None
    if request.POST:
        captcha = FormWithCaptcha(request.POST)
        if not captcha.is_valid():
            return render(request, "charge_online.html", {
                "completed": False,
                "error": "لطفا تیک من ربات نیستم را بزنید.",
                "form": FormWithCaptcha()
            })

        try:
            amount = int(request.POST.get("amount"))
            valid_amounts = [5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 100000]
            if amount not in valid_amounts:
                return render(request, "charge_online.html", {
                    "completed": False,
                    "error": "مبلغ وارد شده معتبر نمی‌باشد.",
                    "form": FormWithCaptcha()
                })
        except:
            return render(request, "charge_online.html", {
                "completed": False,
                "error": "فرمت اطلاعات فرستاده شده درست نیست.",
                "form": FormWithCaptcha()
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
            "error": "اطلاعات شما در دیتابیس به درستی ثبت نشده است.",
            "form": FormWithCaptcha()
        })

    return render(request, "charge_online.html", {
        "completed": False,
        "form": FormWithCaptcha()
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


@login_required
def history(request):
    member = Member.objects.get(username=request.user.username)
    transactions = list(reversed(Transaction.objects.filter(Q(destination=member) | Q(origin=member))))

    return render(request, "history.html", {
        "transactions": transactions,
        "noTransaction": len(transactions) == 0,
        "member": member
    })

from .models import rack,sell
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
#from suds.client import Client
from zeep import Client
import json
from django.utils import timezone



@login_required
def lock(request):
    theRacks = rack.objects.filter(receiver=request.user)
    racks = rack.objects.all()
    user = request.user
    return render(request,'locker.html',{ 'racks':racks,'theRacks':theRacks , 'user':user })

@login_required
def add_new(request):
    if request.method == "POST":
        name = request.POST.get('locker-name')
        if rack.objects.filter(name__contains=name):
            if rack.objects.get(name=name).payment == True:
                return HttpResponse('has chosen before')
            else:
                Rack = rack.objects.get(name=name)
                if sell.objects.filter(locker=Rack):
                    Sell = sell.objects.get(locker=rack.objects.get(name=name),is_success=False)
                    if Rack.payment == True:
                        return HttpResponse('on payment')
                    else:
                        Rack.receiver = request.user
                        Rack.save()
                        Sell.user = request.user
                        Sell.locker = Rack
                        Sell.tried = True
                        Sell.save()
                        return render(request,'confirmation.html',{'rack':Rack})
                else:
                    Sell = sell(user=request.user,locker=Rack,is_success=False,tried=True)
                    Sell.save()
                    return render(request,'confirmation.html',{'rack':Rack})

        else:
            user = request.user
            Rack = rack(name=name,receiver=user,payment=False,receivie_date=timezone.now(),condition=0)
            Rack.save()
            if sell.objects.filter(locker=Rack):
                Sell = sell.objects.get(locker=Rack)
                Sell.tried = True
                Sell.save()
            else:
                Sell = sell(locker=Rack,user=request.user,tried=True)
                Sell.save()
            return render(request,'confirmation.html',{'rack':Rack})
    else :
        return HttpResponse('You choose badway !')


url = "https://www.zarinpal.com/pg/services/WebGate/wsdl"
client = Client(url)
MERCHANT = '0f3e8346-d100-11e8-b90d-005056a205be'

def payment(request, rack_id):
    Rack = get_object_or_404(rack, id=rack_id)
    if request.method == "POST":
        if Rack.payment==True:
            return HttpResponse('someone else is on payment')
        moneyt = 40000
        Sell = sell(value=moneyt, locker=Rack, is_success=False,tried=True)
        if request.user.is_authenticated:
            Sell.user = request.user
        Sell.save()
        site_name = request.META.get('HTTP_HOST', 'shora.ce.sharif.edu')
        url = "https://www.zarinpal.com/pg/services/WebGate/wsdl"
        client = Client(url)
        callBackUrl = "http://%s/locker/payment-result/" % (site_name)
        s = client.service.PaymentRequest(MERCHANT, 40000, "receive locker "+str(Sell.locker.name),'', "",callBackUrl)
        Sell.authority = s.Authority
        Sell.save()
        print(s , Sell.authority , site_name)
        if s.Status == 100:
            Rack.payment = True
            Rack.save()
            return redirect("https://www.zarinpal.com/pg/StartPay/"+str(s.Authority))
        else:
            return HttpResponse(s.Status)

    return HttpResponse("Badway!")  # Todo Login page ~

def payment_result(request):
    try:
        Sell = sell.objects.get(authority=request.GET.get('Authority'))
    except sell.DoesNotExist:
        raise Http404
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET.get('Authority'), 40000)
        if result.Status == 100:
            try:
                Sell = sell.objects.get(authority=request.GET.get('Authority'))
            except sell.DoesNotExist:
                raise Http404
            ref_num = str(result.RefID)
            if not ref_num:
                raise PermissionDenied
            Sell.is_success = True
            Sell.locker.payment = True
            Sell.save()
            Sell.locker.save()
            return render(request, 'success.html', {'sell': Sell})
        elif result.Status == 101:
            Sell.tried = False
            Sell.is_success = False
            Sell.locker.name = 'Non'
            Sell.locker.payment = False
            Sell.locker.save()
            Sell.save()
            return render(request, 'success.html', {'sell': Sell})
        else:
            Sell.tried = False
            Sell.locker.name = 'Non'
            Sell.is_success = False
            Sell.locker.payment = False
            Sell.locker.save()
            Sell.save()
            return render(request, 'success.html', {'sell': Sell})
    else:
        Sell.tried = False
        Sell.is_success = False
        Sell.locker.payment = False
        Sell.locker.name = 'Non'
        Sell.locker.save()
        Sell.save()
        return render(request, 'success.html', {'sell': Sell})

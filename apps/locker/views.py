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
    Racks = rack.objects.all()
    return render(request,'locker.html',{ 'racks':Racks })

@login_required
def add_new(request):
    if request.method == "POST":
        name = request.POST.get('locker-name')
        if rack.objects.filter(name__contains=name) :
            if rack.objects.get(name__contains=name).receiver == request.user:
                if rack.objects.get(name__contains=name).payment:
                    return HttpResponse(" This locker is yours :) ")
                else :
                    return render(request,'confirmation.html',{'rack':rack.objects.get(name__contains=name)})
            else:
                return HttpResponse('this locker has been chosen before sorry!')
        else :
            user = request.user
            Rack = rack(name=name,receiver=user,payment=False,receivie_date=timezone.now(),condition=0)
            Rack.save()
            return render(request,'confirmation.html',{'rack':Rack})
    else:
        return HttpResponse('You choose badway !')


url = "https://www.zarinpal.com/pg/services/WebGate/wsdl"
client = Client(url)
MERCHANT = 'e0d2334e-86fb-11e7-af91-000c295eb8fc'


def payment(request, rack_id):

    if request.method == "POST":
        moneyt = 1000
        Rack = get_object_or_404(rack, id=rack_id)
        Sell = sell(value=moneyt, locker=Rack, is_success=False)
        if request.user.is_authenticated:
            Sell.user = request.user
        Sell.save()
        site_name = request.META.get('HTTP_HOST', 'shora.ce.sharif.edu')
        url = "https://www.zarinpal.com/pg/services/WebGate/wsdl"
        client = Client(url)
        callBackUrl = "http://%s/locker/payment-result/" % (site_name)
        s = client.service.PaymentRequest(MERCHANT, 1000, "receive locker "+str(Sell.locker.name),'', "",callBackUrl)
        Sell.authority = s.Authority
        Sell.save()
        print(s , Sell.authority , site_name)
        if s.Status == 100:
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
        result = client.service.PaymentVerification(MERCHANT, request.GET.get('Authority'), 1000)
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
            return render(request, 'success.html', {'sell': Sell})
        else:
            return render(request, 'success.html', {'sell': Sell})
    else:
        return render(request, 'success.html', {'sell': Sell})


#@csrf_exempt
#def payment_result(request, sell_id):
#    if not request.method == "POST":
#        raise PermissionDenied
#    try:
#        Sell = sell.objects.get(id=int(sell_id))
#    except Sell.DoesNotExist:
#        raise PermissionDenied # # TODO: Http404
#    if not request.POST.get('resnumber') == Sell.get_code():
#        raise PermissionDenied
#    ref_num = request.POST.get('RefID')
#    if not ref_num:
#        raise PermissionDenied
#    verify_payment(Sell, ref_num)
#    if Sell.is_success:
#        Sell.save()
#    return render(request, 'payment_result.html', {'sell': Sell})





#def verify_payment(Sell, ref_num):
#    url = "http://www.zarinpal.com/pg/services/WebGate/wsdl"
#    client = Client(url)
#    MERCHANT = 'e0d2334e-86fb-11e7-af91-000c295eb8fc'
#    s = client.service.PaymentVerification(MERCHANT, Sell.value, ref_num)
#    status = s.Status
#    price = s.PayementedPrice
#    Sell.credit = int(price)
#    Sell.is_success = (status == "Verifyed" or status == "success")
#    Sell.save()

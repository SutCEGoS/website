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
        if rack.objects.filter(name__contains=name):
            return HttpResponse('this locker has been chosen before sorry!')
        else:
            user = request.user
            Rack = rack(name=name,receiver=user,payment=False,receivie_date=timezone.now(),condition=0)
            Rack.save()
            return render(request,'rackForm.html',{'rack':Rack})
    else:
        return HttpResponse('You choose badway !')




def payment(request, rack_id):

    if request.method == "POST":
        moneyt = 20000
        Rack = get_object_or_404(rack, id=rack_id)
        Sell = sell(value=moneyt, locker=Rack, is_success=False)
        if request.user.is_authenticated:
            Sell.user = request.user
        Sell.save()
        site_name = request.META.get('HTTP_HOST', 'shora.sabbaghian.ir')
        url = "http://www.zarinpal.com/pg/services/WebGate/wsdl"
        client = Client(url)
        s = client.service.PaymentRequest('11380930-2456-11e8-8cb6-005056a205be', 20000, "", "",
                                          "",
                                          "http://%s/locker/payment-result/%s" % (site_name, str(Rack.id)))
        print(s)
        if s.Status == 100:
            return redirect("//http//:www.zarinpal.com/pg/StartPay/"+str(s.Authority))
        else:
            return HttpResponse(s.Status)

    return HttpResponse("Badway!")  # Todo Login page ~


@csrf_exempt
def payment_result(request, sell_id):
    if not request.method == "POST":
        raise PermissionDenied
    try:
        Sell = sell.objects.get(id=int(sell_id))
    except Sell.DoesNotExist:
        raise PermissionDenied # # TODO: Http404
    if not request.POST.get('resnumber') == Sell.get_code():
        raise PermissionDenied
    ref_num = request.POST.get('RefID')
    if not ref_num:
        raise PermissionDenied
    verify_payment(Sell, ref_num)
    if Sell.is_success:
        Sell.save()
    return render(request, 'payment_result.html', {'sell': Sell})





def verify_payment(Sell, ref_num):
    url = "http://www.zarinpal.com/pg/services/WebGate/wsdl"
    client = Client(url)
    s = client.service.PaymentVerification("11380930-2456-11e8-8cb6-005056a205be", Sell.value, ref_num)
    status = s.Status
    price = s.PayementedPrice
    Sell.credit = int(price)
    Sell.is_success = (status == "Verifyed" or status == "success")
    Sell.save()

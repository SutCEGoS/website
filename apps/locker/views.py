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


def calculate_difference(x,y):
    day = y.day-x.day
    hour = y.hour-x.hour
    minute = y.minute-x.minute
    return day*24*60+hour*60+minute


@login_required
def lock(request):
    theRacks = rack.objects.filter(receiver=request.user)
    broken_lockers = ['A23', 'A42', 'B13', 'B22', 'B23', 'B32', 'B41', 'C21',
            'C41', 'D11', 'D12', 'D23', 'E11', 'E12', 'E13', 'E21', 'E22',
            'E41', 'E42', 'F11', 'F12', 'F13', 'F21', 'F23', 'F32', 'F41',
            'F42', 'F43', 'G11', 'G12', 'G13', 'G22', 'G41', 'G42', 'G43',
            'H11', 'H12', 'H23', 'H33', 'H42', 'I23', 'I33', 'J11', 'J12',
            'J13', 'J21', 'J23', 'J41', 'K11', 'K12', 'K21', 'K22', 'K23',
            'K32', 'L13', 'L22', 'L31', 'L32', 'L33', 'L42', 'L43', 'O11',
            'O12', 'O13', 'O21', 'O31', 'O33', 'N13', 'N21', 'N22', 'N23',
            'N32', 'N33', 'N41', 'Q11', 'Q12', 'Q21', 'Q22', 'Q31', 'Q32',
            'Q33', 'Q41', 'Q42', 'P13', 'P21', 'P22', 'P23', 'P31', 'P33',
            'P42', 'P43',]
    racks = rack.objects.all()
    for track in racks:
        if sell.objects.filter(locker=track):
            if track.payment == True:
                if sell.objects.filter(locker=track,is_success=False):
                    if calculate_difference(track.receivie_date,timezone.now()) > 10:
                        track.payment = False
                        track.save()
            elif track.payment == False:
                for tsell in sell.objects.filter(locker=track):
                    tsell.is_success = False
                    tsell.save()


    user = request.user
    return render(request,'locker.html',{ 'racks':racks,'theRacks':theRacks , 'user':user,
        'broken_lockers': broken_lockers})

@login_required
def add_new(request):
    if request.method == "POST":
        name = request.POST.get('locker-name')
        if rack.objects.filter(name__contains=name):
            if rack.objects.get(name=name).payment == True:
                return HttpResponse('has chosen before')
            else:
                Rack = rack.objects.get(name=name)
                Sell = sell(user=request.user,locker=Rack,is_success=False)
                Rack.receiver=request.user
                Rack.receivie_date = timezone.now()
                Rack.save()
                return render(request,'confirmation.html',{'rack':Rack})
        else:
            user = request.user
            Rack = rack(name=name,receiver=user,payment=True,receivie_date=timezone.now())
            Rack.save()
            if sell.objects.filter(locker=Rack):
                Sell = sell.objects.get(locker=Rack)
                Sell.is_success = False
                Sell.save()
            else:
                Sell = sell(locker=Rack,user=request.user)
                Sell.is_success = False
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
        if Rack.payment==True and Rack.receiver != request.user:
            return HttpResponse('someone else is on payment for this locker')
        moneyt = 40000
        Sell = sell(value=moneyt, locker=Rack, is_success=False)
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
            Sell.save()
            return render(request, 'success.html', {'sell': Sell})
        elif result.Status == 101:
            Sell.is_success = False
            Sell.locker.name = 'Non'
            Sell.locker.save()
            Sell.save()
            return render(request, 'success.html', {'sell': Sell})
        else:
            Sell.locker.name = 'Non'
            Sell.is_success = False
            Sell.locker.save()
            Sell.save()
            return render(request, 'success.html', {'sell': Sell})
    else:
        Sell.is_success = False
        Sell.locker.name = 'Non'
        Sell.locker.save()
        Sell.save()
        return render(request, 'success.html', {'sell': Sell})

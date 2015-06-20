# coding=utf-8
import json
import logging

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from suds.client import Client

from event.models import Event, EventRegister, Donate


def all_events(request):
    events = Event.objects.order_by('-id')

    return render(request, 'event/events.html', {
        'events': events,
    })


def get_event(request):
    event_id = request.POST.get('event-id')
    event = get_object_or_404(Event, id=event_id)
    if request.user.is_authenticated():
        std_id = request.user.std_id or request.user.username
        has_registered = event.registered(std_id)
    else:
        has_registered = False
    return render(request, 'event/event.html', {
        'event': event,
        'has_registered': has_registered,
    })


def register_in_event(request):
    data = {}
    if not request.is_ajax():
        raise Http404
    error = ""
    event_id = request.POST.get('event-id')
    selected_event = get_object_or_404(Event, id=event_id)
    if request.user.is_authenticated():
        std_id = request.user.std_id or request.user.username
    else:
        std_id = request.POST.get('std-id')
    if not std_id:
        error = u"لطفا شماره دانشجویی خود را وارد کنید"
    else:
        if not selected_event.active:
            raise PermissionDenied
        if selected_event.registered(std_id):
            error = u"شما قبلا در این رویداد ثبت نام کرده اید."
        if error is '':
            EventRegister.objects.create(event=selected_event, std_id=std_id)
    data.update({'error': error,
                 'count': selected_event.get_count(), })
    return HttpResponse(json.dumps(data), content_type='application/json')


def make_donate_url(d, site_name, event):
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)

    url = "http://merchant.parspal.com/WebService.asmx?wsdl"
    client = Client(url)
    s = client.service.RequestPayment("3368002", "m7Twb3C1E", d.value, event.name, "",
                                      "", "", d.get_code(),
                                      "http://%s/events/payment-result/%s" % (site_name, str(d.id)))
    if s.ResultStatus == 'Succeed':
        return s.PaymentPath
    return ""


def verify_payment(d, ref_num):
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)

    url = "http://merchant.parspal.com/WebService.asmx?wsdl"
    client = Client(url)
    s = client.service.verifyPayment("3368002", "m7Twb3C1E", d.value, ref_num)
    status = s.ResultStatus
    price = s.PayementedPrice
    d.credit = int(price)
    d.is_success = (status == "Verifyed" or status == "success")
    d.save()


def payment(request, event_id):
    if request.method == "POST":
        moneyt = request.POST.get('donate-value')
        event = get_object_or_404(Event, id=event_id)
        donate_obj = Donate(value=moneyt, event=event)
        if request.user.is_authenticated():
            donate_obj.user = request.user
        name = request.POST.get('donate-name')
        if name:
            donate_obj.name = name
        donate_obj.save()
        site_name = request.META.get('HTTP_HOST', 'shora.sabbaghian.ir')
        url = make_donate_url(donate_obj, site_name, event)
        if url:
            return redirect(url)
    else:
        return HttpResponse("Badway!")  # Todo Login page ~


@csrf_exempt
def payment_result(request, donate_id):
    if not request.method == "POST":
        raise PermissionDenied
    try:
        d = Donate.objects.get(id=int(donate_id))
    except Donate.DoesNotExist:
        raise Http404
    if not request.POST.get('resnumber') == d.get_code():
        raise PermissionDenied
    ref_num = request.POST.get('refnumber')
    if not ref_num:
        raise PermissionDenied
    verify_payment(d, ref_num)
    if d.is_success:
        d.save()
    return render(request, 'payment_result.html', {'donate_obj': d})

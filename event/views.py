# coding=utf-8
import json

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

from event.models import Event, EventRegister


def all_events(request):
    events = Event.objects.all()  # order_by('-active', '-id')

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

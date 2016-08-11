# coding=utf-8
import json

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Poll, PollChoice, Vote


def all_polls(request):
    polls = Poll.objects.filter(is_active=True).order_by('-id')

    return render(request, 'polls.html', {
        'polls': polls,
    })


def get_poll(request):
    poll_id = request.POST.get('poll_id')
    poll = get_object_or_404(Poll, id=poll_id)
    poll_choices = PollChoice.objects.filter(poll=poll)
    has_voted = False
    if request.user.is_authenticated():
        has_voted = request.user.has_voted(poll)
    return render(request, 'poll.html', {
        'poll_question': poll,
        'poll_choices': poll_choices,
        'has_voted': has_voted,
    })


def submit_vote(request):
    data = {}
    if not request.is_ajax():
        raise Http404
    error = ""
    if not request.POST.get('poll-choice'):
        error = u"لطفا یکی از گزینه ها را انتخاب کنید."
    try:
        poll_choice = PollChoice.objects.get(id=request.POST.get('poll-choice'))
    except PollChoice.DoesNotExist:
        poll_choice = None
        if error is "":
            error = u"ثبت نظر امکان پذیر نمی باشد. لطفا مجددا تلاش فرمایید."
    if poll_choice and not error:
        if not poll_choice.poll.active:
            raise PermissionDenied
        comment = request.POST.get('comment')
        v = Vote(choice=poll_choice,
                 comment=comment,
                 ip=request.META['REMOTE_ADDR'], )
        if request.user.is_authenticated():
            if request.user.has_voted(poll_choice.poll):
                error = u"شما قبلا در این نظرسنجی شرکت کرده اید."
            v.member = request.user
            v.save()
        else:
            username = request.POST.get('username')
            v.username = username
            v.save()
        if error is '':
            v.save()
            data.update({'id': poll_choice.poll.id})
    data.update({'error': error})
    return HttpResponse(json.dumps(data), content_type='application/json')

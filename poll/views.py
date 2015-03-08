from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from poll.models import Poll, PollChoice, Vote


@login_required
def all_polls(request):
    polls = Poll.objects.order_by('-is_active', '-id')

    return render(request, 'poll/polls.html', {
        'polls': polls,
    })


@login_required
def get_poll(request):
    poll_id = request.POST.get('poll_id')
    poll = get_object_or_404(Poll, id=poll_id)
    poll_choices = PollChoice.objects.filter(poll=poll)
    has_voted = Vote.objects.filter(member=request.user, choice__poll=poll).exists()
    return render(request, 'poll/poll.html', {
        'poll_question': poll,
        'poll_choices': poll_choices,
        'has_voted': has_voted,
    })


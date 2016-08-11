from django.http import Http404
from django.shortcuts import render

from vendor.shamsi.templatetags.shamsi_template_tags import pdatetime
from .models import Announcement


# Create your views here.

def all_announcements(request):
    announcements = Announcement.objects.order_by('-id')
    for an in announcements:
        an.date = pdatetime(an.date)

    return render(request, 'announcements.html', {
        'announcements': announcements,
    })


def show_announcement(request, announcement_id):
    try:
        announcement = Announcement.objects.get(pk=announcement_id)
        announcement.date = pdatetime(announcement.date)

    except Announcement.DoesNotExist:
        raise Http404("Announcement does not exist")

    return render(request, 'announcement.html', {
        'announcement': announcement,
    })

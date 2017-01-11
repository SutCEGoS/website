from django.http import Http404
from django.shortcuts import render, get_object_or_404

from apps.announcements.models import AnnouncementView
from vendor.shamsi.templatetags.shamsi_template_tags import pdatetime
from .models import Announcement


def all_announcements(request):
    announcements = Announcement.objects.all()[:10]

    return render(request, 'announcements.html', {
        'announcements': announcements,
    })


def show_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, pk=announcement_id)

    announcement.register_view(request.user)
    return render(request, 'announcement.html', {
        'announcement': announcement,
    })

from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .models import Link


def page_visit(request, slug):
    link = get_object_or_404(Link, slug=slug, enabled=True)

    if not link.enabled or (link.login_required and not request.user.is_authenticated()):
        raise Http404

    if request.user.is_authenticated():
        link.visit(request.user)
    else:
        link.visit(None)

    if link.type == 1:
        return HttpResponseRedirect(link.url)

    return render(request, 'pages/frame_page.html', {
        'link_title': link.title,
        'link_url': link.url,
    })

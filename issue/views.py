import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest

from issue.forms import IssueForm
from issue.models import Issue
from objection.models import Objection


@login_required
def requests(request):
    form = IssueForm()

    user_email = request.user.email

    params = {
        'form': form,
        'user_email': user_email
    }

    return render(request, 'issues.html', params)


@login_required
def search_issue(request):
    if request.method != 'GET':
        return HttpResponseBadRequest
    if not request.user.is_authenticated:
        raise PermissionDenied
    search_result = Issue.get_available(request.user)
    obj_id = request.GET.get('id')
    if obj_id:
        obj_id = int(obj_id)
        obj = get_object_or_404(Objection, pk=obj_id)
        if obj in search_result:
            return HttpResponse(json.dumps([obj.get_serialized(request.user)]), content_type="application/json")
        raise PermissionDenied
    category = request.GET.get('category')
    category = int(category) if category else category

    if category:
        search_result = search_result.filter(category=category)
    search_result = search_result.order_by('-id')
    objections_list = []
    for item in search_result:
        objections_list.append(
            item.get_serialized(request.user)
        )
    return HttpResponse(json.dumps(objections_list), content_type="application/json")


@login_required
def add_issue(request):
    data = request.POST.copy()
    data['sender'] = request.user.id
    data['status'] = 1
    form = IssueForm(data=data)
    if form.is_valid():
        f = form.save()
        x = f.get_serialized(request.user)
        return HttpResponse(json.dumps(x), content_type="application/json")
    else:
        x = dict(form.errors).values()
        return HttpResponse(json.dumps(x), content_type="application/json", status=400)


@login_required
def add_me_too(request):
    item_id = request.POST.get('data_id')
    try:
        item_id = int(item_id)
    except ValueError:
        return HttpResponse(status=400)  # Thank you amin

    item = get_object_or_404(Issue, pk=item_id)
    available_items = Issue.get_available(request.user)
    if item not in available_items:
        raise PermissionDenied
    if item.sender.__eq__(request.user):
        raise PermissionDenied
    if request.user in item.like.all():
        me_too_ed = False
        item.like.remove(request.user)
    else:
        me_too_ed = True
        item.like.add(request.user)
    retrurn_obj = {
        'metooed': me_too_ed,
        'metoos': item.like.count()
    }
    return HttpResponse(json.dumps(retrurn_obj), content_type="application/json")

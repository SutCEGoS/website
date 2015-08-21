# coding=utf-8
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest

from course.models import OfferedCourse
from course.views import get_current_year
from objection.forms import MessageForm
from objection.models import Objection


@login_required
def requests(request):
    form = MessageForm()

    user_email = request.user.email

    params = {
        'form': form,
        'user_email': user_email
    }

    return render(request, 'messages.html', params)


@login_required
def search(request):
    if request.method != 'GET':
        return HttpResponseBadRequest
    if not request.user.is_authenticated:
        raise PermissionDenied
    search_result = Objection.get_available(request.user)
    obj_id = request.GET.get('id')
    if obj_id:
        obj_id = int(obj_id)
        obj = get_object_or_404(Objection, pk=obj_id)
        if obj in search_result:
            return HttpResponse(json.dumps([obj.get_serialized(request.user)]), content_type="application/json")
        raise PermissionDenied
    category = request.GET.get('category')
    offered_course = request.GET.get('offered_course')
    second_course = request.GET.get('second_course')
    course_name = request.GET.get('course_name')

    category = int(category) if category else category
    offered_course = int(offered_course) if offered_course else offered_course
    second_course = int(second_course) if second_course else second_course

    if offered_course and not second_course and category in [2, 4, 5, 6]:
        search_result = search_result.filter(offered_course__id=offered_course)
    if offered_course and second_course and category == 1:
        search_result = search_result.filter(
            Q(offered_course__id=offered_course, second_course__id=second_course) |
            Q(offered_course__id=second_course, second_course__id=offered_course))

    if course_name and category == 3:
        search_result = search_result.filter(course_name=course_name)

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
def get_courses(request):
    if request.method != 'GET':
        return HttpResponseBadRequest
    if not request.user.is_authenticated:
        raise PermissionDenied
    courses_list = {}
    for course in OfferedCourse.objects.filter(term=settings.CURRENT_TERM, year=get_current_year()):
        courses_list.update({
            course.id: {
                'course_name': course.course.name,
                'course_number': course.course.course_number,
                'professor': course.professor.name,
                'group_number': course.group_number,
                'exam_time': course.exam_time,
                'capacity': course.capacity,
                'details': course.details,
            }
        })
    return HttpResponse(json.dumps(courses_list), content_type="application/json")


@login_required
def add_objection(request):
    # category = request.POST.get('category')
    # offered_course = request.POST.get('offered_course')
    # second_course = request.POST.get('second_course')
    # course_name = request.POST.get('course_name')
    # message = request.POST.get('message')
    data = request.POST.copy()
    data['sender'] = request.user.id
    data['status'] = 1
    data['term'] = settings.CURRENT_TERM
    data['year'] = get_current_year().id
    form = MessageForm(data=data)
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

    item = get_object_or_404(Objection, pk=item_id)
    available_items = Objection.get_available(request.user)
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

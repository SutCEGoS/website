# coding=utf-8
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest

from course.models import OfferedCourse
from course.views import get_current_year
from objection.forms import MessageForm
from objection.models import Objection


@login_required
def requests(request):
    result = ''
    result_type = False
    params = {}
    form = MessageForm()

    params = {
        'form': form,
        'messages': Objection.objects.filter().order_by('reply').reverse()  # FIXME: fuck
    }

    return render(request, 'messages.html', params)

@login_required
def search(request):
    if request.method != 'GET':
        return HttpResponseBadRequest
    if not request.user.is_authenticated:
        raise PermissionDenied
    search_result = Objection.get_available(request.user)
    category = request.GET.get('category')
    offered_course = request.GET.get('offered_course')
    second_course = request.GET.get('second_course')
    course_name = request.GET.get('course_name')
    if category:
        search_result = search_result.filter(category=request.GET)
    if offered_course:
        search_result = search_result.filter(offered_course__id=offered_course)
    if second_course:
        search_result = search_result.filter(second_course__id=second_course)
    if course_name:
        search_result = search_result.filter(course_name=course_name)
    objections_list = []
    for item in search_result:
        objections_list.append({
            'category': item.get_category_display(),
            'status': item.get_status_display(),
            'likes_num': item.like.count(),
            'offered_course': item.offered_course.id,
            'second_course': item.second_course.id,
            'course_name': item.course_name,
            'message': item.message,
        })
    return HttpResponse(json.dumps({'list': objections_list}), content_type="application/json")

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

# coding=utf-8
import urllib2
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseBadRequest
from objection.forms import MessageForm
from objection.models import Objection
import json


def requests(request):
    result = ''
    result_type = False
    params = {}
    form = MessageForm()

    params = {
        'form': form,
        'messages': Objection.objects.filter().order_by('reply').reverse() # FIXME: fuck
    }

    return render(request, 'message.html', params)


def search(request):
    if request.method != 'GET':
        raise HttpResponseBadRequest

    form = MessageForm(request.POST)
    if form.is_valid():
        form.save()

        # FIXME: make these messages in semora json format
        result = u'پیغام شما با موفقیت ثبت گردید  و پس از تایید به نمایش درخواهد آمد. باتشکر از شما'
    else:
        # FIXME: make these messages in semora json format
        result = u'لطفا فرم را با دقت پر نمایید. پر کردن فیلهای ستاره دار الزامی است. برحسب نوع مشکل انتخابی، پرکردن فیلدهای دیگر نیز الزامی است.'

    return HttpResponse(json.dumps(result), content_type="application/json")


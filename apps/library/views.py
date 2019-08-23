from django.shortcuts import render
from django.http import HttpResponse


def library_index(request):
    return HttpResponse("salam")

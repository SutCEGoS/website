from django.shortcuts import render
from .models import rack
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import rackForm
import json




# Create your views here.
@login_required
def lock(request):
    Form = rackForm()
    user = request.user
    return render(request,'locker.html', {
            'form' : Form,
            'user' : user,
    })
@login_required
def add(request):
    data = request.POST.copy()
    data['receiver'] = request.user if request.user.is_authenticated() else None
    form = IssueForm(data=data)
    if form.is_valid():
        f = form.save()
        x = f.get_serialized(request.user)
        return HttpResponse(json.dumps(x), content_type="application/json")
    else:
        x = dict(form.errors).values()
        return HttpResponse(json.dumps(x), content_type="application/json", status=400)

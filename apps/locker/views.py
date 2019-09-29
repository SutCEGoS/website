from .models import Rack, sell
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
import re

price = 50000


def calculate_difference(x, y):
    day = y.day - x.day
    hour = y.hour - x.hour
    minute = y.minute - x.minute
    return day * 24 * 60 + hour * 60 + minute


@login_required
def lock(request):
    theRacks = Rack.objects.filter(receiver=request.user)
    broken_lockers = ['A42', 'B23', 'B41',
                      'D11',
                      'F42', 'G12', 'G22', 'G42', 'G43',
                      'H12', 'J12',
                      'K23',
                      'K32', 'K42',
                      'O13', 'N22',
                      'N32', 'N41', 'Q21',
                      'P13', 'P22', 'P23', 'P31',
                      ]
    racks = Rack.objects.all()
    for track in racks:
        if sell.objects.filter(locker=track):
            if track.payment == True:
                if sell.objects.filter(locker=track, is_success=False):
                    if calculate_difference(track.receivie_date, timezone.now()) > 10:
                        track.payment = False
                        track.save()
            elif track.payment == False:
                for tsell in sell.objects.filter(locker=track):
                    tsell.is_success = False
                    tsell.save()

    user = request.user
    return render(request, 'locker.html', {'racks': racks, 'theRacks': theRacks, 'user': user,
                                           'broken_lockers': broken_lockers})


@login_required
def lock_disable(request):
    return render(request, 'locker_disable.html')


@login_required
def add_new(request):
    if request.method == "POST":
        name = request.POST.get('locker-name')
        rack_status = Rack.get_rack_status(rack_name=name)
        if rack_status == 0:
            pass

        return render(request, "success.html", {
            "status": 4  # rack_status
        })
    else:
        return render(request, "success.html", {
            "status": -1
        })

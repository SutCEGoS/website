from django.http import HttpResponse

from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

price = 45000


def calculate_difference(x, y):
    day = y.day - x.day
    hour = y.hour - x.hour
    minute = y.minute - x.minute
    return day * 24 * 60 + hour * 60 + minute


@login_required
def lock(request):
    if not request.user.is_staff:
        return render(request, 'locker_disable.html')

    theRacks = Rack.objects.filter(receiver=request.user, archived=False)
    broken_lockers = ['A42',
                      'B23', 'B41',
                      'D11',
                      'F42',
                      'G12', 'G22', 'G42', 'G43',
                      'H12',
                      'J12',
                      'K23', 'K32', 'K42',
                      'N22', 'N32', 'N41',
                      'O13',
                      'P13', 'P22', 'P23', 'P31',
                      'Q21',

                      # new broken lockers
                      'A21', 'A23',
                      'C21', 'C31', 'C33', 'C42', 'C43',
                      'D12', 'D13',
                      'E42', 'E22',
                      'G21', 'G43',
                      'H32', 'H42', 'H22',
                      'I21', 'I23', 'I31', 'I42',
                      'J22', 'J32',
                      'K43', 'K22', 'K11',
                      'L11', 'L12', 'L23', 'L33', 'L43',
                      'N12',
                      'O12', 'O22', 'O23', 'O31', 'O33', 'O32', 'O41',
                      'P12', 'P33',
                      'Q13',
                      ]
    racks = Rack.objects.filter(archived=False)


    user = request.user
    return render(request, 'locker.html', {'racks': racks, 'theRacks': theRacks, 'user': user,
                                           'broken_lockers': broken_lockers})


@login_required
def add_new(request):
    if request.method == "POST":
        locker_name = request.POST.get('locker-name')
        rack_status = Rack.get_rack_status(rack_name=locker_name)
        if rack_status == 0:
            member = Member.objects.get(username=request.user.username)
            if member.cash < price:  # cash is not enough
                return render(request, "success.html", {
                    "status": 4
                })

            member.cash -= price
            transaction = Transaction(origin=member, type=4, amount=price, is_successfully=True, data=locker_name)
            transaction.save()
            member.save()
            rack = Rack(name=locker_name, receiver=member, payment=True, transaction=transaction, condition=1, archived=False)
            rack.save()

        return render(request, "success.html", {
            "status": rack_status
        })
    else:
        return render(request, "success.html", {
            "status": -1
        })


@login_required
def archive(request):
    if request.user.is_staff and request.user.is_superuser:
        name = request.GET.get("name")
        if name is None:
            return HttpResponse("Bad request", status=400)
        rack = Rack.objects.get(name=name)
        if rack is not None:
            rack.archived = True
            rack.save()
            return HttpResponse("Rack archived", status=200)
        else:
            return HttpResponse("Rack not found", status=406)
    else:
        return HttpResponse("access denied", status=403)
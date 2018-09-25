from django.shortcuts import render
from .models import locker,rack
# Create your views here.

def lock(request):
    lockers = locker.objects.all()
    racks_row1 = rack.objects.all()[:3]
    racks_row2 = rack.objects.all()[3:6]
    racks_row3 = rack.objects.all()[6:9]
    return render(request,'locker.html',{   'lockers':lockers ,
                                            'racks1':racks_row1 ,
                                            'racks2':racks_row2 ,
                                            'racks3':racks_row3,
                                              })
def show_locker_condition(request, locker_id):
    theLocker = get_object_or_404(locker, pk=locker_id)

    return render(request, 'lockerCondition.html', {
        'locker': theLocker,
    })

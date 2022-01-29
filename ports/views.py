from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from ports.models import Port


# Create your views here.

def ports_main(request):
    ports_list = Port.objects.all()
    return render(request, 'ports/index.html', {
        'ports_list': ports_list
    })


def ports_add(request):
    if request.method == 'POST':
        i_port_name = request.POST['port_name']
        i_temp = request.POST['temperature']
        i_latitude = request.POST['latitude']
        i_longitude = request.POST['longitude']
        is_valid, error_msg = valid_data(i_port_name, i_temp, i_latitude, i_longitude)
        if not is_valid:
            return render(request, 'ports/add.html', {
                'has_error': True,
                'error_msg': error_msg
            })
        new_port = Port(port_name=i_port_name, temperature=i_temp, latitude=i_latitude, longitude=i_longitude)
        new_port.save()
        resolved_path = reverse('ports-index', args=[])
        return HttpResponseRedirect(resolved_path)

    return render(request, 'ports/add.html', {
        'has_error': False
    })


def valid_data(i_port_name, i_temp, i_latitude, i_longitude):
    if int(i_temp) <= -30 or int(i_temp) >= 30:
        return False, 'Temperature should be between -30 and 30'
    if int(i_latitude) <= -180 or int(i_latitude) >= 180:
        return False, 'Latitude values should be between -180 and 180'
    if int(i_longitude) <= -90 or int(i_longitude) >= 90:
        return False, 'Longitude values should be between -90 and 90'

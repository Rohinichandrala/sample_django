from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.urls import reverse
from ports.models import Port
from .add_form import AddForm
from django.template.loader import render_to_string


# Create your views here.

def ports_main(request):
    ports_list = Port.objects.all()
    return render(request, 'ports/index.html', {
        'ports_list': ports_list
    })


def ports_add(request):
    try:
        has_error = False
        if request.method == 'POST':
            form = AddForm(request.POST)
            if form.is_valid():
                i_port_name = form.cleaned_data.get('port_name')
                i_temp = form.cleaned_data.get('temperature')
                i_latitude = form.cleaned_data.get('latitude')
                i_longitude = form.cleaned_data.get('longitude')
                new_port = Port(port_name=i_port_name, temperature=i_temp,
                                latitude=i_latitude, longitude=i_longitude)
                new_port.save()
                resolved_path = reverse('ports-index', args=[])
                return HttpResponseRedirect(resolved_path)
            else:
                has_error = True
        else:
            form = AddForm()

        return render(request, 'ports/add.html', {
            "forms": form,
            "has_error": has_error
        })
    except:
        render_string = render_to_string('404.html')
        return HttpResponseNotFound(render_string)

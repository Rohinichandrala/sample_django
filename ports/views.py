from django.shortcuts import render
from django.http import HttpResponse
from ports.models import Port


# Create your views here.

def ports_main(request):
    ports_list = Port.objects.all()
    return render(request, 'ports/index.html', {
        'ports_list': ports_list
    })


def ports_add(request):
    return render(request, 'ports/add.html')

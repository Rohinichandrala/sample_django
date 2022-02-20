from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.urls import reverse
from ports.models import Port
from ports.models import BatchPort
from .forms import AddForm, BatchImportPortForm, SearchForm
from django.template.loader import render_to_string
from django.views.generic.base import View
import pandas as pd
from django.template import loader


# Create your views here.
class MainPort(View):
    def get(self, request):
        ports_list = Port.objects.all()
        form = SearchForm()
        return render(request, 'ports/index.html', {
            'ports_list': ports_list,
            'form': form,
            "invalidSearch": False
        })

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            port_list = Port.objects.all()
            filtered_ports = form.cleaned_data.get('port_name')
            min_lat = form.cleaned_data.get('min_latitude')
            max_lat = form.cleaned_data.get('max_latitude')
            print("Entered port", filtered_ports)
            if filtered_ports and filtered_ports.strip():
                port_list = port_list.filter(port_name__contains=filtered_ports)
            if min_lat is not None:
                port_list = port_list.filter(latitude__gt=min_lat)
            if max_lat is not None:
                port_list = port_list.filter(latitude__lt=max_lat)
            return render(request, 'ports/index.html', {
                'ports_list': port_list,
                'form': form,
                "invalidSearch": False
            })
        else:
            return render(request, 'ports/index.html', {
                'form': form,
                "invalidSearch": True
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


def sample_csv_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )

    csv_data = (('port_name', 'temperature', 'latitude', 'longitude'),
                ('Halifax', '-10', '22.9', '89.9'),
                ('Montreal', '-15', '66.8', '123.9')
                )

    t = loader.get_template('ports/sample_port_data.txt')
    c = {'data': csv_data}
    response.write(t.render(c))
    return response


class UploadBatchPortView(View):
    def get(self, request):
        form = BatchImportPortForm()
        return render(request, 'ports/batch_import.html', {
            "form": form
        })

    def post(self, request):
        submitted_form = BatchImportPortForm(request.POST, request.FILES)
        if submitted_form.is_valid():
            uploaded_file = BatchPort(batch_import_csv=request.FILES['import_ports'])
            uploaded_file.save()
            with open(uploaded_file.batch_import_csv.path, 'r') as fp:
                reader = pd.read_csv(fp)
                for _, row in reader.iterrows():
                    port_info = Port(
                        port_name=row['port_name'],
                        temperature=row['temperature'],
                        latitude=row['latitude'],
                        longitude=row['longitude']
                    )
                    port_info.save()
                fp.close()
            return_path = reverse('ports-index', args=[])
            return HttpResponseRedirect(return_path)


class EditView(View):
    def get(self, request, port_id):
        port_info = Port.objects.get(pk=port_id)
        form = AddForm()
        form.fields["port_name"].initial = port_info.port_name
        form.fields["temperature"].initial = port_info.temperature
        form.fields["latitude"].initial = port_info.latitude
        form.fields["longitude"].initial = port_info.longitude
        return render(request, 'ports/edit.html', {
            "forms": form,
            "has_error": False
        })

    def post(self, request, port_id):
        form = AddForm(request.POST)
        if form.is_valid():
            db_port = Port.objects.get(pk=port_id)
            db_port.port_name = form.cleaned_data.get('port_name')
            db_port.temperature = form.cleaned_data.get('temperature')
            db_port.latitude = form.cleaned_data.get('latitude')
            db_port.longitude = form.cleaned_data.get('longitude')
            db_port.save()
            resolved_path = reverse('ports-index', args=[])
            return HttpResponseRedirect(resolved_path)
        else:
            has_error = True
            return render(request, 'ports/edit.html', {
                "forms": form,
                "has_error": has_error
            })


class DeleteView(View):
    def get(self, request, port_id):
        port_info = Port.objects.get(pk=port_id)
        port_info.delete()
        resolved_path = reverse('ports-index', args=[])
        return HttpResponseRedirect(resolved_path)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPort.as_view(), name='ports-index'),
    path('add', views.ports_add, name='add-ports'),
    path('upload-file', views.UploadBatchPortView.as_view(), name='upload'),
    path('download-sample-file', views.sample_csv_view, name='download-port-sample-data'),
]

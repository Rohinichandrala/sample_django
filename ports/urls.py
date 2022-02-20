from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPort.as_view(), name='ports-index'),
    path('add', views.ports_add, name='add-ports'),
    path('edit/<int:port_id>', views.EditView.as_view(), name='edit-port'),
    path('delete/<int:port_id>', views.DeleteView.as_view(), name='delete-port'),
    path('upload-file', views.UploadBatchPortView.as_view(), name='upload'),
    path('download-sample-file', views.sample_csv_view, name='download-port-sample-data'),
]

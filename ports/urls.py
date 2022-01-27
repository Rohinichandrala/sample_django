from django.urls import path
from . import views

urlpatterns = [
    path('', views.ports_main, name='ports-index'),
    path('add', views.ports_add, name='add-ports'),
]

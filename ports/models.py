from django.db import models


# Create your models here.

class Port(models.Model):
    port_name = models.CharField(max_length=50)
    temperature = models.IntegerField()
    latitude = models.DecimalField(max_digits=5, decimal_places=2)
    longitude = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f'Port {self.port_name} with temperature {self.temperature} ' \
               f'located at lat/long ({self.latitude},{self.longitude})'

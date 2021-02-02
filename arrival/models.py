from django.db import models
from office.models import Customer

class Material(models.Model):
    name = models.CharField(max_length=200)

class Arrival(models.Model):
    material = models.ForeignKey(Material, on_delete=models.DO_NOTHING)
    arrival_time = models.DateTimeField('time delivered')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


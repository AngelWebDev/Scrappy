from django.db import models
from office.models import Customer, ScrappyUser


class Material(models.Model):
    class Meta:
        db_table = "material"

    name = models.CharField(max_length=200)
    price_per_kg = models.FloatField()


class Arrival(models.Model):
    class Meta:
        db_table = "arrival"

    class StatusChoices(models.TextChoices):
        OPEN = 'Open', 'Open'
        PAID = 'Paid', 'Paid'

    material = models.ForeignKey(Material, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(ScrappyUser, on_delete=models.CASCADE)
    arrived_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.OPEN)
    gross_weight_kg = models.FloatField()
    tare_kg = models.FloatField()
    net_weight_kg = models.FloatField()

from django.db import models
from arrival.models import Arrival
from office.models import ScrappyUser, Identification


# Create your models here.
class Payout(models.Model):
    class Meta:
        db_table = "payout"

    arrival = models.OneToOneField(Arrival, on_delete=models.CASCADE)
    user = models.ForeignKey(ScrappyUser, on_delete=models.CASCADE)
    identification = models.OneToOneField(Identification, on_delete=models.CASCADE)
    paid_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.FloatField()
    vat_rate = models.FloatField()
    vat_amount = models.FloatField()

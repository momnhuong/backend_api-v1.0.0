from django.db import models
from django.conf import settings
from .contract import Contract


class Billing(models.Model):
    class Meta:
        db_table = 'billing'
    contract = models.ForeignKey(Contract, null=True, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.BooleanField(default=True)
    payment_time = models.DateTimeField()
    paid = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    on_active = models.BooleanField(default=True)

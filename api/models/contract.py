from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .customer import Customer
from .product import Product
from .order import Order
import uuid
from django.utils.timezone import now


class Contract(models.Model):
    ACTIVE = 'ACTIVE',
    DEACTIVE = 'DEACTIVE'
    STATUS_CHOICES = (
        ('ACTIVE', 'ACTIVE'),
        ('DEACTIVE', 'DEACTIVE')
    )

    class Meta:
        db_table = 'contract'
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    contract_id = models.CharField(max_length=100, null=True, blank=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    contract_name = models.CharField(max_length=100, null=True, blank=True)
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    view = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    contract_date = models.DateTimeField(auto_now_add=True)
    billed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now_add=True)
    on_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.contract_name}'

    def set_on_active(self, is_bool):
        self.on_active = is_bool
        self.save()
        return

    def set_status(self, is_bool):
        self.status = is_bool
        self.save()
        return

    def set_contract_date(self):
        self.contract_date = now()
        self.save()
        return

    def set_billed(self, is_bool):
        self.billed = is_bool
        self.save()
        return

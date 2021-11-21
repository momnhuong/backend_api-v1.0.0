from django.db import models
from django.conf import settings
from .customer import Customer
from .product_of_customer import ProductOfCustomer
from .customer import Customer


class Alert(models.Model):
    LOW = 'LOW'
    NORMAL = 'NORMAL'
    HIGH = 'HIGH'
    URGENT = 'URGENT'
    PRIORITY_CHOICES = (
        (LOW, 'LOW'),
        (NORMAL, 'NORMAL'),
        (HIGH, 'HIGH'),
        (URGENT, 'URGENT')
    )

    class Meta:
        db_table = 'alert'
    product_of_customer = models.ForeignKey(
        ProductOfCustomer, null=True, on_delete=models.CASCADE)
    system_id = models.CharField(max_length=100, blank=True, null=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    priority = models.CharField(
        max_length=50, choices=PRIORITY_CHOICES, default=LOW)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    on_active = models.BooleanField(default=True)

    def __str__(self):
        return self.message

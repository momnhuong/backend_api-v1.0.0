
from django.db import models
from .product import Product
from .package import Package
from .product_of_customer import ProductOfCustomer


class PackageOfProductCustomer(models.Model):
    ACTIVE = 'ACTIVE'
    RESTARING = 'RESTARING'
    STATUS_CHOICES = (
        (ACTIVE, 'ACTIVE'),
        (RESTARING, 'RESTARING')
    )

    class Meta:
        db_table = 'package_of_product_customer'
    product_of_customer = models.ForeignKey(
        ProductOfCustomer, related_name='package_of_product_customer', null=True, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, null=True, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default=ACTIVE)
    view = models.TextField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, default=0)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, default=0)
    on_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'

    def set_on_active(self, on_bool):
        self.on_active = on_bool
        self.save()
        return

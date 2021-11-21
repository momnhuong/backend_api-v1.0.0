from django.db import models
from .customer import Customer
from .product import Product
from .package import Package
from .contract import Contract


class ProductOfCustomer(models.Model):
    class Meta:
        db_table = 'product_of_customer'
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    system_name = models.CharField(max_length=100, null=True, blank=True)
    contract = models.ForeignKey(
        Contract, null=True, on_delete=models.CASCADE, blank=True)
    package = models.ForeignKey(
        Package, null=True, on_delete=models.CASCADE, blank=True)
    system_id = models.CharField(max_length=100, blank=True, null=True)
    address_ip = models.CharField(max_length=100, blank=True, null=True)
    expired = models.DateTimeField(blank=True, null=True)
    on_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'

    def set_on_active(self, on_bool):
        self.on_active = on_bool
        self.save()
        return

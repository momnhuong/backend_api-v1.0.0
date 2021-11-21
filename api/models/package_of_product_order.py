
from django.db import models
from .product import Product
from .package import Package
from .product_of_order import ProductOfOrder
from .order import Order


class PackageOfProductOrder(models.Model):
    class Meta:
        db_table = 'package_of_product_order'
    product_of_order = models.ForeignKey(
        ProductOfOrder, related_name='package_of_product_order', null=True, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, null=True, on_delete=models.CASCADE)
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

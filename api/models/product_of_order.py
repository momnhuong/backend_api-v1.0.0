from django.db import models
from .customer import Customer
from .product import Product
from .order import Order


class ProductOfOrder(models.Model):
    class Meta:
        db_table = 'product_of_order'
    order = models.ForeignKey(
        Order, related_name='product_of_order', null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, default=0)

    on_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.order} - {self.id}'

    def set_on_active(self, on_bool):
        self.on_active = on_bool
        self.save()
        return

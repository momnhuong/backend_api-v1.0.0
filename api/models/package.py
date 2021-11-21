
from django.db import models
from django.conf import settings
from .product import Product


class Package(models.Model):

    class Meta:
        db_table = 'package'
    product = models.ForeignKey(
        Product, related_name='package', null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, default=0)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, default=0)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    on_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

    def set_on_active(self, is_bool):
        self.on_active = is_bool
        self.save()
        return

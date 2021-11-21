from django.db import models
from .customer import Customer
# from .product_of_order import ProductOfOrder


class Order(models.Model):
    class Meta:
        db_table = 'order'
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=200, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, default=0)
    # discount = models.DecimalField(
    #     max_digits=10, decimal_places=2, blank=True, default=0)
    on_confirm = models.BooleanField(default=False)
    on_active = models.BooleanField(default=True)
    signed = models.BooleanField(default=False)
    order_time = models.IntegerField(default=1, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id}'

    def set_on_active(self, on_bool):
        self.on_active = on_bool
        self.save()
        return

    def set_on_confirm(self, on_bool):
        self.on_confirm = on_bool
        self.save()
        return

    def set_signed(self, on_bool):
        self.signed = on_bool
        self.save()
        return

    def set_status(self, on_bool):
        self.status = on_bool
        self.save()
        return

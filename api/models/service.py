from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .customer import Customer


class Service(models.Model):

    class Meta:
        db_table = 'service'

    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    system_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    on_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.system_id} & {self.customer}'

    def set_on_active(self, on_bool):
        self.on_active = on_bool
        self.save()
        return

from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .catelog import Catelog


class Product(models.Model):

    class Meta:
        db_table = 'product'
    catelog_id = models.ForeignKey(
        Catelog, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    price = models.IntegerField(blank=True, default=0)
    to = models.CharField(max_length=50, blank=True)
    src = models.ImageField(upload_to='product_image', blank=True, null=True)
    link = models.CharField(max_length=50, blank=True)
    specifications = models.TextField(blank=True)
    description_vn = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    brief_description_vn = models.TextField(blank=True)
    brief_description_en = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    on_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def set_on_active(self, on_bool):
        self.on_active = on_bool
        self.save()
        return

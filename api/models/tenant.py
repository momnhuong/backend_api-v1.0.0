from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator

class Tenant(models.Model):
    
    class Meta:
        db_table = 'tenant'

    name = models.CharField(max_length=50, null=False, unique=True)
    status = models.IntegerField(validators=[MaxLengthValidator(5)], choices=settings.TENANT_STATUS,  default=settings.TENANT_STATUS_DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from django.db import models
from django.conf import settings
from .tenant import Tenant
from .customer import Customer
from .product import Product
from django.core.validators import MinLengthValidator, MaxLengthValidator

class Ticket(models.Model):
    
    class Meta:
        db_table = 'ticket'

    title = models.CharField(max_length=15, null=False, unique=True)
    customer = models.ForeignKey(Customer, null=True, related_name='ticket_customer', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, related_name='ticket_product', on_delete=models.CASCADE)
    priority = models.IntegerField(validators=[MaxLengthValidator(5)], choices=settings.TICKET_PRIORITY, default=settings.TICKET_PRIORITY_DEFAULT)
    mobile_number = models.CharField(max_length=200, null=True)
    description = models.TextField(blank=True, null=True)
    ticket_type = models.IntegerField(validators=[MaxLengthValidator(5)], choices=settings.TICKET_TYPE, default=settings.TICKET_TYPE_DEFAULT)
    verify_code = models.CharField(max_length=15, null=True)
    tenant = models.ForeignKey(Tenant, null=True, related_name='ticket_tenant', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(validators=[MaxLengthValidator(5)], choices=settings.TICKET_STATUS, default=settings.TICKET_STATUS_DEFAULT)

    def __str__(self):
        return self.title


class TicketActionLog(models.Model):
    
    class Meta:
        db_table = 'ticket_action_log'

    ticket = models.ForeignKey(Ticket, null=True, related_name='ticket_log', on_delete=models.CASCADE)
    previous_status = models.IntegerField(validators=[MaxLengthValidator(5)], choices=settings.TICKET_STATUS, default=settings.TICKET_STATUS_DEFAULT)
    status = models.IntegerField(validators=[MaxLengthValidator(5)], choices=settings.TICKET_STATUS, default=settings.TICKET_STATUS_DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

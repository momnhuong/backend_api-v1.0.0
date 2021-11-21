from django.db import models


class Customer(models.Model):

    class Meta:
        db_table = 'customer'

    requester_id = models.CharField(max_length=50, null=False, blank=True)
    customer_name = models.CharField(max_length=200, null=True)
    tax_code = models.CharField(max_length=100, null=True, blank=True)
    main_email = models.EmailField(
        max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    fax_number = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    on_active = models.BooleanField(default=True)

    def __str__(self):
        return self.customer_name

    def set_on_active(self, is_bool):
        self.on_active = is_bool
        self.save()
        return

    def set_requester_id(self, data):
        self.requester_id = data
        self.save()
        return

from django.db import models
from django.conf import settings
from django.utils.timezone import now
from .role import Role
from .customer import Customer
import uuid


class Account(models.Model):
    ACCOUNTANT = 'ACCOUNTANT'
    TECHNICAL = 'TECHNICAL'
    ADMIN = 'ADMIN'
    SUPPER_ADMIN = 'SUPPER_ADMIN'
    ROLE_CHOICES = (
        (ACCOUNTANT, 'ACCOUNTANT'),
        (TECHNICAL, 'TECHNICAL'),
        (ADMIN, 'ADMIN'),
        (SUPPER_ADMIN, 'SUPPER_ADMIN')
    )

    class Meta:
        db_table = 'account'

    def __str__(self):
        return self.username
    username = models.CharField(max_length=51, null=False, unique=True)
    password = models.CharField(max_length=200, null=False)
    fullname = models.CharField(max_length=255, default=None, blank=True)
    role = models.ForeignKey(Role, null=True, on_delete=models.CASCADE)
    # requester_id = models.CharField(max_length=50, null=False, blank=True)
    # role = models.CharField(
    #     max_length=50, choices=ROLE_CHOICES, default=SUPPER_ADMIN)
    fcm_token = models.TextField(blank=True, null=True)
    account_code = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=100, null=True, blank=True)
    identity_card = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    mobile = models.CharField(max_length=50, blank=True)
    fax = models.CharField(max_length=50, blank=True)
    address = models.CharField(
        max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    first_login = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now_add=True)
    customer_of = models.ForeignKey(
        Customer, blank=True, null=True, on_delete=models.CASCADE)
    on_active = models.BooleanField(default=True)

    def set_new_password(self, new_password):
        self.password = new_password
        self.first_login = False
        self.save()
        return

    def set_last_login(self):
        self.last_login = now()
        self.save()

    def set_on_active(self, on_bool):
        self.on_active = on_bool
        self.save()

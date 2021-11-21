from django.db import models


class Static(models.Model):
    class Meta:
        db_table = 'static'

    email = models.EmailField(max_length=100, null=True, blank=True)
    hotline = models.CharField(max_length=20, null=True, blank=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    # contract_name = models.CharField(max_length=100, null=True, blank=True)
    registration_address = models.CharField(
        max_length=100, null=True, blank=True)
    tranding_address = models.CharField(max_length=100, null=True, blank=True)
    tax_code = models.CharField(max_length=100, null=True, blank=True)
    account_holder = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=100, null=True, blank=True)
    bank = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.CharField(max_length=200, blank=True, null=True)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    twitter = models.CharField(max_length=200, blank=True, null=True)
    linkedin = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.email

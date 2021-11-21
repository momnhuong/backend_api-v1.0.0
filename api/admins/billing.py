from django.contrib import admin


class BillingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'invoice_number',
        'payment_status',
        'paid',
        'payment_status',
    )
    list_display_links = ('id', 'invoice_number')
    empty_value_display = '--empty--'

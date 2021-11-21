from django.contrib import admin


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_name',
        'created_at',
        'phone_number',
        'main_email',
        'phone_number',
        'fax_number',
        'on_active'
    )
    list_display_links = ('id', 'customer_name')
    empty_value_display = '--empty--'

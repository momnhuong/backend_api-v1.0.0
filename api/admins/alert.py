from django.contrib import admin


class AlertAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'message',
        'customer',
        'product_of_customer',
        'read'
    )
    list_display_links = ('id', 'message')
    empty_value_display = '--empty--'

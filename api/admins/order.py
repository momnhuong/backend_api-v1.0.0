from django.contrib import admin


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'signed'
    )
    list_display_links = ('id', 'customer')
    empty_value_display = '--empty--'

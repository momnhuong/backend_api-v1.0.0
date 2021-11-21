from django.contrib import admin


class ProductOrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'price'
    )
    list_display_links = ('id', 'order')
    empty_value_display = '--empty--'

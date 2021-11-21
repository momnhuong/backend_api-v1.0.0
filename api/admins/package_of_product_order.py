from django.contrib import admin


class PackageOfProductOrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product_of_order',
        'price',
        'discount',
    )
    list_display_links = ('id', 'product_of_order')
    empty_value_display = '--empty--'

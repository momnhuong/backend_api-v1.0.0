from django.contrib import admin


class PackageOfProductCustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product_of_customer',
        'price',
        'discount',
    )
    list_display_links = ('id', 'product_of_customer')
    empty_value_display = '--empty--'

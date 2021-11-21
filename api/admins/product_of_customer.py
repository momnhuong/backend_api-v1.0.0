from django.contrib import admin


class ProductOCAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'product',
    )
    list_display_links = ('id', 'customer')
    empty_value_display = '--empty--'

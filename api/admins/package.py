from django.contrib import admin


class PackageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'discount',
    )
    list_display_links = ('id', 'name')
    empty_value_display = '--empty--'

from django.contrib import admin


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'to',
        'src',
        'description_vn',
        'description_en',
        'brief_description_vn',
        'brief_description_en'
    )
    list_display_links = ('id', 'name')
    empty_value_display = '--empty--'

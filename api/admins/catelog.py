
from django.contrib import admin


class CatelogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'on_active'
    )
    list_display_links = ('id', 'name')
    empty_value_display = '--empty--'

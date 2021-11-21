from django.contrib import admin


class RoleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    list_display_links = ('id', 'name')
    empty_value_display = '--empty--'

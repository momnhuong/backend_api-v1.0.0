from django.contrib import admin


class StaticAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'hotline',
        'email'
    )
    list_display_links = ('id', 'email')
    empty_value_display = '--empty--'

from django.contrib import admin


class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        # 'created_at',
        'system_id',
    )
    list_display_links = ('id', 'customer')
    empty_value_display = '--empty--'

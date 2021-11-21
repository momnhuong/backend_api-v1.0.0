from django.contrib import admin


class ContractAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'code',
        'customer',
        'created_at',
        'contract_date'
    )
    list_display_links = ('id', 'code')
    empty_value_display = '--empty--'

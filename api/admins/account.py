from django.contrib import admin


class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'fullname',
        'email',
        'role',
        'account_code',
        'customer_of',
        'phone',
        'fax',
        'address',
        'first_login',
        'last_login',
        'created_at',
    )
    list_display_links = ('username', 'fullname')
    empty_value_display = '--empty--'

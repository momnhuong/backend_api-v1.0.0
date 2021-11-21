from django.contrib import admin
from .models import Account, Role, Customer, Static, Product, Order, ProductOfCustomer, ProductOfOrder, Service, Contract, Catelog, Package, PackageOfProductOrder, PackageOfProductCustomer, Alert, Billing
from api.admins.order import OrderAdmin
from api.admins.account import AccountAdmin
from api.admins.role import RoleAdmin
from api.admins.customer import CustomerAdmin
from api.admins.static import StaticAdmin
from api.admins.product import ProductAdmin
from api.admins.product_of_customer import ProductOCAdmin
from api.admins.product_of_order import ProductOrderAdmin
from api.admins.service import ServiceAdmin
from api.admins.contract import ContractAdmin
from api.admins.catelog import CatelogAdmin
from api.admins.package import PackageAdmin
from api.admins.package_of_product_order import PackageOfProductOrderAdmin
from api.admins.package_of_product_customer import PackageOfProductCustomerAdmin
from api.admins.alert import AlertAdmin
from api.admins.billing import BillingAdmin
admin.site.register(Order, OrderAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Static, StaticAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductOfCustomer, ProductOCAdmin)
admin.site.register(ProductOfOrder, ProductOrderAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Catelog, CatelogAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(PackageOfProductOrder, PackageOfProductOrderAdmin)
admin.site.register(PackageOfProductCustomer, PackageOfProductCustomerAdmin)
admin.site.register(Alert, AlertAdmin)
admin.site.register(Billing, BillingAdmin)

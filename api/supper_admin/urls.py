from django.urls import path
from .customer import ListCustomerView, DetailCustomerView, CreateCustomerView
from .customer_account import ListCustomerAccountView, DetailCustomerAccountView, DetailUpdateCustomerAccountView, DetailAccountView
from .role import ListRoleView
from .product import DetailUpdateProductView, CreateProductView
from .order_of_customer import ListOrderOfCustomerView, DetailOrderOfCustomerView
from .product_of_customer import ListProductOfCustomerView, DetailProductOfCustomerView, CreateProductOfCustomer, UpdateStatusProductOfCustomerView, DetailProductOfCustomerItemView
from .contract import ListContractView, DetailContractView, DetailContractInputCustomerView
from .catelog import ListCatelogView, DetailCatelogView
from .product_of_catelog import ProductOfCatelogView
from .package import ListPackageView, EditPackageView, UpdateStatusPackageView
from .homepage import HomePageListPackageOfCustomerSAView, HomePageCountPackageSAView, HomePageListTicketSAView, HomePageListCustomerOfProductSAView, HomePageListBalanceOfCustomerSAView
from .alert import ListAlertView, CreateAlertView
from .billing import ListBillingView, DetailBillingView
urlpatterns = [
    # Customers API
    path('customers/', ListCustomerView.as_view()),
    path('customers/<int:customer_id>/', DetailCustomerView.as_view()),

    # Customer Account API
    path('customers/accounts/', ListCustomerAccountView.as_view()),
    path('customer/create/', CreateCustomerView.as_view()),
    path('customers/accounts/<int:customer_id>/',
         DetailCustomerAccountView.as_view()),
    path('customers/account/<int:account_id>',
         DetailUpdateCustomerAccountView.as_view()),
    path('customers/accounts/account_id/<int:account_id>',
         DetailAccountView.as_view()),
    # Role API
    path('roles/', ListRoleView.as_view()),

    # Product API
    #     path('products/', ListProductView.as_view()),
    path('products/<int:product_id>/', DetailUpdateProductView.as_view()),
    path('product/create/', CreateProductView.as_view()),
    # Order Of Customer
    path('order-of-customer/', ListOrderOfCustomerView.as_view()),
    path('order-of-customer/<int:order_id>/',
         DetailOrderOfCustomerView.as_view()),

    # Product Of Customer
    path('product-of-customer/', ListProductOfCustomerView.as_view()),
    path('product-of-customer/<int:customer_id>/',
         DetailProductOfCustomerView.as_view()),
    path('product-of-customer/create/', CreateProductOfCustomer.as_view()),
    path('product-of-customer/change-status/<int:product_of_customer_id>/',
         UpdateStatusProductOfCustomerView.as_view()),
    path('product-of-customer/detail/<product_of_customer_id>/',
         DetailProductOfCustomerItemView.as_view()),

    #     # Contract
    path('contract/', ListContractView.as_view()),
    path('contract/<int:contract_id>/', DetailContractView.as_view()),
    path('contract/customer/<int:customer_id>/',
         DetailContractInputCustomerView.as_view()),
    #     Catelog
    path('catelog/', ListCatelogView.as_view()),
    path('catelog/<int:catelog_id>/', DetailCatelogView.as_view()),

    #     Product Of Catelog
    path('product-of-catelog/<int:catelog_id>/',
         ProductOfCatelogView.as_view()),

    #     Package
    path('package/', ListPackageView.as_view()),
    path('package/<int:package_id>/', EditPackageView.as_view()),
    path('package/update-status/<int:package_id>/',
         UpdateStatusPackageView.as_view()),

    # Homepage
    path('homepage/package_of_customer/',
         HomePageListPackageOfCustomerSAView.as_view()),
    path('homepage/count_package_of_customer/',
         HomePageCountPackageSAView.as_view()),
    path('homepage/count_ticket/', HomePageListTicketSAView.as_view()),
    path('homepage/list-customer-of-product/<int:product_id>/',
         HomePageListCustomerOfProductSAView.as_view()),
    path('homepage/list-balance/', HomePageListBalanceOfCustomerSAView.as_view()),

    # Alert
    path('alert/', ListAlertView.as_view()),
    path('alert/create/', CreateAlertView.as_view()),

    # Billing
    path('billing/', ListBillingView.as_view()),
    path('billing/<int:billing_id>/', DetailBillingView.as_view()),
]

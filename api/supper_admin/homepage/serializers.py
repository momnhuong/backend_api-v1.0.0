
from rest_framework import serializers
from api.models import ProductOfCustomer, Customer, Product, Service, PackageOfProductCustomer
from api.supper_admin.product_of_customer.serializers import HomePageListProductOCSerializer
from api.serializers.product import ProductSerializer
from api.supper_admin.package.serializers import PackageSerializer

# class HomePageListPackageOfSerializer(serializers.ModelSerializer):
#     product_of_customer = HomePageListProductOCSerializer()
#     package = PackageSerializer()

#     class Meta:
#         model = PackageOfProductCustomer
#         fields = ('id', 'status', 'view', 'price', 'discount',
#                   'created_at', 'product_of_customer', 'package')


class HomepageCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class HomePageListPackageOfSerializer(serializers.ModelSerializer):
    package = PackageSerializer()
    product = ProductSerializer()
    customer = HomepageCustomerSerializer()

    class Meta:
        model = ProductOfCustomer
        fields = '__all__'


class HomePageListPackageOfNoCustomerSerializer(serializers.ModelSerializer):
    package = PackageSerializer()
    product = ProductSerializer()

    class Meta:
        model = ProductOfCustomer
        fields = ('id', 'package', 'product', 'system_id', 'address_ip')

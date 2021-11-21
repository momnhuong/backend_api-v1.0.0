

from rest_framework import serializers
from api.models import Contract, Customer, Product, Service, Order, Package, PackageOfProductOrder, ProductOfOrder
from api.serializers.product import ProductSerializer


class NamePackageSerializer(serializers.ModelSerializer):

    class Meta():
        model = Package
        fields = ('id', 'name', 'description')


class FullProductOfOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta():
        model = ProductOfOrder
        fields = '__all__'


class FullPackageOfOrderSerializer(serializers.ModelSerializer):
    product_of_order = FullProductOfOrderSerializer()
    package = NamePackageSerializer()

    class Meta():
        model = PackageOfProductOrder
        fields = ('id', 'product_of_order', 'package',
                  'price', 'discount', 'view')


class PackageOfOrderSerializer(serializers.ModelSerializer):

    class Meta():
        model = PackageOfProductOrder
        fields = '__all__'


class CustomPackageOrderSerializer(serializers.ModelSerializer):
    class Meta():
        model = PackageOfProductOrder
        fields = ('package', 'on_active')

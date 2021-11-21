from rest_framework import serializers
from api.models import ProductOfCustomer, PackageOfProductCustomer
from .product import ProductSerializer
from api.supper_admin.package.serializers import PackageSerializer
from api.supper_admin.catelog.serializers import CatelogSerializer
from api.supper_admin.product_of_customer.serializers import ProductOCSerializer, FullProductOfCustomerSerializer


class HomePageGetAllProductOCSerializer(serializers.ModelSerializer):
    package = PackageSerializer()
    product = ProductSerializer()

    class Meta:
        model = ProductOfCustomer
        fields = '__all__'


class HomePageGetProductOCSerializer(serializers.ModelSerializer):
    catelog = CatelogSerializer()
    product_of_customer = FullProductOfCustomerSerializer(many=True)

    class Meta:
        model = ProductOfCustomer  # every table doesn't important
        fields = ('catelog', 'product_of_customer')

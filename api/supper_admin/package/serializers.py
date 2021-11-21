
from rest_framework import serializers
from api.models import Contract, Customer, Product, Service, Order, Package
from api.supper_admin.order_of_customer.serializers import OrderSerializer, ListOrderSerializer, ListOrderNoCustomerSerializer
from api.serializers.product import ProductSerializer
from api.supper_admin.customer.serializers import CustomerSerializer
from django.utils.timezone import now
from api.serializers.static_info import StaticSerializer
from api.models import Static, Order, Customer
from api.supper_admin.order_of_customer.serializers import DetailOrderSerializers


class NamePackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Package
        fields = ('id', 'name')


class PackageSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Package
        fields = '__all__'


class CreatePackageSerializer(serializers.ModelSerializer):

    product_id = serializers.CharField()
    name = serializers.CharField()
    price = serializers.CharField()
    discount = serializers.CharField(allow_blank=True, required=False)
    description = serializers.CharField()

    class Meta:
        model = Package
        fields = ('product_id', 'name', 'price', 'discount', 'description')

    # def validate_product_id(self, product_id):
    #     try:
    #         product = Product.objects.get(id=product_id, on_active=True)
    #     except:
    #         raise serializers.ValidationError('product is invalid')
    #     return product_id

    def create(self, validated_data):
        return super().create(validated_data)


class EditPackageSerializer(serializers.ModelSerializer):

    product_id = serializers.CharField()
    name = serializers.CharField()
    price = serializers.CharField()
    discount = serializers.CharField(allow_blank=True, required=False)
    description = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Package
        fields = ('product_id', 'name', 'price', 'discount', 'description')

    def product_id(self, product_id):
        try:
            product = Product.objects.get(id=product_id, on_active=True)
        except:
            raise serializers.ValidationError('product is invalid')
        return product_id


class UpdateStatusSerializer(serializers.ModelSerializer):
    on_active = serializers.BooleanField()

    class Meta:
        model = Package
        fields = ('id', 'on_active')

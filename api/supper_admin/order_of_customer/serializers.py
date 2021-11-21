from rest_framework import serializers
from api.models import Order, Customer, Product, ProductOfOrder, Package, PackageOfProductOrder
from api.supper_admin.customer.serializers import CustomerSerializer
from api.serializers.product import ProductSerializer
from api.supper_admin.package_of_order.serializers import PackageOfOrderSerializer, CustomPackageOrderSerializer, FullPackageOfOrderSerializer
import json
import operator


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class FullOrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class ProductOfOrderSerializer(serializers.ModelSerializer):
    package_of_product_order = CustomPackageOrderSerializer(many=True)

    class Meta:
        model = ProductOfOrder
        fields = ('product', 'on_active', 'package_of_product_order')


class DetailOrderSerializers(serializers.ModelSerializer):

    class Meta:
        model = ProductOfOrder
        fields = ('product_id', 'price')


class OrderOfCustomerSerializers(serializers.ModelSerializer):
    # product = ProductSerializer(many=True)
    customer = CustomerSerializer()
    service = FullPackageOfOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'order_id', 'signed',
                  'created_at', 'customer', 'amount', 'order_time', 'service', 'on_active', 'on_active')


class ListOrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class ListOrderNoCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'signed', 'order_time',
                  'amount', 'order_id', 'created_at', 'on_active')


class CreateOrderSerializer(serializers.ModelSerializer):
    product_of_order = ProductOfOrderSerializer(many=True)
    customer_id = serializers.CharField()
    order_id = serializers.CharField(required=False)
    order_time = serializers.CharField(required=False)
    amount = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = ('id', 'order_id', 'customer_id',
                  'product_of_order', 'order_time', 'amount')

    def create(self, validated_data):
        list_product = validated_data.pop('product_of_order')
        order = Order.objects.create(**validated_data)
        for product in list_product:
            list_package = product.pop('package_of_product_order')
            product_of_order = ProductOfOrder.objects.create(
                order=order, **product)
            for package in list_package:
                package_of_product_order = PackageOfProductOrder.objects.create(
                    product_of_order=product_of_order, **package)
                just_package = PackageOfProductOrder.objects.get(
                    id=package_of_product_order.id)
                old_package = Package.objects.get(
                    id=package_of_product_order.package_id)
                just_package.price = old_package.price
                just_package.discount = old_package.discount
                just_package.view = {
                    'name': old_package.name,
                    'package': old_package.id,
                    'price': float(old_package.price),
                    'discount': float(old_package.discount)
                }
                just_package.save()
        return order

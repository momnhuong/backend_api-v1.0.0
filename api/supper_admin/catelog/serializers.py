from rest_framework import serializers
from api.models import Contract, Customer, Product, Service, Order, Catelog
from api.supper_admin.order_of_customer.serializers import OrderSerializer, ListOrderSerializer, ListOrderNoCustomerSerializer
from api.serializers.product import ProductSerializer
from api.supper_admin.customer.serializers import CustomerSerializer
from django.utils.timezone import now
from api.serializers.static_info import StaticSerializer
from api.models import Static, Order, Customer
from api.supper_admin.order_of_customer.serializers import DetailOrderSerializers


class CatelogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catelog
        fields = '__all__'


class CreateCatelogSerializer(serializers.ModelSerializer):

    name = serializers.CharField()

    class Meta:
        model = Catelog
        fields = ('id', 'name')

    def create(self, validated_data):
        return super().create(validated_data)


class EditCatelogSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100, allow_blank=True, required=False)
    on_active = serializers.BooleanField(required=False)

    class Meta:
        model = Catelog
        fields = ('id', 'name', 'on_active')

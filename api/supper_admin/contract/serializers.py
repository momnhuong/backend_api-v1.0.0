from rest_framework import serializers
from api.models import Contract, Customer, Product, Service, Order
from api.supper_admin.order_of_customer.serializers import OrderSerializer, ListOrderSerializer, ListOrderNoCustomerSerializer, FullOrderSerializer
from api.serializers.product import ProductSerializer
from api.supper_admin.package_of_order.serializers import FullPackageOfOrderSerializer
from api.supper_admin.customer.serializers import CustomerSerializer
from api.supper_admin.customer.serializers import CustomerSerializer
from django.utils.timezone import now
from api.serializers.static_info import StaticSerializer
from api.models import Static, Order, Customer
from api.supper_admin.order_of_customer.serializers import DetailOrderSerializers
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = '__all__'


class ListContractSerializer(serializers.ModelSerializer):
    order = ListOrderNoCustomerSerializer()
    customer = CustomerSerializer()

    class Meta:
        model = Contract
        fields = ('id', 'order', 'code', 'billed', 'customer',
                  'contract_date', 'contract_id', 'end_time', 'created_at')


class CreateContractSerializer(serializers.ModelSerializer):

    order_id = serializers.CharField(max_length=10)
    contract_id = serializers.CharField(max_length=100, required=False)
    contract_name = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = Contract
        fields = ('id', 'order_id', 'contract_id', 'contract_name')

    def validate_order_id(self, order_id):
        order = Order.objects.filter(id=order_id)
        if not order:
            raise serializers.ValidationError('Order is invalid')
        order_in_contract = Contract.objects.filter(order_id=order_id)
        if order_in_contract:
            raise serializers.ValidationError('Order already exist')
        return order_id

    def create(self, validated_data):
        static = Static.objects.all().first()
        order = Order.objects.get(id=self.data['order_id'])
        customer = Customer.objects.get(id=order.customer_id)
        view = {
            'email': static.email,
            'hotline': static.hotline,
            'company_name': static.company_name,
            # 'contract_name': static.contract_name,
            'registration_address': static.registration_address,
            'tranding_address': static.tranding_address
        }
        validated_data['view'] = view
        validated_data['customer_id'] = customer.id
        validated_data['end_time'] = now(
        ) + relativedelta(months=order.order_time)
        return super().create(validated_data)


class DetailContractSerializer(serializers.ModelSerializer):
    order = FullOrderSerializer()
    service = FullPackageOfOrderSerializer(many=True)

    class Meta:
        model = Contract
        fields = ('id', 'order', 'code', 'service', 'customer', 'view',
                  'contract_date', 'contract_id', 'end_time', 'billed', 'contract_name', 'created_at')


class DetailContractNoServiceSerializer(serializers.ModelSerializer):
    order = FullOrderSerializer()

    class Meta:
        model = Contract
        fields = ('id', 'order', 'code',  'customer', 'view',
                  'contract_date', 'contract_id', 'end_time', 'billed', 'contract_name', 'created_at')

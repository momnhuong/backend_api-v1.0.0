from rest_framework import serializers
from api.models import Contract, Customer, Product, Service, Order, Catelog, Billing
from api.supper_admin.order_of_customer.serializers import OrderSerializer, ListOrderSerializer, ListOrderNoCustomerSerializer
from api.serializers.product import ProductSerializer
from api.supper_admin.customer.serializers import CustomerSerializer
from django.utils.timezone import now
from api.serializers.static_info import StaticSerializer
from api.models import Static, Order, Customer
from api.supper_admin.order_of_customer.serializers import DetailOrderSerializers
from api.supper_admin.contract.serializers import DetailContractSerializer, DetailContractNoServiceSerializer


class BillingSerializer(serializers.ModelSerializer):
    contract = DetailContractNoServiceSerializer()

    class Meta:
        model = Billing
        fields = '__all__'


class CreateBillingSerializer(serializers.ModelSerializer):

    invoice_number = serializers.CharField()
    payment_status = serializers.BooleanField()
    payment_time = serializers.CharField()
    contract_id = serializers.CharField()

    class Meta:
        model = Billing
        fields = ('invoice_number', 'payment_status',
                  'payment_time', 'contract_id')

    def validate_contract_id(self, contract_id):
        contract = Contract.objects.all().filter(id=contract_id)
        if not contract:
            raise serializers.ValidationError('Contract is incorrect')
        billing = Billing.objects.all().filter(contract_id=contract_id)
        if not billing:
            return contract_id
        else:
            raise serializers.ValidationError('Contract is incorrect')

    def create(self, validated_data):
        return super().create(validated_data)


class EditBillingSerializer(serializers.ModelSerializer):
    invoice_number = serializers.CharField(
        max_length=100, allow_blank=True, required=False)
    payment_status = serializers.BooleanField(required=False)
    payment_time = serializers.CharField(required=False)

    class Meta:
        model = Catelog
        fields = ('invoice_number', 'payment_status', 'payment_time')

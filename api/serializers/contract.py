from rest_framework import serializers
from api.models import Contract
from api.supper_admin.order_of_customer.serializers import ListOrderNoCustomerSerializer, DetailOrderSerializers, ListOrderSerializer
from .product import ProductSerializer


class ContractCustomerSerializer(serializers.ModelSerializer):
    # order = ListOrderNoCustomerSerializer()
    order = ListOrderSerializer()

    class Meta:
        model = Contract
        fields = ('id', 'order', 'contract_id', 'code', 'view',
                  'contract_date', 'end_time', 'billed', 'created_at')


class DetailContractCustomerSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)
    price = DetailOrderSerializers(many=True)

    class Meta:
        model = Contract
        fields = ('id', 'contract_id', 'end_time',
                  'product', 'price', 'billed')

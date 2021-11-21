from rest_framework import serializers
from api.models import ProductOfCustomer
from .product import ProductSerializer


class GetProductOCSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductOfCustomer
        fields = ('id', 'product', 'system_name',
                  'system_id', 'expired', 'created_at')

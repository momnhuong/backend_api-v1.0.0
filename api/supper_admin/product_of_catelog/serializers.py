from rest_framework import serializers
from api.models import ProductOfCustomer, Customer, Product, Service
from api.supper_admin.customer.serializers import GetLessInfoCustomerSerializers
from api.serializers.product import ProductSerializer


class ProductOfCatelogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

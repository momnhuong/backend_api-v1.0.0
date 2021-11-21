from rest_framework import serializers
from api.models import Contract, Customer, Product, Service, Order, Package, Alert, ProductOfCustomer
from api.models import Static, Order, Customer
from api.supper_admin.order_of_customer.serializers import DetailOrderSerializers
from api.supper_admin.customer.serializers import CustomerSerializer
from api.supper_admin.product_of_customer.serializers import ProductOCSerializer


class ListAlertSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    product_of_customer = ProductOCSerializer()

    class Meta:
        model = Alert
        fields = '__all__'


class EditAlertSerializer(serializers.ModelSerializer):
    read = serializers.BooleanField()

    class Meta:
        model = Alert
        fields = ('id', 'read')


class CreateAlertSerializer(serializers.ModelSerializer):

    system_id = serializers.CharField()
    message = serializers.CharField()
    priority = serializers.CharField()

    class Meta:
        model = Alert
        fields = ('system_id', 'message', 'priority')

    def validate_priority(self, priority):
        for i in Alert.PRIORITY_CHOICES:
            if priority == i[0]:
                return priority
        raise serializers.ValidationError('Priority is incorrect')

    def validate_system_id(self, system_id):
        product_of_customer = ProductOfCustomer.objects.all().filter(
            system_id=system_id)
        if not product_of_customer:
            raise serializers.ValidationError('system_id is incorrect')
        return system_id

    def create(self, validated_data):
        product_of_customer = ProductOfCustomer.objects.get(
            system_id=self.data['system_id'])
        validated_data['product_of_customer_id'] = product_of_customer.id
        validated_data['customer_id'] = product_of_customer.customer_id
        return super().create(validated_data)

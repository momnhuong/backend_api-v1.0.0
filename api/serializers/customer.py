from rest_framework import serializers
from api.models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        # fields = ('id', 'title', 'fullname', 'mainEmail', 'phoneNumber')
        fields = '__all__'


class DetailCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'

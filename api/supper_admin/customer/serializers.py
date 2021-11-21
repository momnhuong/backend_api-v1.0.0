from rest_framework import serializers
from api.models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class CreateCustomerSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(max_length=200)
    main_email = serializers.EmailField(
        max_length=100, allow_blank=True, required=False)
    phone_number = serializers.CharField(
        max_length=200, allow_blank=True, required=False)
    fax_number = serializers.CharField(
        max_length=200, allow_blank=True, required=False)
    address = serializers.CharField(
        max_length=200, allow_blank=True, required=False)
    tax_code = serializers.CharField(
        max_length=100, allow_blank=True, required=False)

    class Meta:
        model = Customer
        fields = ('customer_name', 'main_email',
                  'phone_number', 'address', 'fax_number', 'tax_code')

    def validate_main_email(self, main_email):
        r = Customer.objects.all().filter(main_email=main_email)
        if not r:
            return main_email
        raise serializers.ValidationError('Email already exists')

    def create(self, validated_data):
        return super().create(validated_data)


class GetLessInfoCustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'customer_name', 'main_email', 'tax_code')


class ListCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class EditCustomerSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        max_length=200, allow_blank=True, required=False)
    main_email = serializers.EmailField(
        max_length=100, allow_blank=True, required=False)
    phone_number = serializers.CharField(
        max_length=200, allow_blank=True, required=False)
    fax_number = serializers.CharField(
        max_length=200, allow_blank=True, required=False)
    address = serializers.CharField(
        max_length=200, allow_blank=True, required=False)
    tax_code = serializers.CharField(
        max_length=100, allow_blank=True, required=False)
    on_active = serializers.BooleanField(required=False)

    class Meta:
        model = Customer
        fields = ('customer_name', 'main_email',
                  'phone_number', 'fax_number', 'address', 'tax_code', 'on_active')


class DeleteCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = None

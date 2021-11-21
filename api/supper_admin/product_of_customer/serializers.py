from rest_framework import serializers
from api.models import ProductOfCustomer, Customer, Product, Service
from api.supper_admin.customer.serializers import GetLessInfoCustomerSerializers
from api.serializers.product import ProductSerializer
from api.supper_admin.package.serializers import PackageSerializer
from api.supper_admin.contract.serializers import ContractSerializer


class FullProductOfCustomerSerializer(serializers.ModelSerializer):
    customer = GetLessInfoCustomerSerializers()
    product = ProductSerializer()
    package = PackageSerializer()
    contract = ContractSerializer()

    class Meta:
        model = ProductOfCustomer
        fields = '__all__'


class ProductOCSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOfCustomer
        fields = '__all__'


class ProductOfCustomerCreatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOfCustomer
        fields = ('product_id', 'created_at')


class CreateProductOfCustomerSerializer(serializers.ModelSerializer):
    customer_id = serializers.CharField()
    product_id = serializers.CharField()
    package_id = serializers.CharField(required=False)
    address_ip = serializers.CharField(allow_blank=True, required=False)
    system_name = serializers.CharField(allow_blank=True, required=False)
    expired = serializers.CharField(allow_blank=True, required=False)
    contract_id = serializers.CharField()

    class Meta:
        model = ProductOfCustomer
        fields = ('product_id', 'package_id',
                  'customer_id', 'address_ip', 'expired', 'system_name', 'system_id', 'on_active', 'contract_id', 'contract_id')

    def validate(self, attrs):
        try:
            service = Service.objects.get(
                customer_id=attrs['customer_id'], on_active=True)
        except:
            raise serializers.ValidationError('Customer is invalid')
        return attrs

    def create(self, validated_data):
        return super().create(validated_data)


class DetailProductOCSerializers(serializers.ModelSerializer):
    product = ProductSerializer(many=True)
    customer = GetLessInfoCustomerSerializers()
    created_product = ProductOfCustomerCreatedSerializer(many=True)

    class Meta:
        model = ProductOfCustomer
        fields = ('id', 'customer', 'system_id',
                  'product', 'system_name', 'expired', 'created_product')


class ListProductOCSerializer(serializers.ModelSerializer):
    customer = GetLessInfoCustomerSerializers()
    # package = PackageSerializer()

    class Meta:
        model = Service
        fields = ('id', 'customer', 'created_at')


class EditProductOCSerializer(serializers.ModelSerializer):

    system_name = serializers.CharField(allow_blank=True, required=False)
    system_id = serializers.CharField(allow_blank=True, required=False)
    expired = serializers.CharField(allow_blank=True, required=False)
    address_ip = serializers.CharField(allow_blank=True, required=False)
    on_active = serializers.BooleanField(required=False)
    contract_id = serializers.CharField(required=False)

    class Meta:
        model = ProductOfCustomer
        fields = ('expired', 'system_name', 'system_id',
                  'address_ip', 'contract_id',  'on_active')

    # def validate_customer(self, customer):
    #     r = Customer.objects.all().filter(id=customer)
    #     if not r:
    #         raise serializers.ValidationError('customer is invalid')
    #     return customer

    # def validate_product(self, product):
    #     r = Product.objects.all().filter(id=product)
    #     if not r:
    #         raise serializers.ValidationError('product is invalid')
    #     return product

    def update(self, instance, validated_data):
        # instance.customer_id = validated_data['customer']
        # instance.product_id = validated_data['product']
        # del validated_data['customer']
        # del validated_data['product']
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance


class CreateServiceSerializer(serializers.ModelSerializer):

    customer_id = serializers.CharField(max_length=10)
    system_id = serializers.IntegerField()

    class Meta:
        model = Service
        fields = ('id', 'customer_id', 'system_id')

    def validate_customer_id(self, customer_id):
        customer = Customer.objects.filter(id=customer_id, on_active=True)
        if not customer:
            raise serializers.ValidationError('Customer is invalid')
        # customer_in_p = Service.objects.filter(customer_id=customer_id)
        customer_in_p = Service.objects.filter(
            customer_id=customer_id, on_active=True)
        print('customer_in_p: ', customer_in_p)
        if customer_in_p:
            raise serializers.ValidationError('Customers already exist')
        return customer_id

# from home page


class HomePageListProductOCSerializer(serializers.ModelSerializer):
    customer = GetLessInfoCustomerSerializers()
    product = ProductSerializer()

    class Meta:
        model = ProductOfCustomer
        fields = ('id', 'customer', 'system_name',
                  'product', 'expired', 'system_id', 'created_at')

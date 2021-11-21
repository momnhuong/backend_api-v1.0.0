from rest_framework import serializers
from api.models import Account, Role
from api.supper_admin.role.serializers import RoleSerializer
from api.supper_admin.customer.serializers import CustomerSerializer


class CustomerAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'


class ListCustomerAccountSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    customer_of = CustomerSerializer()

    class Meta:
        model = Account
        fields = '__all__'


class EditCustomerAccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=51, allow_blank=True, required=False)
    password = serializers.CharField(
        max_length=200, allow_blank=True, required=False)
    fullname = serializers.CharField(
        max_length=255, allow_blank=True, required=False)
    role = serializers.CharField(
        max_length=10, allow_blank=True, required=False)
    email = serializers.EmailField(
        max_length=100, allow_blank=True, required=False)
    identity_card = serializers.CharField(
        max_length=50, allow_blank=True, required=False)
    phone = serializers.CharField(
        max_length=50, allow_blank=True, required=False)
    mobile = serializers.CharField(
        max_length=50, allow_blank=True, required=False)
    fax = serializers.CharField(
        max_length=50, allow_blank=True, required=False)
    address = serializers.CharField(
        max_length=100, allow_blank=True, required=False)
    # customer_of = serializers.CharField(max_length=)
    on_active = serializers.BooleanField(required=False)

    class Meta:
        model = Account
        fields = ('username', 'fullname', 'password', 'role', 'email',
                  'identity_card', 'phone', 'mobile', 'fax', 'address', 'on_active')

    def validate_role(self, role):
        r = Role.objects.all().filter(id=role)
        if not r:
            raise serializers.ValidationError('role is invalid')
        return role

    def update(self, instance, validated_data):
        instance.role_id = validated_data['role']
        del validated_data['role']
        for k, v in validated_data.items():
            setattr(instance, k, v)

        instance.save()
        return instance

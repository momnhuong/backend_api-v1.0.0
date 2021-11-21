from rest_framework import serializers
from api.models import Account
from api.models import Role, Customer


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class CreateAccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    fullname = serializers.CharField(allow_blank=True, required=False)
    role_id = serializers.CharField()
    customer_of_id = serializers.CharField()

    class Meta:
        model = Account
        fields = ('username', 'password', 'email',
                  'fullname', 'role_id', 'customer_of_id')

    def validate_username(self, username):
        try:
            account = Account.objects.get(username=username)
        except:
            return username
        raise serializers.ValidationError('Username already exists')

    def validate_role_id(self, role_id):
        try:
            role = Role.objects.get(id=role_id)
        except:
            raise serializers.ValidationError('Role is invalid')
        if role.name == Account.SUPPER_ADMIN:
            raise serializers.ValidationError('Role is invalid!')
        return role_id

    def validate_customer_id(self, customer_of_id):
        try:
            customer = Customer.objects.get(id=customer_of_id)
        except:
            raise serializers.ValidationError('Customer is invalid')
        return customer_of_id

    def create(self, validated_data):
        role = Role.objects.get(id=self.data['role_id'])
        customer = Customer.objects.get(id=self.data['customer_of_id'])
        print('customer: ', customer.id)
        validated_data['role_id'] = str(role.id)
        validated_data['customer_of_id'] = customer.id
        return super().create(validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = Account(
            email=self.validated_data['email'], username=self.validated_data['username'],)
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if(password != password2):
            raise serializers.ValidationError(
                {'password': 'Password must match!'})
        account.set_password(password)
        account.save()
        return account


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=50, min_length=8, write_only=True)
    password = serializers.CharField(max_length=200, min_length=8)

    class Meta:
        model = Account
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class LogoutSerializer(serializers.ModelSerializer):
    zendesk_id = serializers.CharField()

    class Meta:
        model = Account
        fields = ('id', 'zendesk_id')


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        max_length=50, min_length=8, required=True)
    new_password = serializers.CharField(
        max_length=50, min_length=8, required=True)

    class Meta:
        model = Account
        fields = ['old_password', 'new_password']


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    # def validate(self, attrs):
    #     try:
    #         password = attrs.get('password')
    #         token = attrs.get('token')
    #         uidb64 = attrs.get('uidb64')

    #         id = force_str(urlsafe_base64_decode(uidb64))
    #         user = Account.objects.get(id=id)
    #         if not PasswordResetTokenGenerator().check_token(user, token):
    #             raise AuthenticationFailed('The reset link is invalid', 401)

    #         user.set_new_password(password)
    #         user.save()

    #         return (user)
    #     except Exception as e:
    #         raise AuthenticationFailed('The reset link is invalid', 401)
    #     return super().validate(attrs)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        # fields = '__all__'
        fields = ('username', 'fullname', 'email', 'account_code',
                  'identity_card', 'phone', 'mobile', 'fax', 'address')


class UserProfileEditSerializer(serializers.ModelSerializer):

    fullname = serializers.CharField(
        max_length=255, allow_blank=True, required=False)
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

    class Meta:
        model = Account
        fields = ('fullname', 'email', 'identity_card',
                  'phone', 'mobile', 'fax', 'address')

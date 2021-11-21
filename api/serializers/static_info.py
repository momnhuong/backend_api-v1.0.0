from rest_framework import serializers
from api.models import Static


class StaticSerializer(serializers.ModelSerializer):

    class Meta:
        model = Static
        fields = '__all__'


class EditStaticSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(allow_blank=True, required=False)
    hotline = serializers.CharField(allow_blank=True, required=False)
    company_name = serializers.CharField(allow_blank=True, required=False)
    # contract_name = serializers.CharField(allow_blank=True, required=False
    #                                       )
    registration_address = serializers.CharField(allow_blank=True, required=False
                                                 )
    tranding_address = serializers.CharField(allow_blank=True, required=False
                                             )
    tax_code = serializers.CharField(allow_blank=True, required=False)
    account_number = serializers.CharField(allow_blank=True, required=False)
    account_holder = serializers.CharField(allow_blank=True, required=False)
    bank = serializers.CharField(allow_blank=True, required=False)
    facebook = serializers.CharField(allow_blank=True, required=False)
    instagram = serializers.CharField(allow_blank=True, required=False)
    twitter = serializers.CharField(allow_blank=True, required=False)
    linkedin = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Static
        fields = '__all__'

from rest_framework import serializers
from api.models import Account


class UpdateFcmTokenSerializer(serializers.ModelSerializer):
    fcm_token = serializers.CharField()

    class Meta:
        model = Account
        fields = ('id', 'fcm_token')

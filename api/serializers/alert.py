from rest_framework import serializers
from api.models import Alert

class AlertSerializer(serializers.ModelSerializer):

  class Meta:
    model = Alert
    # fields = ('id', 'title', 'fullname', 'mainEmail', 'phoneNumber')
    fields = '__all__'       

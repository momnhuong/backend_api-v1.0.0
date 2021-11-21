from rest_framework import serializers
from api.models import Product, Catelog


class CatelogInProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catelog
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ListProductSerializer(serializers.ModelSerializer):
    catelog_id = CatelogInProductSerializer()

    class Meta:
        model = Product
        fields = '__all__'


# homepage
class HomePageProductSerializer(serializers.ModelSerializer):
    # catelog = CatelogSerializer()
    # package =

    class Meta:
        model = Product
        fields = ('id', 'name')

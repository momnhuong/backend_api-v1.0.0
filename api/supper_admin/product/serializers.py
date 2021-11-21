from rest_framework import serializers
from api.models import Product, Catelog

# class ADProductSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Product
#         fields = '__all__'


class CreateProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    to = serializers.CharField(allow_blank=True, required=False)
    src = serializers.FileField()
    link = serializers.CharField(allow_blank=True, required=False)
    description_vn = serializers.CharField(allow_blank=True, required=False)
    description_en = serializers.CharField(allow_blank=True, required=False)
    brief_description_vn = serializers.CharField(
        allow_blank=True, required=False)
    brief_description_en = serializers.CharField(
        allow_blank=True, required=False)
    catelog_id = serializers.CharField()
    specifications = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Product
        fields = ('name', 'to', 'src', 'link', 'description_vn', 'description_en',
                  'brief_description_vn', 'brief_description_en', 'specifications', 'catelog_id')

    def validate_catelog_id(self, catelog_id):
        try:
            catelog = Catelog.objects.get(id=catelog_id, on_active=True)
        except:
            raise serializers.ValidationError('Catelog is not exists')
        return catelog_id

    def create(self, validated_data):
        print('catelog ne: ', self.data['catelog_id'])
        validated_data['catelog_id'] = Catelog.objects.get(
            id=self.data['catelog_id'])
        return super().create(validated_data)


class ListProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class EditProductSerializer(serializers.ModelSerializer):
    specifications = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)

        instance.save()
        return instance

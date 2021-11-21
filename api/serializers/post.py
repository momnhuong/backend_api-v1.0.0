from rest_framework import serializers
from api.models import Post
from .account import AccountSerializer

class PostSerializer(serializers.ModelSerializer):
  user = AccountSerializer()

  class Meta:
    model = Post
    fields = ('id', 'title', 'image', 'workingtime', 'material', 'guide', 'category', 'level', 'user', 'created_at')

class PostCreateSerializer(serializers.ModelSerializer):

  class Meta:
    model = Post
    fields = '__all__'

class PostUpdateSerializer(serializers.ModelSerializer):

  class Meta:
    model = Post
    fields = ('id', 'title', 'image', 'workingtime', 'material', 'guide', 'category', 'level')
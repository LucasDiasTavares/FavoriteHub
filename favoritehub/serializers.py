import pdb

from rest_framework import serializers
from .models import Client, Product, Favorite


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'email']

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'image', 'price', 'average_rating']

    def get_average_rating(self, obj):
        if obj.average_rating():
            return round(obj.average_rating(), 2)
        return None


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ['id', 'client']

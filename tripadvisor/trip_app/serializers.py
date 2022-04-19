
import rest_framework.fields
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CharField

from .models import Restaurant, Review


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = '__all__'
        depth = 1


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        depth = 1
# foods/serializers.py
from rest_framework import serializers
from .models import Meal, MealItem, FoodImage

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'meal_type', 'date', 'user']

class MealItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealItem
        fields = ['id', 'meal', 'food_name', 'calories', 'carbs', 'protein', 'fat']

class FoodImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodImage
        fields = ['id', 'image', 'user']

from rest_framework import serializers
from .models import Dish, DishIngredient
from ingredients.models import Ingredient


class DishIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.ReadOnlyField(source='ingredient.name')

    class Meta:
        model = DishIngredient
        fields = ['ingredient', 'ingredient_name', 'quantity']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('The amount of the ingredient must be greater than 0.')
        return value


class DishSerializer(serializers.ModelSerializer):
    ingredients = DishIngredientSerializer(source='dishingredient_set', many=True)

    class Meta:
        model = Dish
        fields = ['id', 'name', 'description', 'price', 'ingredients']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('The price of the dish must be greater than 0.')
        return value

    def create(self, validated_data):
        ingredients_data = validated_data.pop('dishingredient_set')
        dish = Dish.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            DishIngredient.objects.create(dish=dish, **ingredient_data)

        return dish

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('dishingredient_set')
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()

        instance.dishingredient_set.all().delete()
        for ingredient_data in ingredients_data:
            DishIngredient.objects.create(dish=instance, **ingredient_data)

        return instance

from rest_framework import serializers


from ingredients.models import Ingredient
from .models import Order, Dish, OrderDish
from tables.models import Table

class OrderDishSerializer(serializers.ModelSerializer):
    dish_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = OrderDish
        fields = ['dish_id', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    table = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all())
    order_dishes = OrderDishSerializer(many=True)

    order_time = serializers.DateTimeField(read_only=True)
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES, default='pending')

    class Meta:
        model = Order
        fields = ['id', 'table', 'order_dishes', 'order_time', 'status']

    def validate(self, data):
        order_dishes = data.get('order_dishes')
        if order_dishes:
            for dish_data in order_dishes:
                dish_instance = Dish.objects.get(id=dish_data['dish_id'])
                for dish_ingredient in dish_instance.dishingredient_set.all():
                    required_quantity = dish_ingredient.quantity * dish_data['quantity']
                    if not self.check_ingredients(dish_ingredient.ingredient, required_quantity):
                        raise serializers.ValidationError(
                            f"Not enough {dish_ingredient.ingredient.name} for dish {dish_instance.name}"
                        )
        return data

    def check_ingredients(self, ingredient, required_quantity):
        try:
            ingredient_instance = Ingredient.objects.get(id=ingredient.id)
            return ingredient_instance.quantity >= required_quantity
        except Ingredient.DoesNotExist:
            return False

    def create(self, validated_data):
        order_dishes_data = validated_data.pop('order_dishes')
        order = Order.objects.create(**validated_data)
        for dish_data in order_dishes_data:
            OrderDish.objects.create(order=order, dish_id=dish_data['dish_id'], quantity=dish_data['quantity'])


        self.update_ingredients(order_dishes_data, operation="deduct")

        return order

    def update_ingredients(self, order_dishes_data, operation="deduct"):
        for dish_data in order_dishes_data:
            dish_instance = Dish.objects.get(id=dish_data['dish_id'])
            for dish_ingredient in dish_instance.dishingredient_set.all():
                quantity = dish_ingredient.quantity * dish_data['quantity']
                if operation == "deduct":
                    self.deduct_ingredients(dish_ingredient.ingredient, quantity)
                elif operation == "add":
                    self.add_ingredients(dish_ingredient.ingredient, quantity)

    def deduct_ingredients(self, ingredient, quantity):
        try:
            ingredient_instance = Ingredient.objects.get(id=ingredient.id)
            if ingredient_instance.quantity >= quantity:
                ingredient_instance.quantity -= quantity
                ingredient_instance.save()
            else:
                raise serializers.ValidationError(f"Not enough {ingredient.name} to write off.")
        except Ingredient.DoesNotExist:
            raise serializers.ValidationError(f"Ingredient {ingredient.name} not found.")

    def add_ingredients(self, ingredient, quantity):
        try:
            ingredient_instance = Ingredient.objects.get(id=ingredient.id)
            ingredient_instance.quantity += quantity
            ingredient_instance.save()
        except Ingredient.DoesNotExist:
            raise serializers.ValidationError(f"Ingredient {ingredient.name} not found.")

    def update(self, instance, validated_data):
        old_order_dishes = instance.order_dishes.all()
        self.update_ingredients_from_order_dishes(old_order_dishes, operation="add")

        instance.order_dishes.all().delete()

        instance.table = validated_data.get('table', instance.table)
        instance.status = validated_data.get('status', instance.status)

        if 'order_dishes' in validated_data:
            order_dishes_data = validated_data.pop('order_dishes')
            for dish_data in order_dishes_data:
                OrderDish.objects.create(order=instance, dish_id=dish_data['dish_id'], quantity=dish_data['quantity'])
            self.update_ingredients(order_dishes_data, operation="deduct")

        instance.save()
        return instance

    def update_ingredients_from_order_dishes(self, order_dishes, operation="deduct"):
        for order_dish in order_dishes:
            dish_instance = order_dish.dish
            for dish_ingredient in dish_instance.dishingredient_set.all():
                quantity = dish_ingredient.quantity * order_dish.quantity
                if operation == "deduct":
                    self.deduct_ingredients(dish_ingredient.ingredient, quantity)
                elif operation == "add":
                    self.add_ingredients(dish_ingredient.ingredient, quantity)

from rest_framework import serializers

from suppliers.models import Supplier
from .models import Ingredient, SupplierIngredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('The quantity must be a positive number.')
        return value



class SupplierIngredientSerializer(serializers.ModelSerializer):
    supplier_name = serializers.SerializerMethodField()
    ingredient_name = serializers.SerializerMethodField()

    class Meta:
        model = SupplierIngredient
        fields = ['supplier', 'ingredient', 'price_per_unit', 'supplier_name', 'ingredient_name']

    def get_supplier_name(self, obj):
        return obj.supplier.name

    def get_ingredient_name(self, obj):
        return obj.ingredient.name

    def validate_price_per_unit(self, value):
        if value <= 0:
            raise serializers.ValidationError('The unit price must be a positive number.')
        return value

    def validate(self, data):
        supplier = data.get('supplier')
        ingredient = data.get('ingredient')

        if supplier and ingredient:
            if SupplierIngredient.objects.filter(supplier=supplier, ingredient__name__iexact=ingredient.name).exists():
                raise serializers.ValidationError(
                    f'The supplier {supplier.name} already supplies the ingredient named {ingredient.name}.'
                )
        return data


class PurchaseSerializer(serializers.Serializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    quantity = serializers.IntegerField(min_value=0)

    def validate(self, data):
        supplier = data.get('supplier')
        ingredient = data.get('ingredient')
        quantity = data.get('quantity')

        try:
            supplier_ingredient = SupplierIngredient.objects.get(supplier=supplier, ingredient=ingredient)
        except SupplierIngredient.DoesNotExist:
            raise serializers.ValidationError(f'Supplier {supplier.name} does not offer ingredient {ingredient.name}.')

        return data


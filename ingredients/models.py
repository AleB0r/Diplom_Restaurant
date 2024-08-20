from django.core.exceptions import ValidationError
from django.db import models
from suppliers.models import Supplier

class Ingredient(models.Model):
    MEASUREMENT_CHOICES = [
        ('kg', 'Kilograms'),
        ('ml', 'Milliliters'),
        ('pcs', 'Pieces'),
    ]

    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    measurement_unit = models.CharField(max_length=3, choices=MEASUREMENT_CHOICES, default='kg')

    def __str__(self):
        return self.name

class SupplierIngredient(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='supplier_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='supplier_ingredients')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('supplier', 'ingredient')

    def clean(self):
        if self.price_per_unit <= 0:
            raise ValidationError('The unit price must be a positive number.')

    def __str__(self):
        return f'{self.supplier.name} - {self.ingredient.name} @ {self.price_per_unit}'

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

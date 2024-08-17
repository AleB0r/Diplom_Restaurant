from django.db import models
from dishes.models import Dish
from tables.models import Table

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    @property
    def order_dishes(self):
        return OrderDish.objects.filter(order=self)

class OrderDish(models.Model):
    order = models.ForeignKey(Order, related_name='order_dishes', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Order {self.id} - {self.table}"

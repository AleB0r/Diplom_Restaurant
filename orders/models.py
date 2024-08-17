from django.db import models
from dishes.models import Dish
from tables.models import Table
from django.contrib.auth import get_user_model

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    dishes = models.ManyToManyField(Dish, related_name='orders')
    order_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Order {self.id} by {self.user}'

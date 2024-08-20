from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = [
        ('waiter', 'Waiter'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
        ('buyer', 'Buyer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='waiter')
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    contract_end_date = models.DateField(null=True, blank=True)
    last_activity = models.DateTimeField(default=timezone.now)
    last_action = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

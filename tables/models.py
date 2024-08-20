from django.db import models
from django.core.exceptions import ValidationError

class Table(models.Model):
    number = models.IntegerField(unique=True)
    seats = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def clean(self):
        if self.seats <= 0:
            raise ValidationError('The number of seats must be greater than 0.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def toggle_availability(self):
        self.is_available = not self.is_available
        self.save()

    def __str__(self):
        return f'Table {self.number}'

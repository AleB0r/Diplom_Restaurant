from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True, default='default@example.com')  # Добавлено поле email
    contact_info = models.TextField()

    def __str__(self):
        return self.name

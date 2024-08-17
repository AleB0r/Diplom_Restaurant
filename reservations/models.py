from django.db import models

from client.models import Client
from tables.models import Table


class Reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField()
    number_of_people = models.IntegerField()

    def __str__(self):
        return f'Reservation by {self.client} for table {self.table.number} at {self.reservation_time}'

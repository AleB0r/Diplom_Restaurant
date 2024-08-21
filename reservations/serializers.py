from rest_framework import serializers
from django.core.exceptions import ValidationError
from datetime import datetime, time, timedelta
import pytz

from .models import Reservation
from client.models import Client
from tables.models import Table

class ReservationSerializer(serializers.ModelSerializer):
    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source='client')
    table_id = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all(), source='table')
    table_number = serializers.CharField(source='table.number', read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'client_id', 'table_id', 'reservation_time', 'number_of_people', 'table_number']

    def validate_reservation_time(self, value):
        now = datetime.now(pytz.utc)
        start_time = datetime.combine(now.date(), time(9, 0), tzinfo=pytz.utc)
        end_time = datetime.combine(now.date() + timedelta(days=1), time(23, 0), tzinfo=pytz.utc)

        if value.minute % 30 != 0:
            raise serializers.ValidationError('Booking time must be a multiple of 30 minutes.')

        if not (start_time <= value <= end_time):
            raise serializers.ValidationError('Reservation time must be between 09:00 and 23:00.')

        if value < now:
            raise serializers.ValidationError('The booking time cannot be in the past.')

        return value

    def validate(self, data):
        reservation_time = data.get('reservation_time')
        table = data.get('table')

        if reservation_time and table:
            reservations = Reservation.objects.filter(
                table=table,
                reservation_time__date=reservation_time.date(),
                reservation_time__time__gte=(reservation_time - timedelta(minutes=30)).time(),
                reservation_time__time__lt=(reservation_time + timedelta(minutes=30)).time()
            ).exclude(id=self.instance.id if self.instance else None)

            if reservations.exists():
                raise serializers.ValidationError('This table is already booked for this time or within it.')

            if data.get('number_of_people') > table.seats:
                raise serializers.ValidationError('The number of people seated cannot exceed the number of seats at the table.')

        return data

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

from rest_framework import serializers
from django.core.exceptions import ValidationError
from datetime import datetime, time, timedelta
import pytz  # Убедитесь, что pytz установлен

from .models import Reservation
from client.models import Client
from tables.models import Table

class ReservationSerializer(serializers.ModelSerializer):
    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source='client')
    table_id = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all(), source='table')
    table_number = serializers.CharField(source='table.number', read_only=True)  # Номер стола для чтения

    class Meta:
        model = Reservation
        fields = ['id', 'client_id', 'table_id', 'reservation_time', 'number_of_people', 'table_number']

    def validate_reservation_time(self, value):
        """Проверка времени бронирования."""
        now = datetime.now(pytz.utc)  # Получить текущее время с временной зоной
        start_time = datetime.combine(now.date(), time(9, 0), tzinfo=pytz.utc)  # Начало временного диапазона
        end_time = datetime.combine(now.date() + timedelta(days=1), time(21, 0), tzinfo=pytz.utc)  # Конец временного диапазона

        # Проверка кратности 30 минутам
        if value.minute % 30 != 0:
            raise serializers.ValidationError('Время бронирования должно быть кратным 30 минутам.')

        # Проверка на в пределах времени
        if not (start_time <= value <= end_time):
            raise serializers.ValidationError('Время бронирования должно быть между 09:00 и 21:00.')

        # Проверка, что время не в прошлом
        if value < now:
            raise serializers.ValidationError('Время бронирования не может быть в прошлом.')

        return value

    def validate(self, data):
        """Проверка пересечения бронирований и других условий."""
        reservation_time = data.get('reservation_time')
        table = data.get('table')

        if reservation_time and table:
            # Проверка на пересечение бронирований
            reservations = Reservation.objects.filter(
                table=table,
                reservation_time__date=reservation_time.date(),
                reservation_time__time__gte=(reservation_time - timedelta(minutes=30)).time(),
                reservation_time__time__lt=(reservation_time + timedelta(minutes=30)).time()
            ).exclude(id=self.instance.id if self.instance else None)

            if reservations.exists():
                raise serializers.ValidationError('Этот столик уже забронирован на это время или в его пределах.')

            # Проверка на количество сидений
            if data.get('number_of_people') > table.seats:
                raise serializers.ValidationError('Число сидящих не может превышать количество мест за столом.')

        return data

    def create(self, validated_data):
        # Создание бронирования
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Обновление бронирования
        return super().update(instance, validated_data)

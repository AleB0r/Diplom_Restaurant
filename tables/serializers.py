from rest_framework import serializers
from .models import Table

class TableSerializer(serializers.ModelSerializer):
    is_available = serializers.BooleanField(read_only=True)
    class Meta:
        model = Table
        fields = ['number', 'seats','is_available']

    def validate_seats(self, value):
        if value <= 0:
            raise serializers.ValidationError('Количество сидений должно быть больше 0.')
        return value

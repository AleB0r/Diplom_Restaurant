from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name','phone_number']
        read_only_fields = ['id']

    def validate_email(self, value):
        if Client.objects.filter(email=value).exists():
            raise serializers.ValidationError('A client with this email already exists.')
        return value

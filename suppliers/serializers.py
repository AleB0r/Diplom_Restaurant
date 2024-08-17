from rest_framework import serializers
from .models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'contact_info']  # Не включаем 'id' в поля для создания
        read_only_fields = ['id']  # Указываем, что 'id' только для чтения

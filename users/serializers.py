from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8)
    password_confirm = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'salary', 'contract_end_date', 'password', 'password_confirm']
        read_only_fields = ['id']

    def validate(self, data):
        """
        Проверка того, что пароли совпадают, если они предоставлены.
        """
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password or password_confirm:
            if password != password_confirm:
                raise serializers.ValidationError({"password": "Пароли не совпадают."})


        return data

    def create(self, validated_data):
        """
        Создание нового пользователя с зашифрованным паролем.
        """
        password = validated_data.pop('password', None)
        password_confirm = validated_data.pop('password_confirm', None)

        if password and password_confirm:
            if password != password_confirm:
                raise serializers.ValidationError({"password": "Пароли не совпадают."})

        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role'),
            salary=validated_data.get('salary'),
            contract_end_date=validated_data.get('contract_end_date')
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Обновление существующего пользователя, включая возможность изменения пароля.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.contract_end_date = validated_data.get('contract_end_date', instance.contract_end_date)

        # Обработка пароля
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance

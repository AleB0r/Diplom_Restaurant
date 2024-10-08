from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8)
    password_confirm = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'salary', 'contract_end_date', 'password', 'password_confirm']
        read_only_fields = ['id']

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password or password_confirm:
            if password != password_confirm:
                raise serializers.ValidationError({"password": "The passwords do not match."})


        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)

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
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.contract_end_date = validated_data.get('contract_end_date', instance.contract_end_date)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
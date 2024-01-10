from rest_framework import serializers
from .models import User

class SellerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['is_seller'] = True  # Устанавливаем is_seller автоматически
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active = True  # Активируем пользователя
        user.save()
        return user

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['is_seller'] = False  # Устанавливаем is_seller автоматически
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active = True  # Активируем пользователя
        user.save()
        return user
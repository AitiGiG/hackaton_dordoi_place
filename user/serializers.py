from rest_framework import serializers

from .models import User


class SellerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password','password_confirmation', 'shop_name')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password_conf = attrs.pop('password_confirmation')
        if password_conf != attrs['password']:
            raise serializers.ValidationError(
                'Пароли не совпадают'
            )
        return attrs

    def create(self, validated_data):
        validated_data['is_seller'] = True 
        user = User.objects.create_user(**validated_data, is_active=False)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirmation', 'username')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password_conf = attrs.pop('password_confirmation')
        if password_conf != attrs['password']:
            raise serializers.ValidationError(
                'Пароли не совпадают'
            )
        
    
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, is_active=False)
        user.set_password(validated_data['password'])
        user.save()
        return user
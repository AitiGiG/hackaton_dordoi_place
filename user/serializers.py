from rest_framework import serializers
from .models import User
from busket.serializers import BusketSerializer
from favorite.serializers import FavoriteSerializer
from review.serializers import ReviewSerializer
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
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active = True 
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
        validated_data['is_seller'] = False 
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active = True  
        user.save()
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'shop_name', 'buskets', 'favorites', 'reviews')
        extra_kwargs = {'password': {'write_only': True}}

    buskets = serializers.SerializerMethodField(method_name='get_buskets')
    favorites = serializers.SerializerMethodField(method_name='get_favorites')
    reviews = serializers.SerializerMethodField(method_name='get_reviews')
    def get_buskets(self, instance):
        buskets = getattr(instance, 'buskets', None)
        if buskets is not None:
            buskets_data = BusketSerializer(buskets.all(), many=True).data
            return buskets_data
        return None
    def get_favorites(self, instance):
        favorites = getattr(instance, 'buskets', None)
        if favorites is not None:
            favorites_data = FavoriteSerializer(favorites.all(), many=True).data
            return favorites_data
        return None  # Или подходящее значение по умолчанию, если favorites не существует
    
    def get_reviews(self, instance):
        reviews = instance.reviews.all()
        serializer = ReviewSerializer(
            reviews, many=True
        ) 
        return serializer.data
from rest_framework.serializers import ModelSerializer
from .models import Product
from rest_framework import serializers
from category.models import Category
from busket.serializers import BusketSerializer
from favorite.serializers import FavoriteSerializer
from review.serializers import ReviewSerializer

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'category', 'subcategory', 'price', 'description', 'image', 'quantity', 'available', 'favorites', 'owner', 'reviews']

    owner = serializers.ReadOnlyField(source='owner.email')
    favorites = serializers.SerializerMethodField(method_name='get_favorites_counter')

    reviews = serializers.SerializerMethodField(method_name='get_reviews')
    def get_favorites_counter(self, instance):
        favorites_counter = instance.favorites.all().count()
        return favorites_counter

      
    def get_reviews(self, instance):
        reviews = instance.reviews.all()
        serializer = ReviewSerializer(
            reviews, many=True
        ) 
        return serializer.data

    

    def get_favorites_counter(self, instance):
        favorites = getattr(instance, 'favorites', None)
        if favorites is not None:
            favorites_data = FavoriteSerializer(favorites.all(), many=True).data
            return favorites_data
        return None 

    


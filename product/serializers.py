from rest_framework.serializers import ModelSerializer
from .models import Product
from rest_framework import serializers
from category.models import Category
from busket.serializers import BusketSerializer
from favorite.serializers import FavoriteSerializer

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'category', 'subcategory', 'price', 'description', 'image', 'quantity', 'available', 'favorites', 'owner']

    owner = serializers.ReadOnlyField(source='owner.email')
    category = serializers.StringRelatedField()
    subcategory = serializers.StringRelatedField()
    favorites = serializers.SerializerMethodField(method_name='get_favorites_counter')
    

    def get_favorites_counter(self, instance):
        favorites = getattr(instance, 'favorites', None)
        if favorites is not None:
            favorites_data = FavoriteSerializer(favorites.all(), many=True).data
            return favorites_data
        return None 

    

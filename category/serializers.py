from rest_framework import serializers
from .models import Category, Subcategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def __str__(self):
        return self.title
    
    
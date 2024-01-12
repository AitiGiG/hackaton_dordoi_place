from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source='owner.email')
    product = serializers.ReadOnlyField(source='product.title')

    class Meta:
        exclude = ['created_at']
        model = Review
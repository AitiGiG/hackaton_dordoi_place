from rest_framework import serializers
from .models import Busket

class BusketSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    post = serializers.ReadOnlyField(source='product.title')
    quantity = serializers.IntegerField()
    class Meta:
        model = Busket
        fields = '__all__'

    # def to_representation(self, instance):
    #     repr = super().to_representation(instance)
    #     return repr
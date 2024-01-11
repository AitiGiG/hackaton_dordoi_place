from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .serializers import ProductSerializer
from .models import Product
from .permissions import IsSellerPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from favorite.models import Favorite


class StandartResultPagination(PageNumberPagination):
    page_size = 5
    page_query_param= 'page'

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']
    filersets_fields = ['category']
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsSellerPermission(), ]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['POST'])
    def toggle_favorite(self, request, pk=None):
        product = self.get_object()
    
    # Проверяем, добавил ли пользователь товар в избранное
        favorite_exists = Favorite.objects.filter(product=product, owner=request.user).exists()

        if favorite_exists:
            # Если товар уже в избранном, удаляем его оттуда
            Favorite.objects.filter(product=product, owner=request.user).delete()
            return Response('Успешно удалено', status=204)
        else:
            # Если товар не в избранном, добавляем его
            Favorite.objects.create(product=product, owner=request.user)
            return Response('Успешно добавлено', status=201)





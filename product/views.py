from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .serializers import ProductSerializer
from .models import Product
from .permissions import IsOwnerOrAdmin

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
        if self.request.method in ['POST', 'PATCH', 'PUT', 'DELETE']:
            return [permissions.IsAdminUser(), IsOwnerOrAdmin()]
        return [permissions.AllowAny()]





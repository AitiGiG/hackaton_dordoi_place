from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from .serializers import ReviewSerializer
from .models import Review
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .permissions import IsOwner
from rest_framework.decorators import action
from rest_framework.response import Response

class StandartResultPagination(PageNumberPagination):
    page_size = 1
    page_query_param = 'page'


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = StandartResultPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ['content']
    filterset_fields = ['product']

    @action(detail=False, methods=['GET'])
    def get_user_comments(self, request):
        user_comments = Review.objects.filter(owner=request.user)
        serializer = ReviewSerializer(user_comments, many=True)
        return Response(serializer.data)


    def get_permissions(self, request, *args, **kwargs):
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated(), IsOwner()]
        return [permissions.AllowAny()]


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)




from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, BusketViewSet, FavoriteViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'busket', BusketViewSet, basename='busket')
router.register(r'favorite', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
]

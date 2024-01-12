from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet

router = DefaultRouter()
router.register(r'', ReviewViewSet, basename='product') 

urlpatterns = [
    path('', include(router.urls)),
    # path('', ProductViewSet.as_view()),
]
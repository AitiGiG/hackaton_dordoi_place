from django.urls import path, include
from .views import SellerRegistrationAPIView, UserRegistrationAPIView, LoginView, LogoutView, RefreshTokenView, UserViewSet 
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns = [
    path('register/seller/', SellerRegistrationAPIView.as_view(), name='register_seller'),
    path('register/user/', UserRegistrationAPIView.as_view(), name='register_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh'),
    path('', include(router.urls)),
]
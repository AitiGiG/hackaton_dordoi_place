from django.urls import path
from .views import SellerRegistrationAPIView, UserRegistrationAPIView, LoginView, LogoutView

urlpatterns = [
    path('register/seller/', SellerRegistrationAPIView.as_view(), name='register_seller'),
    path('register/user/', UserRegistrationAPIView.as_view(), name='register_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
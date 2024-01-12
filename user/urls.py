
from django.urls import path
from .views import SellerRegistrationAPIView, UserRegistrationAPIView, LoginView, LogoutView, RefreshTokenView, ActivateUserView, PasswordResetConfirmView, PasswordResetRequestView
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
    path('activate/<str:token>/',ActivateUserView.as_view() , name='activate_user'),
    path('password_reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('', include(router.urls)),

]
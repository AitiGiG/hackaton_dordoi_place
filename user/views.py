from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView, TokenRefreshView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils import timezone
from datetime import timedelta
import secrets
from .models import User
from .serializers import SellerRegistrationSerializer, UserRegistrationSerializer
from .tasks import send_activation_email, send_password_reset_email
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from .models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from busket.models import Busket
from product.models import Product
from .serializers import SellerRegistrationSerializer, UserRegistrationSerializer ,UserSerializer


class SellerRegistrationAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SellerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.activation_token = secrets.token_urlsafe()
            user.activation_token_expires = timezone.now() + timedelta(days=1)
            activate_link = request.build_absolute_uri(f'/user/activate/{user.activation_token}')
            user.save()
            send_activation_email.delay(user.email, activate_link)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.activation_token = secrets.token_urlsafe()
            user.activation_token_expires = timezone.now() + timedelta(days=1)
            activate_link = request.build_absolute_uri(f'/user/activate/{user.activation_token}')
            user.save()
            send_activation_email.delay(user.email, activate_link)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

class LogoutView(TokenBlacklistView):
    permission_classes = [permissions.AllowAny]

class RefreshTokenView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]


class ActivateUserView(APIView):
    def get(self, request, token):
        try:
            user = User.objects.get(activation_token=token, activation_token_expires__gte=timezone.now())
            user.is_active = True
            user.activation_token = None
            user.activation_token_expires = None
            user.save()
            return Response({'message': 'Account activated successfully'})
        except User.DoesNotExist:
            return Response({'error': 'Invalid or expired token'}, status=404)


class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=400)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = request.build_absolute_uri(f'/user/reset-password-confirm/{uid}/{token}/')
        send_password_reset_email.delay(email, reset_link)
        return Response({'message': 'Password reset email sent'})
    
class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.data.get('password')
            user.set_password(new_password)
            user.save()
            return Response ({'message': 'Password reset successfully'})
        else:
            return Response({'error': 'Invalid reset token or User ID'}, status=400)

        
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # if User.is_seller:
    #     serializer_class = SellerRegistrationSerializer
    # else:
    #     serializer_class = UserRegistrationSerializer



# referral_program/app/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import (
    CustomTokenObtainPairSerializer,
    RefereeDetailSerializer,
    UserDetailSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
)

from django.utils import timezone


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Takes email and password, returns JWT access and refresh tokens.
    Uses the custom serializer to work with the 'email' field.
    """

    serializer_class = CustomTokenObtainPairSerializer


# --- User Registration View ---
class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can register

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "User registered successfully."},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


# --- Custom User Login View (for /api/login/) ---


class UserLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                return Response(
                    {"error": "Invalid Credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if user is not None and user.is_active:
            # Optional: Update last_login
            user.last_login = timezone.now()
            user.save(update_fields=["last_login"])

            response_serializer = UserDetailSerializer(user)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"error": "Invalid Credentials or Inactive User"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


# --- User Referrals View ---


class UserReferralsAPIView(generics.ListAPIView):
    serializer_class = RefereeDetailSerializer
    # Enforce authentication
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return a list of users referred by the currently authenticated user.
        Uses request.user provided by DRF/JWT authentication.
        """
        user = self.request.user
        if user and user.is_authenticated:
            return user.referees.all().order_by("-registration_datetime")
        return User.objects.none()  # Return empty if user not authenticated

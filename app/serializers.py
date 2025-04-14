# referral_program/app/serializers.py

import uuid

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
# Import the SimpleJWT serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User

# --- Custom Token Serializer ---
# This serializer ensures SimpleJWT uses the 'email' field based on your User model's USERNAME_FIELD


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # This method generates the token once the user is authenticated.
        token = super().get_token(user)
        # You can add custom claims to the token here if needed
        # token['name'] = user.name
        return token

    def validate(self, attrs):
        # This method validates the credentials provided in the request.
        # It relies on the parent class's validation, which should correctly
        # use the AUTH_USER_MODEL and its USERNAME_FIELD ('email').
        data = super().validate(attrs)
        # You can add extra data to the response here if needed
        # data['user_id'] = self.user.id
        # data['email'] = self.user.email
        return data


# --- User Registration Serializer ---


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    referral = serializers.CharField(
        max_length=10, required=False, allow_blank=True, write_only=True
    )

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "mobile_number",
            "city",
            "password",
            "referral",
        ]
        extra_kwargs = {
            "email": {"required": True},
            "name": {"required": True},
            "mobile_number": {"required": True},
            "city": {"required": True},
        }

    def validate_referral_code_used(self, value):
        if value:
            try:
                User.objects.get(referral_code=value)
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid referral code provided.")
        return value

    def create(self, validated_data):
        referral_code_used = validated_data.pop("referral", None)
        referrer = None
        if referral_code_used:
            referrer = User.objects.get(referral_code=referral_code_used)

        user = User(
            email=validated_data["email"],
            name=validated_data["name"],
            mobile_number=validated_data["mobile_number"],
            city=validated_data["city"],
            referrer=referrer,
        )
        user.set_password(validated_data["password"])  # Hash password

        user.referral_code = str(uuid.uuid4())[:8]
        while User.objects.filter(referral_code=user.referral_code).exists():
            user.referral_code = str(uuid.uuid4())[:8]

        user.save()
        return user


# --- User Login Serializer (for the custom /api/login/ endpoint) ---


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )


# --- User Detail Serializer (for the custom /api/login/ response) ---


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


# --- Referee Detail Serializer (for the /api/referrals/ endpoint) ---


class RefereeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "registration_datetime"]

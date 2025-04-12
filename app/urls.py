# referral_program/app/urls.py
from django.urls import path

# Make sure to import the new API view classes
from .views import (UserLoginAPIView, UserReferralsAPIView,
                    UserRegistrationAPIView)

urlpatterns = [
    # Use UserRegistrationAPIView.as_view() instead of register_view
    path("api/register/", UserRegistrationAPIView.as_view(), name="api_register"),
    # Use UserLoginAPIView.as_view() instead of login_view
    path("api/login/", UserLoginAPIView.as_view(), name="api_login"),
    # Use UserReferralsAPIView.as_view() for the referrals endpoint
    path("api/referrals/", UserReferralsAPIView.as_view(), name="api_referrals"),
]

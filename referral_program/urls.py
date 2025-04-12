# referral_program/urls.py

from django.contrib import admin
from django.urls import path, include
# Import the default Refresh view
from rest_framework_simplejwt.views import TokenRefreshView
# Import your custom Obtain view from app.views
from app.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- JWT Token Endpoints ---
    # Use your custom view for obtaining the token pair (/api/token/)
    path('api/token/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    # Keep the default view for refreshing the token (/api/token/refresh/)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # --- App API Endpoints ---
    # Include your app's URLs (register, login, referrals)
    # This line includes the paths defined in app/urls.py
    path('', include('app.urls')),
]

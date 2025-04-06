# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
]

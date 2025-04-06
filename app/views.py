from django.contrib.auth.decorators import login_required  # <--- IMPORT THIS
from django.contrib.auth import authenticate, login as auth_login  # <-- IMPORT login
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from app.forms import LoginForm
from .models import User  # <-- Import User model
from django.contrib.auth.hashers import check_password


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Registration successful! Please log in.')
            return redirect('login')  # Redirect to login page name/URL
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'app/registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Manual Authentication Check:
            try:
                user = User.objects.get(email=email)
                # Check password using the hash stored in the database
                if check_password(password, user.password):
                    # Password is correct! Log the user in to establish a session
                    # <--- Use Django's login function
                    auth_login(request, user)
                    messages.success(
                        request, f'Login successful! Welcome {user.name}.')
                    return redirect('home')  # Redirect to the home page
                else:
                    # Password incorrect
                    messages.error(request, 'Invalid email or password.')
            except User.DoesNotExist:
                # User email not found
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})


@login_required
def home_view(request):
    return render(request, 'app/home.html')

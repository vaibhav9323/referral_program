# referral_program/app/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

# --- Custom User Manager ---
# Required when using AbstractBaseUser


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hashes the password

        # Generate unique referral code
        user.referral_code = str(uuid.uuid4())[:8]
        while self.model.objects.filter(referral_code=user.referral_code).exists():
            user.referral_code = str(uuid.uuid4())[:8]

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # Superusers should be active
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Create the user using the regular create_user method
        user = self.create_user(email, password, **extra_fields)
        return user

    # This method is crucial for ModelBackend authentication with email as USERNAME_FIELD
    def get_by_natural_key(self, email):
        return self.get(email=email)


# --- Custom User Model ---
# Inherits from AbstractBaseUser and PermissionsMixin
class User(AbstractBaseUser, PermissionsMixin):
    # Mandatory, unique identifier
    email = models.EmailField(unique=True, blank=False, null=False)
    name = models.CharField(max_length=100, blank=False,
                            null=False)  # Mandatory
    mobile_number = models.CharField(
        max_length=15, blank=False, null=False)  # Mandatory
    city = models.CharField(max_length=100, blank=False,
                            null=False)  # Mandatory

    # Referral fields
    referral_code = models.CharField(
        max_length=10, unique=True, blank=True, null=True)  # Generated automatically
    referrer = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,  # Keep referee even if referrer is deleted
        null=True,
        blank=True,
        related_name='referees'  # Easy access to users referred by this user
    )
    registration_datetime = models.DateTimeField(auto_now_add=True)

    # Fields required by Django admin and auth system
    # AbstractBaseUser provides 'password' and 'last_login'
    is_staff = models.BooleanField(default=False)  # Required for admin access
    # Designates whether this user should be treated as active.
    is_active = models.BooleanField(default=True)
    # PermissionsMixin provides 'is_superuser', 'groups', 'user_permissions'

    # --- Configuration ---
    objects = UserManager()  # Use the custom manager

    USERNAME_FIELD = 'email'  # Use email for login instead of username
    # Fields prompted for createsuperuser command
    REQUIRED_FIELDS = ['name', 'mobile_number', 'city']

    def __str__(self):
        return self.email

    # No need for set_password or check_password here, AbstractBaseUser handles it.
    # No need for is_authenticated, is_anonymous, has_perm, has_module_perms here,
    # AbstractBaseUser and PermissionsMixin handle them.

    # Override save to handle referrer linking if needed during registration
    # Note: Referral code generation is now handled in the UserManager.create_user
    # Referrer linking logic might be better placed in the registration serializer/view.
    # def save(self, *args, **kwargs):
    #     # Example: If linking referrer based on a field set before save
    #     # referral_code_used = getattr(self, '_referral_code_used', None)
    #     # if referral_code_used and not self.referrer_id:
    #     #     try:
    #     #         referrer = User.objects.get(referral_code=referral_code_used)
    #     #         self.referrer = referrer
    #     #     except User.DoesNotExist:
    #     #         pass # Or handle error
    #     super().save(*args, **kwargs)

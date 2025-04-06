from django.db import models
import uuid


class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(
        max_length=15)
    city = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    referral_code = models.CharField(
        max_length=10, unique=True, blank=True)
    referrer = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referees'
    )
    registration_datetime = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_referral_code_used = models.BooleanField(default=False)

    def __str__(self):
        return self.email

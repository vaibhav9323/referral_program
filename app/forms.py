import uuid

from django import forms
from django.contrib.auth.hashers import make_password

from .models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password"
    )
    # Field for entering someone else's code
    referral_code_used = forms.CharField(
        required=False, max_length=10, label="Referral Code (Optional)"
    )

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "mobile_number",
            "city",
            "password",
            "password_confirm",
            "referral_code_used",
        ]

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match")
        return password_confirm

    def clean_referral_code_used(self):
        code = self.cleaned_data.get("referral_code_used")
        if code:
            try:
                # Check if a user exists with this code
                User.objects.get(referral_code=code)
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid referral code.")
        return code

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])

        # Generate unique referral code for this new user
        # Example: Generate an 8-char code
        user.referral_code = str(uuid.uuid4())[:8]
        # Ensure uniqueness (add retry logic if needed in a real app)
        while User.objects.filter(referral_code=user.referral_code).exists():
            user.referral_code = str(uuid.uuid4())[:8]

        # Link to referrer if code was used
        referral_code_used = self.cleaned_data.get("referral_code_used")
        if referral_code_used:
            try:
                referrer = User.objects.get(referral_code=referral_code_used)
                user.referrer = referrer
            except User.DoesNotExist:
                pass

        if commit:
            user.save()
        return user


# users/forms.py (add this class)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label="Confirm password", max_length=100, widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) <= 3:
            self.add_error(
                "username",
                "That username is too short. It must contain at least 4 characters.",
            )
        elif not re.search(r"^\w+$", username):
            self.add_error(
                "username",
                "Username can only contain alphanumeric characters and the underscore.",
            )
        elif User.objects.filter(username=username):
            self.add_error(
                "username", "That user is already taken , please select another."
            )
        return username

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.pop("confirm_password")
        try:
            validate_password(password, User(**self.cleaned_data))
        except ValidationError as e:
            self.add_error("password", e)

        if password != confirm_password:
            self.add_error("confirm_password", "Password does not match.")

        return confirm_password


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

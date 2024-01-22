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

    def clean(self):
        cleaned_data = super().clean()

        # username validation
        username = cleaned_data.get("username")
        user = User.objects.filter(username=username)
        if user:
            self.add_error(
                "username", "That user is already taken , please select another"
            )
        elif not re.search(r"^\w+$", username):
            self.add_error(
                "username",
                "Username can only contain alphanumeric characters and the underscore.",
            )
        self.add_error("username", self.instance)

        # password validation
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        user = User(
            username=cleaned_data.get("username"),
            first_name=cleaned_data.get("first_name"),
            last_name=cleaned_data.get("last_name"),
            email=cleaned_data.get("email"),
            password=cleaned_data.get("password"),
        )
        try:
            validate_password(password, user)
        except ValidationError as e:
            self.add_error("password", e)

        if password != confirm_password:
            self.add_error("confirm_password", "Password does not match")


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

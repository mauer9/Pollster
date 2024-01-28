import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm as BasePasswordChangeForm
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
        data = self.cleaned_data
        password = data.get("password")
        confirm_password = data.pop("confirm_password")
        try:
            validate_password(password, User(**data))
        except ValidationError as e:
            self.add_error("password", e)

        if password != confirm_password:
            self.add_error("confirm_password", "Password does not match.")

        return confirm_password


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class PasswordChangeForm(BasePasswordChangeForm):
    """
    rewriting methods because
    a) it does not validate for old_password and new_password similarity
    b) validate_password(password1, self.user) executed in
    clean_new_password2 method, which assigns errors to new_password2 input
    """

    def clean_new_password1(self):
        old_password = self.cleaned_data.get("old_password")
        password1 = self.cleaned_data.get("new_password1")
        if password1 and old_password and password1 == old_password:
            raise ValidationError(
                "Your new password must be different from old password",
                code="same_password",
            )
        validate_password(password1, self.user)
        return password1

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

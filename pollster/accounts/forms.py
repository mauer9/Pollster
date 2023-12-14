from django import forms
from django.contrib.auth.models import User
from django.contrib.auth .password_validation import validate_password
from django.core.exceptions import ValidationError



class SignupForm(forms.ModelForm):
    password         = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm password', max_length=100, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        try: validate_password(password)
        except ValidationError as e: self.add_error('password', e)
        if password != confirm_password:
            self.add_error("confirm_password",'Password does not match')

        if len(username) < 5:
            self.add_error("username", 'Username too short, must be longer than 5 characters')


class LoginForm(forms.Form):
    uername = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())

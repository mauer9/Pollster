from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_bootstrap5.bootstrap5 import FloatingField

class SignupForm(forms.Form):
    name = forms.CharField(label='your name', max_length=100)
    email = forms.EmailField(label='your email', max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            FloatingField("name", css_class='text-dark'),
            FloatingField("email", css_class='text-dark'),
        )


from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Row, Column, HTML, Submit, Layout
from crispy_bootstrap5.bootstrap5 import FloatingField

class SignupForm(forms.Form):
    first_name       = forms.CharField(max_length=100, required=False)
    last_name        = forms.CharField(max_length=100, required=False)
    username         = forms.CharField(max_length=100)
    email            = forms.EmailField(max_length=100, required=False)
    password         = forms.CharField(max_length=100, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput())

    helper = FormHelper()
    helper.layout = Layout(
        HTML("<h1 class='text-white mb-5'>Sign up to Pollster</h1>"),
        Row(
            Column(FloatingField("first_name", wrapper_class='text-dark')),
            Column(FloatingField("last_name", wrapper_class='text-dark')),
            css_class='g-3'
        ),
        FloatingField("email",    wrapper_class='text-dark'),
        FloatingField("username", wrapper_class='text-dark'),
        Row(
            Column(FloatingField("password", wrapper_class='text-dark')),
            Column(FloatingField("confirm_password", wrapper_class='text-dark')),
            css_class='g-3'
        ),
        HTML("""
            <p>
                Already have an account? Sign In
                <a
                href="{% url 'accounts:login' %}"
                class="link-light link-offset-2">
                    Log In
                </a>
            </p>
        """),
        Submit("submit", "Submit", css_class="btn btn-primary"),
    )
    helper.render_required_fields = True

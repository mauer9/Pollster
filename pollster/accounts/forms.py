from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Row, Div, HTML, Submit, Layout
from crispy_bootstrap5.bootstrap5 import FloatingField

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    username = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100, required=False)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput())

    helper = FormHelper()
    helper.layout = Layout(
        HTML("<h1 class='text-white mb-5'>Sign up to Pollster</h1>"),
        Row(
            FloatingField("first_name", wrapper_class='text-dark col-6 pe-1'),
            FloatingField("last_name", wrapper_class='text-dark col-6 ps-1'),
        ),
        FloatingField("username", wrapper_class='text-dark'),
        FloatingField("email", wrapper_class='text-dark'),
        Row(
            FloatingField("password", wrapper_class='text-dark col-6 pe-1'),
            FloatingField("confirm_password", wrapper_class='text-dark col-6 ps-1'),
        ),
        HTML("""<p>Already have an account? Sign In <a href="{% url 'accounts:login' %}" class="link-light link-offset-2">Log In</a></p>"""),
        Submit("submit", "Submit", css_class="btn btn-primary"),
    )
    helper.render_required_fields = True


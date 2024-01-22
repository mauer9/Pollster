from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm
from django.contrib.auth.models import User


def login(request):
    if request.user.is_authenticated:
        return redirect("polls:index")

    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("polls:index")
        context["error_message"] = "Sorry, your email and password did not match"
        context["error_css"] = "is-invalid"
    context["form"] = LoginForm()
    return render(request, "accounts/login.html", context)


@login_required(redirect_field_name=None)
def logout(request):
    auth_logout(request)
    return redirect("home")


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    context = {}
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            del cleaned_data["confirm_password"]
            user = User.objects.create_user(**cleaned_data)
            auth_login(request, user)
            return redirect("polls:index")
        else:
            for field in form.fields:
                context[field + "_value"] = request.POST[field]
                context[field + "_css"] = "is-valid"
                if field in form.errors:
                    context[field + "_css"] = "is-invalid"
                    context[field + "_feedback"] = form.errors[field]
    else:
        form = SignupForm()

    context["form"] = form
    return render(request, "accounts/signup.html", context)

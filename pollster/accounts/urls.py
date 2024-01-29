from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("votes/", views.MyPolls.as_view(), name="votes"),
    path(
        "change-password/", views.PasswordChangeView.as_view(), name="change-password"
    ),
    path("delete/", views.DeleteAccountView.as_view(), name="delete"),
]

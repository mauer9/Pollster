import debug_toolbar
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path
from django.urls import include


urlpatterns = [
    path("__debug__/", include(debug_toolbar.urls)),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("accounts/", include("pollster.accounts.urls"), name="accounts"),
    path("admin/", admin.site.urls, name="admin"),
    path("polls/", include("pollster.polls.urls"), name="index"),
]

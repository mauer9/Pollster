from django.urls import path
from . import views


app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/vote/", views.vote, name="vote"),
    path("add/", views.AddPollView.as_view(), name="add"),
    path("test/", views.TestView.as_view(), name="test"),
]
